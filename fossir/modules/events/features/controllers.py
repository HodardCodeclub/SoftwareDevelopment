

from __future__ import unicode_literals

from flask import flash, request, session
from werkzeug.exceptions import Forbidden
from wtforms.fields import BooleanField

from fossir.modules.events.features import logger
from fossir.modules.events.features.util import (format_feature_names, get_disallowed_features, get_enabled_features,
                                                 get_feature_definition, get_feature_definitions, set_feature_enabled)
from fossir.modules.events.features.views import WPFeatures
from fossir.modules.events.logs import EventLogKind, EventLogRealm
from fossir.modules.events.management.controllers import RHManageEventBase
from fossir.util.i18n import _, ngettext
from fossir.web.forms.base import FormDefaults, fossirForm
from fossir.web.forms.widgets import SwitchWidget
from fossir.web.menu import render_sidemenu
from fossir.web.util import jsonify_data


class RHFeaturesBase(RHManageEventBase):
    pass


class RHFeatures(RHFeaturesBase):
    """Shows the list of available event features"""

    def _make_form(self):
        form_class = type(b'FeaturesForm', (fossirForm,), {})
        disallowed = get_disallowed_features(self.event)
        for name, feature in sorted(get_feature_definitions().iteritems(), key=lambda x: x[1].friendly_name):
            if name in disallowed:
                continue
            field = BooleanField(feature.friendly_name, widget=SwitchWidget(on_label=_('On'), off_label=_('Off')),
                                 description=feature.description)
            setattr(form_class, name, field)
        defaults = {name: True for name in get_enabled_features(self.event)}
        return form_class(csrf_enabled=False, obj=FormDefaults(defaults))

    def _process(self):
        form = self._make_form()
        widget_attrs = {field.short_name: {'disabled': True} for field in form} if self.event.is_locked else {}
        return WPFeatures.render_template('features.html', self.event, form=form, widget_attrs=widget_attrs)


class RHSwitchFeature(RHFeaturesBase):
    """Enables/disables a feature"""

    def render_event_menu(self):
        return render_sidemenu('event-management-sidemenu', active_item=WPFeatures.sidemenu_option,
                               event=self.event)

    def _process_PUT(self):
        prev = get_enabled_features(self.event)
        feature = get_feature_definition(request.view_args['feature'])
        if feature.name in get_disallowed_features(self.event):
            raise Forbidden('Feature not available')
        changed = set()
        if set_feature_enabled(self.event, feature.name, True):
            current = get_enabled_features(self.event)
            changed = current - prev
            flash(ngettext('Feature enabled: {features}', 'Features enabled: {features}', len(changed))
                  .format(features=format_feature_names(changed)), 'success')
            logger.info("Feature '%s' for event %s enabled by %s", feature.name, self.event, session.user)
            self.event.log(EventLogRealm.management, EventLogKind.positive, 'Features',
                           'Enabled {}'.format(feature.friendly_name), session.user)
        return jsonify_data(enabled=True, event_menu=self.render_event_menu(), changed=list(changed))

    def _process_DELETE(self):
        prev = get_enabled_features(self.event)
        feature = get_feature_definition(request.view_args['feature'])
        changed = set()
        if set_feature_enabled(self.event, feature.name, False):
            current = get_enabled_features(self.event)
            changed = prev - current
            flash(ngettext('Feature disabled: {features}', 'Features disabled: {features}', len(changed))
                  .format(features=format_feature_names(changed)), 'warning')
            logger.info("Feature '%s' for event %s disabled by %s", feature.name, self.event, session.user)
            self.event.log(EventLogRealm.management, EventLogKind.negative, 'Features',
                           'Disabled {}'.format(feature.friendly_name), session.user)
        return jsonify_data(enabled=False, event_menu=self.render_event_menu(), changed=list(changed))
