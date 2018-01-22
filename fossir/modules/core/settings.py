

from __future__ import unicode_literals

from fossir.core.settings import SettingsProxy


core_settings = SettingsProxy('core', {
    'site_title': 'fossir',
    'site_organization': ''
})


social_settings = SettingsProxy('social', {
    'enabled': False,
    'facebook_app_id': ''
})
