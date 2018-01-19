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

from wtforms import BooleanField, StringField
from wtforms.validators import DataRequired

from fossir.modules.designer.models.templates import TemplateType
from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.fields import fossirEnumSelectField
from fossir.web.forms.widgets import SwitchWidget


class AddTemplateForm(fossirForm):
    title = StringField(_('Title'), [DataRequired()])
    type = fossirEnumSelectField(_('Template'), enum=TemplateType, default=TemplateType.poster)
    is_clonable = BooleanField(_('Allow cloning'), widget=SwitchWidget(), default=True,
                               description=_("Allow cloning this template in subcategories and events"))
