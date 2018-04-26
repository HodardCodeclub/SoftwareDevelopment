

from __future__ import unicode_literals

import os


def get_asset_path(path, plugin=None, theme=None):
    if plugin:
        base = 'plugin-{}'.format(plugin)
    elif theme:
        base = 'theme-{}'.format(theme)
    else:
        base = 'core'
    return os.path.join(base, path)
