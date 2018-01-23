

from __future__ import unicode_literals

import pytest


@pytest.fixture
def smtp(disallow_emails, smtpserver, app):
    """Wrapper for the `smtpserver` fixture which updates the fossir config
    and disables the SMTP autofail logic for that smtp server.
    """
    old_config = app.config['fossir']
    app.config['fossir'] = dict(app.config['fossir'])  # make it mutable
    app.config['fossir']['SMTP_SERVER'] = smtpserver.addr
    disallow_emails.add(smtpserver.addr)  # whitelist our smtp server
    yield smtpserver
    app.config['fossir'] = old_config
