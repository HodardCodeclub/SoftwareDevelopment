

from __future__ import unicode_literals

from flask import session

from fossir.core import signals
from fossir.core.logger import Logger
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


logger = Logger.get('events.persons')


@signals.menu.items.connect_via('event-management-sidemenu')
def _sidemenu_items(sender, event, **kwargs):
    if event.can_manage(session.user):
        return SideMenuItem('persons', _('Roles'), url_for('persons.person_list', event), section='organization')


@signals.get_placeholders.connect_via('event-persons-email')
def _get_placeholders(sender, person, event, register_link=False, **kwargs):
    from fossir.modules.events.persons.placeholders import (FirstNamePlaceholder, LastNamePlaceholder, EmailPlaceholder,
                                                            EventTitlePlaceholder, EventLinkPlaceholder,
                                                            RegisterLinkPlaceholder)
    yield FirstNamePlaceholder
    yield LastNamePlaceholder
    yield EmailPlaceholder
    yield EventTitlePlaceholder
    yield EventLinkPlaceholder
    if register_link:
        yield RegisterLinkPlaceholder
