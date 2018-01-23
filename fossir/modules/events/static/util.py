

from __future__ import unicode_literals

import re


_event_url_prefix_re = re.compile(r'^/event/\d+')
_url_has_extension_re = re.compile(r'.*\.([^/]+)$')


def url_to_static_filename(endpoint, url):
    if endpoint.endswith('.static') or endpoint in ('event_images.logo_display', 'event_layout.css_display'):
        # these urls need to remain intact to be downloaded via a HTTP request
        return url
    # get rid of /event/1234
    url = _event_url_prefix_re.sub('', url)
    # get rid of any other leading slash
    url = url.strip('/')
    if not url.startswith('assets/'):
        # replace all remaining slashes
        url = url.replace('/', '--')
    # it's not executed in a webserver, so we do need a .html extension
    if not _url_has_extension_re.match(url):
        url += '.html'
    return url
