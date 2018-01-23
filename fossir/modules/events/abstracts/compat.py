

from __future__ import unicode_literals

from flask import redirect

from fossir.modules.events.abstracts.models.abstracts import Abstract
from fossir.web.flask.util import url_for
from fossir.web.rh import RHSimple


@RHSimple.wrap_function
def compat_abstract(endpoint, confId, friendly_id, track_id=None, management=False):
    abstract = Abstract.find(event_id=confId, friendly_id=friendly_id).first_or_404()
    return redirect(url_for('abstracts.' + endpoint, abstract, management=management))
