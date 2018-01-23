

from __future__ import unicode_literals

from wtforms.fields import BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired

from fossir.core.db import db
from fossir.modules.networks.fields import MultiIPNetworkField
from fossir.modules.networks.models.networks import IPNetworkGroup
from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.widgets import SwitchWidget


attachment_access_override_warning = _('Do you really want to grant everyone within the specified networks '
                                       'unauthenticated access to all attachments/materials in fossir?')


class IPNetworkGroupForm(fossirForm):
    """Form to create or edit an IPNetworkGroup"""

    name = StringField(_("Name"), [DataRequired()])
    description = TextAreaField(_("Description"))
    networks = MultiIPNetworkField(_('Subnets'), description=_("IPv4 or IPv6 subnets in CIDR notation"))
    hidden = BooleanField(_('Hidden'), widget=SwitchWidget(),
                          description=_("Hidden IP networks cannot be added to ACLs by users"))
    attachment_access_override = BooleanField(_('Full attachment access'),
                                              widget=SwitchWidget(confirm_enable=attachment_access_override_warning),
                                              description=_("If enabled, these IPs have unrestricted access to all "
                                                            "attachments without having to be logged in."))

    def __init__(self, *args, **kwargs):
        self._network_group_id = kwargs['obj'].id if 'obj' in kwargs else None
        super(IPNetworkGroupForm, self).__init__(*args, **kwargs)

    def validate_name(self, field):
        query = IPNetworkGroup.find(db.func.lower(IPNetworkGroup.name) == field.data.lower())
        if self._network_group_id is not None:
            query = query.filter(IPNetworkGroup.id != self._network_group_id)
        if query.first():
            raise ValueError(_("An IP network with this name already exists."))
