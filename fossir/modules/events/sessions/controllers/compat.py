

from __future__ import unicode_literals

from flask import current_app, redirect

from fossir.modules.events.sessions.models.legacy_mapping import LegacySessionMapping
from fossir.web.flask.util import url_for
from fossir.web.rh import RHSimple


@RHSimple.wrap_function
def compat_session(_endpoint, event_id, legacy_session_id):
    sess = (LegacySessionMapping
            .find(event_id=event_id, legacy_session_id=legacy_session_id)
            .first_or_404()
            .session)
    url = url_for('sessions.' + _endpoint, sess)
    return redirect(url, 302 if current_app.debug else 301)
