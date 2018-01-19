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

from platform import python_version

from flask import flash, redirect, render_template, request, session
from markupsafe import Markup
from requests.exceptions import HTTPError, RequestException, Timeout

import fossir
from fossir.core.config import config
from fossir.core.db import db
from fossir.core.db.sqlalchemy.util.queries import get_postgres_version
from fossir.modules.auth import Identity, login_user
from fossir.modules.bootstrap.forms import BootstrapForm
from fossir.modules.cephalopod.util import register_instance
from fossir.modules.core.settings import core_settings
from fossir.modules.users import User
from fossir.util.i18n import _, get_all_locales
from fossir.util.string import to_unicode
from fossir.util.system import get_os
from fossir.web.flask.templating import get_template_module
from fossir.web.flask.util import url_for
from fossir.web.rh import RH
from fossir.web.util import url_for_index


class RHBootstrap(RH):
    def _process_GET(self):
        if User.query.filter_by(is_system=False).has_rows():
            return redirect(url_for_index())
        return render_template('bootstrap/bootstrap.html',
                               form=BootstrapForm(),
                               timezone=config.DEFAULT_TIMEZONE,
                               languages=get_all_locales(),
                               operating_system=get_os(),
                               postgres_version=get_postgres_version(),
                               fossir_version=fossir.__version__,
                               python_version=python_version())

    def _process_POST(self):
        if User.query.filter_by(is_system=False).has_rows():
            return redirect(url_for_index())
        setup_form = BootstrapForm(request.form)
        if not setup_form.validate():
            flash(_("Some fields are invalid. Please, correct them and submit the form again."), 'error')
            return redirect(url_for('bootstrap.index'))

        # Creating new user
        user = User()
        user.first_name = to_unicode(setup_form.first_name.data)
        user.last_name = to_unicode(setup_form.last_name.data)
        user.affiliation = to_unicode(setup_form.affiliation.data)
        user.email = to_unicode(setup_form.email.data)
        user.is_admin = True

        identity = Identity(provider='fossir', identifier=setup_form.username.data, password=setup_form.password.data)
        user.identities.add(identity)

        db.session.add(user)
        db.session.flush()

        user.settings.set('timezone', config.DEFAULT_TIMEZONE)
        user.settings.set('lang', session.lang or config.DEFAULT_LOCALE)

        login_user(user, identity)
        full_name = user.full_name  # needed after the session closes

        db.session.commit()

        # Configuring server's settings
        core_settings.set('site_organization', setup_form.affiliation.data)

        message = get_template_module('bootstrap/flash_messages.html').bootstrap_success(name=full_name)
        flash(Markup(message), 'success')

        # Activate instance tracking
        if setup_form.enable_tracking.data:
            contact_name = setup_form.contact_name.data
            contact_email = setup_form.contact_email.data

            try:
                register_instance(contact_name, contact_email)
            except (HTTPError, ValueError) as err:
                message = get_template_module('bootstrap/flash_messages.html').community_error(err=err)
                category = 'error'
            except Timeout:
                message = get_template_module('bootstrap/flash_messages.html').community_timeout()
                category = 'error'
            except RequestException as exc:
                message = get_template_module('bootstrap/flash_messages.html').community_exception(exc=exc)
                category = 'error'
            else:
                message = get_template_module('bootstrap/flash_messages.html').community_success()
                category = 'success'
            flash(Markup(message), category)

        return redirect(url_for_index())