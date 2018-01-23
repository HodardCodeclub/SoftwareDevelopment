

from __future__ import unicode_literals

from flask import render_template, session

from fossir.core import signals
from fossir.core.settings import SettingsProxy
from fossir.util.i18n import _
from fossir.web.flask.templating import template_hook
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


_DEFAULT_RESTRICTED_DISCLAIMER = ("Circulation to people other than the intended audience is not authorized. "
                                  "You are obliged to treat the information with the appropriate level of "
                                  "confidentiality.")
_DEFAULT_PROTECTED_DISCLAIMER = ("As such, this information is intended for an internal audience only. "
                                 "You are obliged to treat the information with the appropriate level of "
                                 "confidentiality.")


legal_settings = SettingsProxy('legal', {
    'network_protected_disclaimer': _DEFAULT_PROTECTED_DISCLAIMER,
    'restricted_disclaimer': _DEFAULT_RESTRICTED_DISCLAIMER,
    'tos': ''
})


@signals.menu.items.connect_via('admin-sidemenu')
def _sidemenu_items(sender, **kwargs):
    if session.user.is_admin:
        yield SideMenuItem('legal_messages', _('Legal/Disclaimers'), url_for('legal.manage'), section='security')


@template_hook('page-footer')
def _inject_footer(**kwargs):
    if legal_settings.get('tos'):
        return render_template('legal/tos_footer.html')
