

from __future__ import unicode_literals

from wtforms.fields import StringField
from wtforms.validators import DataRequired

from fossir.core.db.sqlalchemy.descriptions import RenderMode
from fossir.util.i18n import _
from fossir.web.forms.base import fossirForm, generated_data
from fossir.web.forms.fields import fossirMarkdownField


class TrackForm(fossirForm):
    title = StringField(_('Title'), [DataRequired()])
    code = StringField(_('Code'))
    description = fossirMarkdownField(_('Description'), editor=True)


class ProgramForm(fossirForm):
    program = fossirMarkdownField(_('Programme'), editor=True, mathjax=True)

    @generated_data
    def program_render_mode(self):
        return RenderMode.markdown
