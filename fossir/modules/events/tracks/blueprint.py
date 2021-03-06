

from __future__ import unicode_literals

from fossir.modules.events.tracks.controllers import (RHCreateTrack, RHDeleteTrack, RHDisplayTracks, RHEditProgram,
                                                      RHEditTrack, RHManageTracks, RHSortTracks, RHTracksPDF)
from fossir.web.flask.util import make_compat_redirect_func
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('tracks', __name__, template_folder='templates', virtual_template_folder='events/tracks',
                      url_prefix='/event/<confId>')

_bp.add_url_rule('/manage/tracks/', 'manage', RHManageTracks)
_bp.add_url_rule('/manage/tracks/program', 'edit_program', RHEditProgram, methods=('GET', 'POST'))
_bp.add_url_rule('/manage/tracks/create', 'create_track', RHCreateTrack, methods=('GET', 'POST'))
_bp.add_url_rule('/manage/tracks/sort', 'sort_tracks', RHSortTracks, methods=('POST',))
_bp.add_url_rule('/manage/tracks/<int:track_id>', 'edit_track', RHEditTrack, methods=('GET', 'POST'))
_bp.add_url_rule('/manage/tracks/<int:track_id>', 'delete_track', RHDeleteTrack, methods=('DELETE',))

_bp.add_url_rule('/program', 'program', RHDisplayTracks)
_bp.add_url_rule('/program.pdf', 'program_pdf', RHTracksPDF)


_compat_bp = fossirBlueprint('compat_tracks', __name__, url_prefix='/event/<int:confId>')
_compat_bp.add_url_rule('/manage/program/tracks/<int:track_id>/contributions/', 'track_contribs',
                        make_compat_redirect_func('contributions', 'contribution_list',
                                                  view_args_conv={'track_id': None}))
