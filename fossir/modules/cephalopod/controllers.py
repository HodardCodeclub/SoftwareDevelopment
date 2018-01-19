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

import platform

from flask import flash, jsonify, redirect
from requests.exceptions import HTTPError, RequestException, Timeout
from werkzeug.urls import url_join

import fossir
from fossir.core.config import config
from fossir.core.db.sqlalchemy.util.queries import get_postgres_version
from fossir.modules.admin import RHAdminBase
from fossir.modules.cephalopod import cephalopod_settings
from fossir.modules.cephalopod.forms import CephalopodForm
from fossir.modules.cephalopod.util import register_instance, sync_instance, unregister_instance
from fossir.modules.cephalopod.views import WPCephalopod
from fossir.modules.core.settings import core_settings
from fossir.util.i18n import _
from fossir.util.system import get_os
from fossir.web.flask.util import url_for
from fossir.web.forms.base import FormDefaults
from fossir.web.rh import RH


class RHCephalopodBase(RHAdminBase):
    pass


class RHCephalopod(RHCephalopodBase):
    def _process(self):
        form = CephalopodForm(obj=FormDefaults(**cephalopod_settings.get_all()))
        if form.validate_on_submit():
            return self._process_form(form)
        hub_url = url_join(config.COMMUNITY_HUB_URL, 'api/instance/{}'.format(cephalopod_settings.get('uuid')))
        cephalopod_settings.set('show_migration_message', False)
        return WPCephalopod.render_template('cephalopod.html', 'cephalopod',
                                            affiliation=core_settings.get('site_organization'),
                                            enabled=cephalopod_settings.get('joined'),
                                            form=form,
                                            fossir_version=fossir.__version__,
                                            instance_url=config.BASE_URL,
                                            language=config.DEFAULT_LOCALE,
                                            operating_system=get_os(),
                                            postgres_version=get_postgres_version(),
                                            python_version=platform.python_version(),
                                            hub_url=hub_url)

    def _process_form(self, form):
        name = form.contact_name.data
        email = form.contact_email.data
        enabled = form.joined.data
        uuid = cephalopod_settings.get('uuid')
        try:
            if not enabled:
                unregister_instance()
            elif enabled and uuid:
                sync_instance(name, email)
            elif enabled and not uuid:
                register_instance(name, email)
        except HTTPError as err:
            flash(_("Operation failed, the community hub returned: {err.message}").format(err=err), 'error')
        except Timeout:
            flash(_("The operation timed-out. Please try again in a while."), 'error')
        except RequestException as err:
            flash(_("Unexpected exception while contacting the Community Hub: {err.message}").format(err=err))

        return redirect(url_for('.index'))


class RHCephalopodSync(RHCephalopodBase):
    def _process(self):
        if not cephalopod_settings.get('joined'):
            flash(_("Synchronization is not possible if you don't join the community first."),
                  'error')
        else:
            contact_name = cephalopod_settings.get('contact_name')
            contact_email = cephalopod_settings.get('contact_email')
            try:
                sync_instance(contact_name, contact_email)
            except HTTPError as err:
                flash(_("Synchronization failed, the community hub returned: {err.message}").format(err=err),
                      'error')
            except Timeout:
                flash(_("Synchronization timed-out. Please try again in a while."), 'error')
            except RequestException as err:
                flash(_("Unexpected exception while contacting the Community Hub: {err.message}").format(err=err))

            return redirect(url_for('.index'))


class RHSystemInfo(RH):
    def _process(self):
        stats = {'python_version': platform.python_version(),
                 'fossir_version': fossir.__version__,
                 'operating_system': get_os(),
                 'postgres_version': get_postgres_version(),
                 'language': config.DEFAULT_LOCALE,
                 'debug': config.DEBUG}
        return jsonify(stats)
