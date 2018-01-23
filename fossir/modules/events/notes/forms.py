

from __future__ import unicode_literals

from wtforms.fields import TextAreaField

from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm
from fossir.web.forms.widgets import CKEditorWidget


class NoteForm(fossirForm):
    # TODO: use something switchable
    source = TextAreaField(_("Minutes"), widget=CKEditorWidget())
