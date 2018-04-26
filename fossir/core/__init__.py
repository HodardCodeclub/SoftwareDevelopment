

from __future__ import unicode_literals

from fossir.core import signals
from fossir.util.i18n import _
from fossir.web.menu import TopMenuItem, TopMenuSection
from fossir.web.util import url_for_index


@signals.menu.sections.connect_via('top-menu')
def _topmenu_sections(sender, **kwargs):
    yield TopMenuSection('services', _('Services'), 60)
    yield TopMenuSection('help', _('Help'), -10)  # put the help section always last


@signals.menu.items.connect_via('top-menu')
def _topmenu_items(sender, **kwargs):
    yield TopMenuItem('home', _('Home'), url_for_index(), 100)
