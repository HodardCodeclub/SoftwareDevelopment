

from __future__ import unicode_literals

import platform


def get_os():
    system_name = platform.system()
    if system_name == 'Linux':
        return '{} {} {}'.format(system_name, platform.linux_distribution()[0], platform.linux_distribution()[1])
    else:
        return '{} {}'.format(system_name, platform.release()).rstrip()
