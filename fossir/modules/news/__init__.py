

from __future__ import unicode_literals

from flask import session

from fossir.core import signals
from fossir.core.logger import Logger
from fossir.core.settings import SettingsProxy
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.menu import SideMenuItem


logger = Logger.get('news')

news_settings = SettingsProxy('news', {
    # Whether to show the recent news on the home page
    'show_recent': True,
    # The number of recent news to show on the home page
    'max_entries': 3,
    # How old a news may be to be shown on the home page
    'max_age': 0,
    # How long a news is labelled as 'new'
    'new_days': 14
})


@signals.menu.items.connect_via('admin-sidemenu')
def _sidemenu_items(sender, **kwargs):
    if session.user.is_admin:
        yield SideMenuItem('news', _('News'), url_for('news.manage'), section='homepage')
