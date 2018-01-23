


from __future__ import unicode_literals

import logging
import os
import re
import sys
import tempfile

import py


# Ignore config file in case there is one
os.environ['fossir_CONFIG'] = os.devnull

pytest_plugins = ('fossir.testing.fixtures.app', 'fossir.testing.fixtures.category',
                  'fossir.testing.fixtures.contribution', 'fossir.testing.fixtures.database',
                  'fossir.testing.fixtures.disallow', 'fossir.testing.fixtures.person', 'fossir.testing.fixtures.user',
                  'fossir.testing.fixtures.event', 'fossir.testing.fixtures.smtp', 'fossir.testing.fixtures.storage',
                  'fossir.testing.fixtures.util')


def pytest_configure(config):
    # Load all the plugins defined in pytest_plugins
    config.pluginmanager.consider_module(sys.modules[__name__])
    config.fossir_temp_dir = py.path.local(tempfile.mkdtemp(prefix='fossirtesttmp.'))
    config.fossir_plugins = filter(None, [x.strip() for x in re.split(r'[\s,;]+', config.getini('fossir_plugins'))])
    # Make sure we don't write any log files (or worse: send emails)
    assert not logging.root.handlers
    logging.root.addHandler(logging.NullHandler())
    # Silence the annoying pycountry logger
    logging.getLogger('pycountry.db').addHandler(logging.NullHandler())


def pytest_unconfigure(config):
    config.fossir_temp_dir.remove(rec=True)


def pytest_addoption(parser):
    parser.addini('fossir_plugins', 'List of fossir plugins to load')
