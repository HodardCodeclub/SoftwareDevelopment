
from __future__ import unicode_literals

from flask import session

from fossir.core import signals
from fossir.util.i18n import _
from fossir.util.placeholders import Placeholder
from fossir.util.struct.enum import RichIntEnum
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


class TemplateType(RichIntEnum):
    __titles__ = [None, _("Badge"), _("Poster")]
    badge = 1
    poster = 2


class PageOrientation(RichIntEnum):
    __titles__ = [None, _('Landscape'), _('Portrait')]
    landscape = 1
    portrait = 2


class PageSize(RichIntEnum):
    __titles__ = [None, 'A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'Letter']
    A0 = 1
    A1 = 2
    A2 = 3
    A3 = 4
    A4 = 5
    A5 = 6
    letter = 7


class PageLayout(RichIntEnum):
    __titles__ = [None, _("Single sided (foldable)"), _("Double sided"), _("Only front side")]
    foldable = 1
    double_sided = 2
    front_only = 3


DEFAULT_CONFIG = {
    TemplateType.poster: {
        'tpl_size': [1050, 1484],  # A4 50 px/cm
        'zoom_factor': 0.5,
        'disallow_groups': ('registrant',)
    },
    TemplateType.badge: {
        'tpl_size': [425, 270],  # A4 50 px/cm
        'zoom_factor': 1
    }
}


@signals.get_placeholders.connect_via('designer-fields')
def _get_notification_placeholders(sender, **kwargs):
    from fossir.modules.designer import placeholders
    for name in placeholders.__all__:
        obj = getattr(placeholders, name)
        if isinstance(obj, type) and issubclass(obj, Placeholder) and hasattr(obj, 'name'):
            yield obj


@signals.menu.items.connect_via('event-management-sidemenu')
def _event_sidemenu_items(sender, event, **kwargs):
    if event.can_manage(session.user):
        return SideMenuItem('designer', _('Posters/Badges'), url_for('designer.template_list', event),
                            section='customization')


@signals.menu.items.connect_via('category-management-sidemenu')
def _category_sidemenu_items(sender, category, **kwargs):
    if category.can_manage(session.user):
        return SideMenuItem('designer', _('Posters/Badges'), url_for('designer.template_list', category),
                            icon='palette')
