

from __future__ import unicode_literals

from fossir.modules.events.reminders.controllers import (RHAddReminder, RHDeleteReminder, RHEditReminder,
                                                         RHListReminders, RHPreviewReminder)
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('event_reminders', __name__, template_folder='templates',
                      virtual_template_folder='events/reminders', url_prefix='/event/<confId>/manage/reminders')

_bp.add_url_rule('/', 'list', RHListReminders)
_bp.add_url_rule('/add', 'add', RHAddReminder, methods=('GET', 'POST'))
_bp.add_url_rule('/preview', 'preview', RHPreviewReminder, methods=('POST',))
_bp.add_url_rule('/<int:reminder_id>/', 'edit', RHEditReminder, methods=('GET', 'POST'))
_bp.add_url_rule('/<int:reminder_id>/delete', 'delete', RHDeleteReminder, methods=('POST',))
