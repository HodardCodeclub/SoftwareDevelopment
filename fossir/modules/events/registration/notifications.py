

from __future__ import unicode_literals

from flask import session

from fossir.core import signals
from fossir.core.notifications import make_email, send_email
from fossir.modules.events.registration.models.registrations import RegistrationState
from fossir.util.placeholders import replace_placeholders
from fossir.util.signals import values_from_signal
from fossir.web.flask.templating import get_template_module


def notify_invitation(invitation, email_subject, email_body, from_address):
    """Send a notification about a new registration invitation."""
    email_body = replace_placeholders('registration-invitation-email', email_body, invitation=invitation)
    email_subject = replace_placeholders('registration-invitation-email', email_subject, invitation=invitation)
    template = get_template_module('emails/custom.html', subject=email_subject, body=email_body)
    email = make_email(invitation.email, from_address=from_address, template=template, html=True)
    send_email(email, invitation.registration_form.event, 'Registration', session.user)


def _notify_registration(registration, template, to_managers=False):
    from fossir.modules.events.registration.util import get_ticket_attachments
    attachments = None
    regform = registration.registration_form
    tickets_handled = values_from_signal(signals.event.is_ticketing_handled.send(regform), single_value=True)
    if (not to_managers and
            regform.tickets_enabled and
            regform.ticket_on_email and
            not any(tickets_handled) and
            registration.state == RegistrationState.complete):
        attachments = get_ticket_attachments(registration)

    template = get_template_module('events/registration/emails/{}'.format(template), registration=registration)
    to_list = registration.email if not to_managers else registration.registration_form.manager_notification_recipients
    from_address = registration.registration_form.sender_address if not to_managers else None
    mail = make_email(to_list=to_list, template=template, html=True, from_address=from_address, attachments=attachments)
    send_email(mail, event=registration.registration_form.event, module='Registration', user=session.user)


def notify_registration_creation(registration, notify_user=True):
    if notify_user:
        _notify_registration(registration, 'registration_creation_to_registrant.html')
    if registration.registration_form.manager_notifications_enabled:
        _notify_registration(registration, 'registration_creation_to_managers.html', to_managers=True)


def notify_registration_modification(registration, notify_user=True):
    if notify_user:
        _notify_registration(registration, 'registration_modification_to_registrant.html')
    if registration.registration_form.manager_notifications_enabled:
        _notify_registration(registration, 'registration_modification_to_managers.html', to_managers=True)


def notify_registration_state_update(registration):
    _notify_registration(registration, 'registration_state_update_to_registrant.html')
    if registration.registration_form.manager_notifications_enabled:
        _notify_registration(registration, 'registration_state_update_to_managers.html', to_managers=True)
