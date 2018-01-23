


from functools import wraps

from jinja2.ext import babel_extract

from fossir.util.string import encode_if_unicode, trim_inner_whitespace


# TODO: Remove this once there's proper support in upstream Jinja
# https://github.com/pallets/jinja/pull/683
def jinja2_babel_extract(fileobj, keywords, comment_tags, options):
    """Custom babel_extract for Jinja.

    Hooks on to Jinja's babel_extract and handles
    whitespace within ``{% trans %}`` tags.
    """
    for lineno, func, message, comments in babel_extract(fileobj, keywords, comment_tags, options):
        if isinstance(message, tuple):
            message = tuple(trim_inner_whitespace(x) if isinstance(x, basestring) else x for x in message)
        else:
            message = trim_inner_whitespace(message)
        yield lineno, func, message, comments
