# This file is part of fossir.
# Copyright (C) 2002 - 2017 European Organization for Nuclear Research (CERN).
#
# fossir is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# fossir is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fossir; if not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from fossir.modules.events import event_object_url_prefixes
from fossir.modules.events.notes.controllers import RHCompileNotes, RHDeleteNote, RHEditNote, RHViewNote
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('event_notes', __name__, template_folder='templates', virtual_template_folder='events/notes',
                      url_prefix='/event/<confId>')

_bp.add_url_rule('/note/compile', 'compile', RHCompileNotes, methods=('GET', 'POST'), defaults={'object_type': 'event'})


for object_type, prefixes in event_object_url_prefixes.iteritems():
    for prefix in prefixes:
        _bp.add_url_rule(prefix + '/note/', 'view', RHViewNote, defaults={'object_type': object_type})
        _bp.add_url_rule(prefix + '/note/edit', 'edit', RHEditNote, methods=('GET', 'POST'),
                         defaults={'object_type': object_type})
        _bp.add_url_rule(prefix + '/note/delete', 'delete', RHDeleteNote, methods=('POST',),
                         defaults={'object_type': object_type})
