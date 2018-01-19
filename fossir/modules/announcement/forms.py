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

from wtforms.fields import BooleanField, TextAreaField
from wtforms.validators import DataRequired

from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.validators import UsedIf
from fossir.web.forms.widgets import SwitchWidget


class AnnouncementForm(fossirForm):
    enabled = BooleanField(_('Enabled'), widget=SwitchWidget())
    message = TextAreaField(_('Message'), [UsedIf(lambda form, _: form.enabled.data), DataRequired()])