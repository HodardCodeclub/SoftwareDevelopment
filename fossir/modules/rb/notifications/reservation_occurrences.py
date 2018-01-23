

from fossir.core.notifications import email_sender, make_email
from fossir.modules.rb.notifications.reservations import ReservationNotification
from fossir.util.date_time import format_datetime
from fossir.web.flask.templating import get_template_module


class ReservationOccurrenceNotification(ReservationNotification):
    def __init__(self, occurrence):
        super(ReservationOccurrenceNotification, self).__init__(occurrence.reservation)
        self.occurrence = occurrence
        self.start_dt = format_datetime(occurrence.start_dt)

    def _get_email_subject(self, **mail_params):
        mail_params = dict(mail_params, **{'subject_suffix': '(SINGLE OCCURRENCE)'})
        return super(ReservationOccurrenceNotification, self)._get_email_subject(**mail_params)

    def _make_body(self, mail_params, **body_params):
        body_params['occurrence'] = self.occurrence
        return super(ReservationOccurrenceNotification, self)._make_body(mail_params, **body_params)


@email_sender
def notify_cancellation(occurrence):
    if not occurrence.is_cancelled:
        raise ValueError('Occurrence is not cancelled')
    notification = ReservationOccurrenceNotification(occurrence)
    return filter(None, [
        notification.compose_email_to_user(
            subject='Booking cancelled on',
            template_name='occurrence_cancellation_email_to_user'
        ),
        notification.compose_email_to_manager(
            subject='Booking cancelled on',
            template_name='occurrence_cancellation_email_to_manager'
        ),
        notification.compose_email_to_vc_support(
            subject='Booking cancelled on',
            template_name='occurrence_cancellation_email_to_vc_support'
        ),
        notification.compose_email_to_assistance(
            subject_prefix='[Support Request Cancellation]',
            subject='Request cancelled for',
            template_name='occurrence_cancellation_email_to_assistance'
        )
    ])


@email_sender
def notify_rejection(occurrence):
    if not occurrence.is_rejected:
        raise ValueError('Occurrence is not rejected')
    notification = ReservationOccurrenceNotification(occurrence)
    return filter(None, [
        notification.compose_email_to_user(
            subject='Booking rejected on',
            template_name='occurrence_rejection_email_to_user'
        ),
        notification.compose_email_to_manager(
            subject='Booking rejected on',
            template_name='occurrence_rejection_email_to_manager'
        ),
        notification.compose_email_to_assistance(
            subject_prefix='[Support Request Cancellation]',
            subject='Request cancelled for',
            template_name='occurrence_rejection_email_to_assistance'
        )
    ])


@email_sender
def notify_upcoming_occurrences(user, occurrences):
    tpl = get_template_module('rb/emails/reservations/reminders/upcoming_occurrence.html',
                              occurrences=occurrences, user=user)
    return make_email(to_list={user.email}, template=tpl, html=True)
