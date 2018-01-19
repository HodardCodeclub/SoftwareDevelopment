# This file is part of fossir.
# Copyright (C) 2002 - 2017 European Organization for Nuclear Research (CERN).
#
# fossir is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# fossir is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fossir; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from io import BytesIO

import qrcode
from flask import json, render_template
from werkzeug.exceptions import Forbidden, NotFound

from fossir.core.config import config
from fossir.core.db import db
from fossir.modules.designer import PageOrientation, PageSize
from fossir.modules.events.registration.controllers.display import RHRegistrationFormRegistrationBase
from fossir.modules.events.registration.controllers.management import RHManageRegFormBase
from fossir.modules.events.registration.forms import TicketsForm
from fossir.modules.events.registration.models.registrations import RegistrationState
from fossir.modules.events.registration.util import generate_ticket
from fossir.modules.oauth.models.applications import OAuthApplication, SystemAppType
from fossir.web.flask.util import secure_filename, send_file, url_for
from fossir.web.util import jsonify_data, jsonify_template


DEFAULT_TICKET_PRINTING_SETTINGS = {
    'top_margin': 0,
    'bottom_margin': 0,
    'left_margin': 0,
    'right_margin': 0,
    'margin_columns': 0,
    'margin_rows': 0.0,
    'page_size': PageSize.A4,
    'page_orientation': PageOrientation.portrait,
    'dashed_border': False,
    'page_layout': None
}


class RHRegistrationFormTickets(RHManageRegFormBase):
    """Display and modify ticket settings."""

    def _process(self):
        form = TicketsForm(obj=self.regform, event=self.event)
        if form.validate_on_submit():
            form.populate_obj(self.regform)
            db.session.flush()
            return jsonify_data(flash=False, tickets_enabled=self.regform.tickets_enabled)

        return jsonify_template('events/registration/management/regform_tickets.html', regform=self.regform, form=form)


class RHTicketDownload(RHRegistrationFormRegistrationBase):
    """Generate ticket for a given registration"""

    def _process_args(self):
        RHRegistrationFormRegistrationBase._process_args(self)
        if not self.registration:
            raise NotFound

    def _check_access(self):
        RHRegistrationFormRegistrationBase._check_access(self)
        if self.registration.state != RegistrationState.complete:
            raise Forbidden
        if not self.regform.tickets_enabled:
            raise Forbidden
        if not self.regform.ticket_on_event_page and not self.regform.ticket_on_summary_page:
            raise Forbidden
        if self.registration.is_ticket_blocked:
            raise Forbidden

    def _process(self):
        filename = secure_filename('{}-Ticket.pdf'.format(self.event.title), 'ticket.pdf')
        return send_file(filename, generate_ticket(self.registration), 'application/pdf')


class RHTicketConfigQRCodeImage(RHManageRegFormBase):
    """Display configuration QRCode."""

    def _process(self):
        # QRCode (Version 6 with error correction L can contain up to 106 bytes)
        qr = qrcode.QRCode(
            version=6,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=4,
            border=1
        )

        checkin_app = OAuthApplication.find_one(system_app_type=SystemAppType.checkin)
        qr_data = {
            "event_id": self.event.id,
            "title": self.event.title,
            "date": self.event.start_dt.isoformat(),
            "version": 1,
            "server": {
                "base_url": config.BASE_URL,
                "consumer_key": checkin_app.client_id,
                "auth_url": url_for('oauth.oauth_authorize', _external=True),
                "token_url": url_for('oauth.oauth_token', _external=True)
            }
        }
        json_qr_data = json.dumps(qr_data)
        qr.add_data(json_qr_data)
        qr.make(fit=True)
        qr_img = qr.make_image()

        output = BytesIO()
        qr_img.save(output)
        output.seek(0)

        return send_file('config.png', output, 'image/png')


class RHTicketConfigQRCode(RHManageRegFormBase):
    def _process(self):
        return render_template('events/registration/management/regform_qr_code.html', regform=self.regform)