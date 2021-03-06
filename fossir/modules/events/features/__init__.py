

from __future__ import unicode_literals

from flask import flash, request, session

from fossir.core import signals
from fossir.core.logger import Logger
from fossir.modules.events.settings import EventSettingsProxy
from fossir.util.i18n import ngettext
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


logger = Logger.get('events.features')
features_event_settings = EventSettingsProxy('features', {
    'enabled': None
})


@signals.menu.items.connect_via('event-management-sidemenu')
def _extend_event_management_menu(sender, event, **kwargs):
    if not event.can_manage(session.user):
        return
    return SideMenuItem('features', 'Features', url_for('event_features.index', event), section='advanced')


@signals.app_created.connect
def _check_feature_definitions(app, **kwargs):
    # This will raise RuntimeError if the feature names are not unique
    from fossir.modules.events.features.util import get_feature_definitions
    get_feature_definitions()


@signals.event.created.connect
def _event_created(event, **kwargs):
    from fossir.modules.events.features.util import get_feature_definitions, get_enabled_features
    feature_definitions = get_feature_definitions()
    for feature in get_enabled_features(event):
        feature_definitions[feature].enabled(event)


@signals.event.type_changed.connect
def _event_type_changed(event, **kwargs):
    from fossir.modules.events.features.util import (get_enabled_features, get_disallowed_features, set_feature_enabled,
                                                     format_feature_names)
    conflicting = get_enabled_features(event, only_explicit=True) & get_disallowed_features(event)
    if conflicting:
        for feature in conflicting:
            set_feature_enabled(event, feature, False)
        if request.endpoint != 'api.jsonrpc':
            # XXX: we cannot flash a message in the legacy js ajax editor for the event type.
            # remove this check once we don't use it anymore (on the general settings page)
            flash(ngettext('Feature disabled: {features} (not available for this event type)',
                           'Features disabled: {features} (not available for this event type)', len(conflicting))
                  .format(features=format_feature_names(conflicting)), 'warning')
