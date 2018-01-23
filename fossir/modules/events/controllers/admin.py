.

from __future__ import unicode_literals

from flask import flash, request

from fossir.core.db import db
from fossir.modules.admin import RHAdminBase
from fossir.modules.events.forms import ReferenceTypeForm
from fossir.modules.events.models.references import ReferenceType
from fossir.modules.events.operations import create_reference_type, delete_reference_type, update_reference_type
from fossir.modules.events.views import WPReferenceTypes
from fossir.util.i18n import _
from fossir.web.flask.templating import get_template_module
from fossir.web.forms.base import FormDefaults
from fossir.web.util import jsonify_data, jsonify_form


def _get_all_reference_types():
    return ReferenceType.query.order_by(db.func.lower(ReferenceType.name)).all()


def _render_reference_type_list():
    tpl = get_template_module('events/admin/_reference_type_list.html')
    return tpl.render_reference_type_list(_get_all_reference_types())


class RHManageReferenceTypeBase(RHAdminBase):
    """Base class for a specific reference type"""

    def _process_args(self):
        RHAdminBase._process_args(self)
        self.reference_type = ReferenceType.find_one(id=request.view_args['reference_type_id'])


class RHReferenceTypes(RHAdminBase):
    """Manage reference types in server admin area"""

    def _process(self):
        types = _get_all_reference_types()
        return WPReferenceTypes.render_template('admin/reference_types.html', 'reference_types', reference_types=types)


class RHCreateReferenceType(RHAdminBase):
    """Create a new reference type"""

    def _process(self):
        form = ReferenceTypeForm()
        if form.validate_on_submit():
            reference_type = create_reference_type(form.data)
            flash(_("External ID type '{}' created successfully").format(reference_type.name), 'success')
            return jsonify_data(html=_render_reference_type_list())
        return jsonify_form(form)


class RHEditReferenceType(RHManageReferenceTypeBase):
    """Edit an existing reference type"""

    def _process(self):
        form = ReferenceTypeForm(obj=FormDefaults(self.reference_type), reference_type=self.reference_type)
        if form.validate_on_submit():
            update_reference_type(self.reference_type, form.data)
            flash(_("External ID type '{}' successfully updated").format(self.reference_type.name), 'success')
            return jsonify_data(html=_render_reference_type_list())
        return jsonify_form(form)


class RHDeleteReferenceType(RHManageReferenceTypeBase):
    """Delete an existing reference type"""

    def _process_DELETE(self):
        delete_reference_type(self.reference_type)
        flash(_("External ID type '{}' successfully deleted").format(self.reference_type.name), 'success')
        return jsonify_data(html=_render_reference_type_list())
