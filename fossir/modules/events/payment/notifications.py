

from __future__ import unicode_literals

from flask import render_template

from fossir.core.notifications import email_sender, make_email


@email_sender
def notify_amount_inconsistency(registration, amount, currency):
    event = registration.registration_form.event
    to = event.creator.email
    body = render_template('events/payment/emails/payment_inconsistency_email_to_manager.txt',
                           event=event, registration=registration, amount=amount, currency=currency)
    return make_email(to, subject='Payment inconsistency', body=body)
