

import copy

from flask import request, session
from sqlalchemy.exc import DatabaseError
from werkzeug.exceptions import BadRequest

from fossir.core import signals
from fossir.core.db import db
from fossir.core.db.sqlalchemy.core import handle_sqlalchemy_database_error
from fossir.core.notifications import flush_email_queue, init_email_queue
from fossir.legacy.services.interface.rpc import handlers
from fossir.util import fossilize


def _lookup_handler(method):
    endpoint, functionName = handlers, method
    while True:
        handler = endpoint.methodMap.get(functionName, None)
        if handler:
            break
        try:
            endpointName, functionName = method.split('.', 1)
        except Exception:
            raise BadRequest('Unsupported method')

        if 'endpointMap' in dir(endpoint):
            endpoint = endpoint.endpointMap.get(endpointName, None)
            if not endpoint:
                raise BadRequest('Unknown endpoint: {}'.format(endpointName))
        else:
            raise BadRequest('Unsupported method')
    return handler


def _process_request(method, params):
    handler = _lookup_handler(method)

    if session.csrf_protected and session.csrf_token != request.headers.get('X-CSRF-Token'):
        msg = _(u"It looks like there was a problem with your current session. Please use your browser's back "
                u"button, reload the page and try again.")
        raise BadRequest(msg)

    if hasattr(handler, 'process'):
        return handler(params).process()
    else:
        return handler(params)


def invoke_method(method, params):
    result = None
    fossilize.clearCache()
    init_email_queue()
    try:
        result = _process_request(method, copy.deepcopy(params))
        signals.after_process.send()
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        handle_sqlalchemy_database_error()
    except Exception:
        db.session.rollback()
        raise
    flush_email_queue()
    return result
