

from __future__ import unicode_literals

from flask import current_app, redirect, request

from fossir.modules.events.registration.models.legacy_mapping import LegacyRegistrationMapping
from fossir.web.flask.util import url_for
from fossir.web.rh import RHSimple


@RHSimple.wrap_function
def compat_registration(event_id, path=None):
    url = url_for('event_registration.display_regform_list', confId=event_id)
    try:
        registrant_id = int(request.args['registrantId'])
        authkey = request.args['authkey']
    except KeyError:
        pass
    else:
        mapping = (LegacyRegistrationMapping
                   .find(event_id=event_id, legacy_registrant_id=registrant_id, legacy_registrant_key=authkey)
                   .first())
        if mapping:
            url = url_for('event_registration.display_regform', mapping.registration.locator.registrant)
    return redirect(url, 302 if current_app.debug else 301)
