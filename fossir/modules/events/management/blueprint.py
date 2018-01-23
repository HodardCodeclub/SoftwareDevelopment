

from __future__ import unicode_literals

from fossir.modules.events import event_management_object_url_prefixes
from fossir.modules.events.management.controllers import actions, cloning, posters, protection, settings
from fossir.web.flask.util import make_compat_redirect_func
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('event_management', __name__, template_folder='templates',
                      virtual_template_folder='events/management',
                      url_prefix='/event/<confId>/manage')

# Settings
_bp.add_url_rule('/', 'settings', settings.RHEventSettings)
_bp.add_url_rule('/settings/data', 'edit_data', settings.RHEditEventData, methods=('GET', 'POST'))
_bp.add_url_rule('/settings/dates', 'edit_dates', settings.RHEditEventDates, methods=('GET', 'POST'))
_bp.add_url_rule('/settings/location', 'edit_location', settings.RHEditEventLocation, methods=('GET', 'POST'))
_bp.add_url_rule('/settings/persons', 'edit_persons', settings.RHEditEventPersons, methods=('GET', 'POST'))
_bp.add_url_rule('/settings/contact-info', 'edit_contact_info', settings.RHEditEventContactInfo,
                 methods=('GET', 'POST'))
_bp.add_url_rule('/settings/classification', 'edit_classification', settings.RHEditEventClassification,
                 methods=('GET', 'POST'))
# Actions
_bp.add_url_rule('/delete', 'delete', actions.RHDeleteEvent, methods=('GET', 'POST'))
_bp.add_url_rule('/change-type', 'change_type', actions.RHChangeEventType, methods=('POST',))
_bp.add_url_rule('/lock', 'lock', actions.RHLockEvent, methods=('GET', 'POST'))
_bp.add_url_rule('/unlock', 'unlock', actions.RHUnlockEvent, methods=('POST',))
_bp.add_url_rule('/move', 'move', actions.RHMoveEvent, methods=('POST',))
# Protection
_bp.add_url_rule('/protection', 'protection', protection.RHEventProtection, methods=('GET', 'POST'))
_bp.add_url_rule('/protection/acl', 'acl', protection.RHEventACL)
_bp.add_url_rule('/protection/acl-message', 'acl_message', protection.RHEventACLMessage)
# Cloning
_bp.add_url_rule('/clone', 'clone', cloning.RHCloneEvent, methods=('GET', 'POST'))
_bp.add_url_rule('/clone/preview', 'clone_preview', cloning.RHClonePreview, methods=('GET', 'POST'))
# Posters
_bp.add_url_rule('/print-poster/settings', 'poster_settings', posters.RHPosterPrintSettings, methods=('GET', 'POST'))
_bp.add_url_rule('/print-poster/<int:template_id>/<uuid>', 'print_poster', posters.RHPrintEventPoster)


for object_type, prefixes in event_management_object_url_prefixes.iteritems():
    if object_type == 'subcontribution':
        continue
    for prefix in prefixes:
        prefix = '!/event/<confId>' + prefix
        _bp.add_url_rule(prefix + '/show-non-inheriting', 'show_non_inheriting', protection.RHShowNonInheriting,
                         defaults={'object_type': object_type})


_compat_bp = fossirBlueprint('compat_event_management', __name__, url_prefix='/event/<confId>/manage')
_compat_bp.add_url_rule('/general/', 'settings', make_compat_redirect_func(_bp, 'settings'))
