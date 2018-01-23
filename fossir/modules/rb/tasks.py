

from __future__ import unicode_literals

from datetime import date, datetime
from itertools import groupby
from operator import attrgetter

from celery.schedules import crontab
from sqlalchemy.orm import contains_eager

from fossir.core.celery import celery
from fossir.core.config import config
from fossir.core.db import db
from fossir.modules.rb import logger, rb_settings
from fossir.modules.rb.models.reservation_occurrences import ReservationOccurrence
from fossir.modules.rb.models.reservations import RepeatFrequency, Reservation
from fossir.modules.rb.models.rooms import Room
from fossir.modules.rb.notifications.reservation_occurrences import notify_upcoming_occurrences
from fossir.util.console import cformat


def _make_occurrence_date_filter():
    _default = rb_settings.get('notification_before_days')
    _default_weekly = rb_settings.get('notification_before_days_weekly')
    _default_monthly = rb_settings.get('notification_before_days_monthly')
    notification_before_days_room = db.case({RepeatFrequency.WEEK.value: Room.notification_before_days_weekly,
                                             RepeatFrequency.MONTH.value: Room.notification_before_days_monthly},
                                            else_=Room.notification_before_days, value=Reservation.repeat_frequency)
    notification_before_days_default = db.case({RepeatFrequency.WEEK.value: _default_weekly,
                                                RepeatFrequency.MONTH.value: _default_monthly},
                                               else_=_default, value=Reservation.repeat_frequency)
    notification_before_days = db.func.coalesce(notification_before_days_room, notification_before_days_default)
    days_until_occurrence = db.cast(ReservationOccurrence.start_dt, db.Date) - date.today()
    return days_until_occurrence == notification_before_days


def _print_occurrences(user, occurrences, _defaults={}, _overrides={}):
    if not _defaults or not _overrides:
        _defaults.update({RepeatFrequency.WEEK: rb_settings.get('notification_before_days_weekly'),
                          RepeatFrequency.MONTH: rb_settings.get('notification_before_days_monthly'),
                          RepeatFrequency.NEVER: rb_settings.get('notification_before_days'),
                          RepeatFrequency.DAY: rb_settings.get('notification_before_days')})
        _overrides.update({RepeatFrequency.WEEK: lambda r: r.notification_before_days_weekly,
                           RepeatFrequency.MONTH: lambda r: r.notification_before_days_monthly,
                           RepeatFrequency.NEVER: lambda r: r.notification_before_days,
                           RepeatFrequency.DAY: lambda r: r.notification_before_days})
    print cformat('%{grey!}*** {} ({}) ***').format(user.full_name, user.email)
    for occ in occurrences:
        default = _defaults[occ.reservation.repeat_frequency]
        override = _overrides[occ.reservation.repeat_frequency](occ.reservation.room)
        days = default if override is None else override
        days_until = (occ.start_dt.date() - date.today()).days
        print cformat('  * %{yellow}{}%{reset} %{green}{:5}%{reset} {} {} {} \t %{blue!}{}%{reset} {} ({})').format(
            occ.start_dt.date(), occ.reservation.repeat_frequency.name,
            days,
            default if override is not None and override != default else ' ',
            days_until,
            occ.reservation.id,
            occ.reservation.room.full_name,
            occ.reservation.room.id
        )


def _notify_occurrences(user, occurrences):
    notify_upcoming_occurrences(user, occurrences)
    for occ in occurrences:
        occ.notification_sent = True
        if occ.reservation.repeat_frequency == RepeatFrequency.DAY:
            future_occurrences_query = (occ.reservation.occurrences
                                        .filter(ReservationOccurrence.start_dt >= datetime.now()))
            future_occurrences_query.update({'notification_sent': True})


@celery.periodic_task(name='roombooking_occurrences', run_every=crontab(minute='15', hour='8'))
def roombooking_occurrences(debug=False):
    if not config.ENABLE_ROOMBOOKING:
        logger.info('Notifications not sent because room booking is disabled')
        return
    if not rb_settings.get('notifications_enabled'):
        logger.info('Notifications not sent because they are globally disabled')
        return

    occurrences = (ReservationOccurrence.query
                   .join(ReservationOccurrence.reservation)
                   .join(Reservation.room)
                   .filter(Room.is_active,
                           Room.notifications_enabled,
                           Reservation.is_accepted,
                           Reservation.booked_for_id.isnot(None),
                           ReservationOccurrence.is_valid,
                           ReservationOccurrence.start_dt >= datetime.now(),
                           ~ReservationOccurrence.notification_sent,
                           _make_occurrence_date_filter())
                   .order_by(Reservation.booked_for_id, ReservationOccurrence.start_dt, Room.id)
                   .options(contains_eager('reservation').contains_eager('room'))
                   .all())

    for user, user_occurrences in groupby(occurrences, key=attrgetter('reservation.booked_for_user')):
        user_occurrences = list(user_occurrences)
        if debug:
            _print_occurrences(user, user_occurrences)
        else:
            _notify_occurrences(user, user_occurrences)
    if not debug:
        db.session.commit()
