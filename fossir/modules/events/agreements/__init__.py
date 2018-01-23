

from __future__ import unicode_literals

from flask import session

from fossir.core import signals
from fossir.core.logger import Logger
from fossir.modules.events.agreements.base import AgreementDefinitionBase, AgreementPersonInfo
from fossir.modules.events.agreements.models.agreements import Agreement
from fossir.modules.events.agreements.placeholders import AgreementLinkPlaceholder, PersonNamePlaceholder
from fossir.modules.events.agreements.util import get_agreement_definitions
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


__all__ = ('AgreementPersonInfo', 'AgreementDefinitionBase')

logger = Logger.get('agreements')


@signals.app_created.connect
def _check_agreement_definitions(app, **kwargs):
    # This will raise RuntimeError if the agreement definition types are not unique
    get_agreement_definitions()


@signals.menu.items.connect_via('event-management-sidemenu')
def _extend_event_management_menu(sender, event, **kwargs):
    if not get_agreement_definitions():
        return
    if not event.can_manage(session.user):
        return
    return SideMenuItem('agreements', _('Agreements'), url_for('agreements.event_agreements', event),
                        section='services')


@signals.users.merged.connect
def _merge_users(target, source, **kwargs):
    Agreement.find(user_id=source.id).update({Agreement.user_id: target.id})


@signals.get_placeholders.connect_via('agreement-email')
def _get_placeholders(sender, agreement, definition, **kwargs):
    yield PersonNamePlaceholder
    yield AgreementLinkPlaceholder
