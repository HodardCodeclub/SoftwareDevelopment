

from __future__ import unicode_literals

import os
import re

from flask import current_app, request, send_from_directory, session
from itsdangerous import BadData
from sqlalchemy.exc import DatabaseError
from werkzeug.exceptions import BadRequest, BadRequestKeyError, Forbidden, HTTPException, NotFound

from fossir.core.errors import fossirError, get_error_description
from fossir.core.logger import Logger, sentry_log_exception
from fossir.modules.auth.util import redirect_to_login
from fossir.util.i18n import _
from fossir.util.string import to_unicode
from fossir.web.errors import render_error
from fossir.web.flask.wrappers import fossirBlueprint


errors_bp = fossirBlueprint('errors', __name__)


@errors_bp.app_errorhandler(NotFound)
def handle_notfound(exc):
    try:
        if re.search(r'\.py(?:/\S+)?$', request.path):
            # While not dangerous per se, we never serve *.py files as static
            raise NotFound
        htdocs = os.path.join(current_app.root_path, 'htdocs')
        try:
            return send_from_directory(htdocs, request.path[1:], conditional=True)
        except (UnicodeEncodeError, BadRequest):
            raise NotFound
    except NotFound:
        if exc.description == NotFound.description:
            # The default reason is too long and not localized
            description = get_error_description(exc)
        else:
            description = exc.description
        return render_error(exc, _('Not Found'), description, exc.code)


@errors_bp.app_errorhandler(Forbidden)
def handle_forbidden(exc):
    if exc.response:
        return exc
    if session.user is None and not request.is_xhr and request.blueprint != 'auth':
        return redirect_to_login(reason=_('Please log in to access this page.'))
    return render_error(exc, _('Access Denied'), get_error_description(exc), exc.code)


@errors_bp.app_errorhandler(BadRequestKeyError)
def handle_badrequestkeyerror(exc):
    if current_app.debug:
        raise
    msg = _('Required argument missing: {}').format(to_unicode(exc.message))
    return render_error(exc, exc.name, msg, exc.code)


@errors_bp.app_errorhandler(HTTPException)
def handle_http_exception(exc):
    if not (400 <= exc.code <= 599):
        # if it's not an actual error, use it as a response.
        # this is needed e.g. for the 301 redirects that are raised
        # as routing exceptions and thus end up here
        return exc
    elif exc.response:
        # if the exception has a custom response, we always use that
        # one instead of showing the default error page
        return exc
    return render_error(exc, exc.name, get_error_description(exc), exc.code)


@errors_bp.app_errorhandler(BadData)
def handle_baddata(exc):
    return render_error(exc, _('Invalid or expired token'), to_unicode(exc.message), 400)


@errors_bp.app_errorhandler(fossirError)
def handle_fossir_exception(exc):
    return render_error(exc, _('Something went wrong'), to_unicode(exc.message), getattr(exc, 'http_status_code', 500))


@errors_bp.app_errorhandler(DatabaseError)
def handle_databaseerror(exc):
    return handle_exception(exc, _('There was a database error while processing your request.'))


@errors_bp.app_errorhandler(Exception)
def handle_exception(exc, message=None):
    Logger.get('flask').exception(to_unicode(exc.message) or 'Uncaught Exception')
    if not current_app.debug or request.is_xhr or request.is_json:
        sentry_log_exception()
        if message is None:
            message = '{}: {}'.format(type(exc).__name__, to_unicode(exc.message))
        return render_error(exc, _('Something went wrong'), message, 500)
    # Let the exception propagate to middleware /the webserver.
    # This triggers the Flask debugger in development and sentry
    # logging (if enabled) (via got_request_exception).
    raise
