

from __future__ import unicode_literals

from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.fields import BooleanField, TextAreaField
from wtforms.fields.html5 import URLField
from wtforms.fields.simple import HiddenField, StringField
from wtforms.validators import DataRequired, Optional

from fossir.core.db import db
from fossir.core.db.sqlalchemy.protection import ProtectionMode
from fossir.modules.attachments.models.folders import AttachmentFolder
from fossir.modules.attachments.util import get_default_folder_names
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.forms.base import fossirForm, generated_data
from fossir.web.forms.fields import (AccessControlListField, EditableFileField, FileField, fossirDateField,
                                     fossirRadioField, fossirSelectMultipleCheckboxField)
from fossir.web.forms.validators import HiddenUnless, UsedIf
from fossir.web.forms.widgets import SwitchWidget, TypeaheadWidget


class AttachmentFormBase(fossirForm):
    protected = BooleanField(_("Protected"), widget=SwitchWidget())
    folder = QuerySelectField(_("Folder"), allow_blank=True, blank_text=_("No folder selected"), get_label='title',
                              description=_("Adding materials to folders allow grouping and easier permission "
                                            "management."))
    acl = AccessControlListField(_("Access control list"), [UsedIf(lambda form, field: form.protected.data)],
                                 groups=True, allow_external=True, default_text=_('Restrict access to this material'),
                                 description=_("The list of users and groups allowed to access the material"))

    def __init__(self, *args, **kwargs):
        linked_object = kwargs.pop('linked_object')
        super(AttachmentFormBase, self).__init__(*args, **kwargs)
        self.folder.query = (AttachmentFolder
                             .find(object=linked_object, is_default=False, is_deleted=False)
                             .order_by(db.func.lower(AttachmentFolder.title)))

    @generated_data
    def protection_mode(self):
        return ProtectionMode.protected if self.protected.data else ProtectionMode.inheriting


class EditAttachmentFormBase(AttachmentFormBase):
    title = StringField(_("Title"), [DataRequired()])
    description = TextAreaField(_("Description"))


class AddAttachmentFilesForm(AttachmentFormBase):
    files = FileField(_("Files"), multiple_files=True)


def _get_file_data(attachment):
    file = attachment.file
    return {
        'url': url_for('attachments.download', attachment, filename=file.filename, from_preview='1'),
        'filename': file.filename,
        'size': file.size,
        'content_type': file.content_type
    }


class EditAttachmentFileForm(EditAttachmentFormBase):
    file = EditableFileField(_("File"), add_remove_links=False, get_metadata=_get_file_data,
                             description=_("Already uploaded file. Replace it by adding a new file."))


class AttachmentLinkFormMixin(object):
    title = StringField(_("Title"), [DataRequired()])
    link_url = URLField(_("URL"), [DataRequired()])


class AddAttachmentLinkForm(AttachmentLinkFormMixin, AttachmentFormBase):
    pass


class EditAttachmentLinkForm(AttachmentLinkFormMixin, EditAttachmentFormBase):
    pass


class AttachmentFolderForm(fossirForm):
    title = HiddenField(_("Name"), [DataRequired()], widget=TypeaheadWidget(),
                        description=_("The name of the folder."))
    description = TextAreaField(_("Description"), description=_("Description of the folder and its content"))
    protected = BooleanField(_("Protected"), widget=SwitchWidget())
    acl = AccessControlListField(_("Access control list"), [UsedIf(lambda form, field: form.protected.data)],
                                 groups=True, allow_external=True, default_text=_('Restrict access to this folder'),
                                 description=_("The list of users and groups allowed to access the folder"))
    is_always_visible = BooleanField(_("Always Visible"), widget=SwitchWidget(),
                                     description=_("By default, folders are always visible, even if a user cannot "
                                                   "access them. You can disable this behavior here, hiding the folder "
                                                   "for anyone who does not have permission to access it."))

    def __init__(self, *args, **kwargs):
        self.linked_object = kwargs.pop('linked_object')
        super(AttachmentFolderForm, self).__init__(*args, **kwargs)
        self.title.choices = self._get_title_suggestions()

    def _get_title_suggestions(self):
        query = db.session.query(AttachmentFolder.title).filter_by(is_deleted=False, is_default=False,
                                                                   object=self.linked_object)
        existing = set(x[0] for x in query)
        suggestions = set(get_default_folder_names()) - existing
        if self.title.data:
            suggestions.add(self.title.data)
        return sorted(suggestions)

    @generated_data
    def protection_mode(self):
        return ProtectionMode.protected if self.protected.data else ProtectionMode.inheriting


class AttachmentPackageForm(fossirForm):
    added_since = fossirDateField(_('Added Since'), [Optional()],
                                  description=_('Include only attachments uploaded after this date'))

    filter_type = fossirRadioField(_('Include'), [DataRequired()])

    sessions = fossirSelectMultipleCheckboxField(_('Sessions'), [HiddenUnless('filter_type', 'sessions'),
                                                                 DataRequired()],
                                                 description=_('Include materials from selected sessions'),
                                                 coerce=int)
    contributions = fossirSelectMultipleCheckboxField(_('Contributions'),
                                                      [HiddenUnless('filter_type', 'contributions'), DataRequired()],
                                                      description=_('Include materials from selected contributions'),
                                                      coerce=int)
    dates = fossirSelectMultipleCheckboxField(_('Events scheduled on'), [HiddenUnless('filter_type', 'dates'),
                                                                         DataRequired()],
                                              description=_('Include materials from sessions/contributions scheduled '
                                                            'on the selected dates'))
