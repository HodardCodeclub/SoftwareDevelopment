
from __future__ import unicode_literals

from fossir.modules.events.layout.compat import compat_image, compat_page
from fossir.modules.events.layout.controllers.images import RHImageDelete, RHImageDisplay, RHImages, RHImageUpload
from fossir.modules.events.layout.controllers.layout import (RHLayoutCSSDelete, RHLayoutCSSDisplay, RHLayoutCSSPreview,
                                                             RHLayoutCSSSaveTheme, RHLayoutCSSUpload, RHLayoutEdit,
                                                             RHLayoutLogoDelete, RHLayoutLogoUpload,
                                                             RHLayoutTimetableThemeForm, RHLogoDisplay)
from fossir.modules.events.layout.controllers.menu import (RHMenuAddEntry, RHMenuDeleteEntry, RHMenuEdit,
                                                           RHMenuEntryEdit, RHMenuEntryPosition,
                                                           RHMenuEntryToggleDefault, RHMenuEntryToggleEnabled,
                                                           RHMenuToggleCustom, RHPageDisplay)
from fossir.web.flask.util import make_compat_redirect_func
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('event_layout', __name__, template_folder='templates',
                      virtual_template_folder='events/layout', url_prefix='/event/<confId>/manage/layout')

_bp.add_url_rule('/', 'index', RHLayoutEdit, methods=('GET', 'POST'))
_bp.add_url_rule('/timetable-theme-form', 'timetable_theme_form', RHLayoutTimetableThemeForm)
_bp.add_url_rule('/menu/', 'menu', RHMenuEdit)
_bp.add_url_rule('/menu/toggle-customize', 'menu_toggle_custom', RHMenuToggleCustom, methods=('POST',))
_bp.add_url_rule('/menu/<int:menu_entry_id>/', 'menu_entry_edit', RHMenuEntryEdit, methods=('GET', 'POST',))
_bp.add_url_rule('/menu/<int:menu_entry_id>/position', 'menu_entry_position', RHMenuEntryPosition, methods=('POST',))
_bp.add_url_rule('/menu/<int:menu_entry_id>/toggle-enabled', 'menu_entry_toggle_enabled', RHMenuEntryToggleEnabled,
                 methods=('POST',))
_bp.add_url_rule('/menu/<int:menu_entry_id>/toggle-default', 'menu_entry_toggle_default', RHMenuEntryToggleDefault,
                 methods=('POST',))
_bp.add_url_rule('/menu/<int:menu_entry_id>/delete', 'menu_delete_entry', RHMenuDeleteEntry, methods=('DELETE',))
_bp.add_url_rule('/menu/add', 'menu_add_entry', RHMenuAddEntry, methods=('GET', 'POST'))
_bp.add_url_rule('/theme/save', 'css_save_theme', RHLayoutCSSSaveTheme, methods=('POST',))
_bp.add_url_rule('/theme/preview', 'css_preview', RHLayoutCSSPreview)
_bp.add_url_rule('/css', 'upload_css', RHLayoutCSSUpload, methods=('POST',))
_bp.add_url_rule('/css', 'delete_css', RHLayoutCSSDelete, methods=('DELETE',))
_bp.add_url_rule('/logo', 'upload_logo', RHLayoutLogoUpload, methods=('POST',))
_bp.add_url_rule('/logo', 'delete_logo', RHLayoutLogoDelete, methods=('DELETE',))
_bp.add_url_rule('/images/', 'images', RHImages)
_bp.add_url_rule('/images/upload', 'images_upload', RHImageUpload, methods=('POST',))
_bp.add_url_rule('/images/<int:image_id>-<filename>', 'image_delete', RHImageDelete, methods=('DELETE',))
_bp.add_url_rule('!/event/<confId>/<slug>.css', 'css_display', RHLayoutCSSDisplay)


_bp_images = fossirBlueprint('event_images', __name__, template_folder='templates',
                             virtual_template_folder='events/layout', url_prefix='/event/<confId>')
_bp_images.add_url_rule('/logo-<slug>.png', 'logo_display', RHLogoDisplay)
_bp_images.add_url_rule('/images/<int:image_id>-<filename>', 'image_display', RHImageDisplay)


_bp_pages = fossirBlueprint('event_pages', __name__, template_folder='templates',
                            virtual_template_folder='events/layout', url_prefix='/event/<confId>')
_bp_pages.add_url_rule('/page/<int:page_id>-<slug>', 'page_display', RHPageDisplay)

_compat_bp = fossirBlueprint('compat_layout', __name__, url_prefix='/event/<event_id>')
_compat_bp.add_url_rule('!/internalPage.py', 'page_modpython',
                        make_compat_redirect_func(_compat_bp, 'page', view_args_conv={'confId': 'event_id',
                                                                                      'pageId': 'legacy_page_id'}))
_compat_bp.add_url_rule('/page/<int:legacy_page_id>', 'page', compat_page)
_compat_bp.add_url_rule('/picture/<int:legacy_image_id>.<image_ext>', 'image', compat_image)
_compat_bp.add_url_rule('/picture/<int:legacy_image_id>', 'image', compat_image)
_compat_bp.add_url_rule('!/conferenceDisplay.py/getPic', 'image_modpython',
                        make_compat_redirect_func(_compat_bp, 'image', view_args_conv={'confId': 'event_id',
                                                                                       'picId': 'legacy_image_id'}))
