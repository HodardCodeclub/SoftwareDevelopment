

from __future__ import unicode_literals

from wtforms.fields.core import BooleanField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import NumberRange

from fossir.modules.api import APIMode
from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.fields import fossirEnumSelectField
from fossir.web.forms.widgets import SwitchWidget


security_mode_titles = {
    APIMode.KEY: _("Key for authenticated requests only"),
    APIMode.ONLYKEY: _("Key for all requests"),
    APIMode.SIGNED: _("Key+signature for authenticated requests only"),
    APIMode.ONLYKEY_SIGNED: _("Key for all requests. Signature for authenticated requests"),
    APIMode.ALL_SIGNED: _("Key+signature for all requests")
}


class AdminSettingsForm(fossirForm):
    allow_persistent = BooleanField(_('Persistent signatures'), widget=SwitchWidget(),
                                    description=_("Allow users to enable persistent signatures (without timestamp)."))
    security_mode = fossirEnumSelectField(_('Security mode'), enum=APIMode, titles=security_mode_titles,
                                          description=_('Specify if/when people need to use an API key or a '
                                                        'signed request.'))
    cache_ttl = IntegerField(_('Cache TTL'), [NumberRange(min=0)],
                             description=_('Time to cache API results (in seconds)'))
    signature_ttl = IntegerField(_('Signature TTL'), [NumberRange(min=1)],
                                 description=_('Time after which a request signature expires. This should not be too '
                                               'low to account for small clock differences between the client and the '
                                               'server.'))
