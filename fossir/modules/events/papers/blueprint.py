

from __future__ import unicode_literals

from flask import current_app, g

from fossir.modules.events.papers.controllers import display, management, paper, templates
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('papers', __name__, url_prefix='/event/<confId>', template_folder='templates',
                      virtual_template_folder='events/papers')


# Display pages
_bp.add_url_rule('/papers/', 'call_for_papers', display.RHCallForPapers)
_bp.add_url_rule('/papers/select-contribution', 'select_contribution', display.RHSelectContribution)
_bp.add_url_rule('/papers/<int:contrib_id>/', 'paper_timeline', display.RHPaperTimeline)
_bp.add_url_rule('/papers/<int:contrib_id>/files/<int:file_id>-<filename>', 'download_file',
                 display.RHDownloadPaperFile)
_bp.add_url_rule('/papers/templates/<int:template_id>-<filename>', 'download_template',
                 templates.RHDownloadPaperTemplate)
_bp.add_url_rule('/contributions/<int:contrib_id>/paper/submit', 'submit_revision',
                 display.RHSubmitPaper, methods=('GET', 'POST'))
# Paper reviews/judgments
_bp.add_url_rule('/papers/<int:contrib_id>/review/type/<review_type>', 'submit_review',
                 display.RHSubmitPaperReview, methods=('GET', 'POST'))
_bp.add_url_rule('/papers/<int:contrib_id>/revision/<int:revision_id>/review/<int:review_id>/edit', 'edit_review',
                 display.RHEditPaperReview, methods=('GET', 'POST'))
_bp.add_url_rule('/papers/<int:contrib_id>/judgment', 'judge_paper',
                 display.RHJudgePaper, methods=('POST',))
_bp.add_url_rule('/papers/<int:contrib_id>/judgment', 'reset_paper_state',
                 display.RHResetPaperState, methods=('DELETE',))
# Paper comments
_bp.add_url_rule('/papers/<int:contrib_id>/comment', 'submit_comment',
                 display.RHSubmitPaperComment, methods=('POST',))
_bp.add_url_rule('/papers/<int:contrib_id>/revision/<int:revision_id>/comment/<int:comment_id>', 'edit_comment',
                 display.RHEditPaperComment, methods=('GET', 'POST'))
_bp.add_url_rule('/papers/<int:contrib_id>/revision/<int:revision_id>/comment/<int:comment_id>', 'delete_comment',
                 display.RHDeletePaperComment, methods=('DELETE',))
# Reviewing area
_bp.add_url_rule('/papers/reviewing/', 'reviewing_area', display.RHReviewingArea)

# Management
_bp.add_url_rule('/manage/papers/', 'management', management.RHPapersDashboard)
_bp.add_url_rule('/manage/papers/deadlines/<any(judge,content_reviewer,layout_reviewer):role>', 'manage_deadline',
                 management.RHSetDeadline, methods=('GET', 'POST'))
_bp.add_url_rule('/manage/papers/settings', 'manage_reviewing_settings', management.RHManageReviewingSettings,
                 methods=('GET', 'POST'))
_bp.add_url_rule('/manage/papers/templates/', 'manage_templates', templates.RHManagePaperTemplates)
_bp.add_url_rule('/manage/papers/templates/add', 'upload_template',
                 templates.RHUploadPaperTemplate, methods=('GET', 'POST'))
_bp.add_url_rule('/manage/papers/templates/<int:template_id>-<filename>', 'delete_template',
                 templates.RHDeletePaperTemplate, methods=('DELETE',))
_bp.add_url_rule('/manage/papers/templates/<int:template_id>-<filename>/edit', 'edit_template',
                 templates.RHEditPaperTemplate, methods=('GET', 'POST'))
_bp.add_url_rule('/manage/papers/teams/', 'manage_teams', management.RHManagePaperTeams, methods=('GET', 'POST'))
_bp.add_url_rule('/manage/papers/teams/competences', 'manage_competences', management.RHManageCompetences,
                 methods=('GET', 'POST'))
_bp.add_url_rule('/manage/papers/teams/contact', 'contact_staff', management.RHContactStaff, methods=('GET', 'POST'))
_bp.add_url_rule('/manage/papers/enable/<any(content,layout):reviewing_type>', 'switch',
                 management.RHSwitchReviewingType, methods=('PUT', 'DELETE'))

# CFP scheduling
_bp.add_url_rule('/manage/papers/schedule', 'schedule_cfp', management.RHScheduleCFP,
                 methods=('GET', 'POST'))
_bp.add_url_rule('/manage/papers/open', 'open_cfp', management.RHOpenCFP, methods=('POST',))
_bp.add_url_rule('/manage/papers/close', 'close_cfp', management.RHCloseCFP, methods=('POST',))

# URLs available in both management and display areas
# Note: When adding a new one here make sure to specify `defaults=defaults`
#       for each rule. Otherwise you may not get the correct one.
for prefix, is_management in (('/manage/papers/assignment-list', True), ('/papers/judging', False)):
    defaults = {'management': is_management}
    _bp.add_url_rule(prefix + '/', 'papers_list', paper.RHPapersList, defaults=defaults)
    _bp.add_url_rule(prefix + '/download', 'download_papers', paper.RHDownloadPapers, methods=('POST',),
                     defaults=defaults)
    _bp.add_url_rule(prefix + '/customize', 'customize_paper_list', paper.RHCustomizePapersList,
                     methods=('GET', 'POST'), defaults=defaults)
    _bp.add_url_rule(prefix + '/judge', 'judge_papers', paper.RHJudgePapers, methods=('GET', 'POST'), defaults=defaults)
    _bp.add_url_rule(prefix + '/assign/<any(judge,content_reviewer,layout_reviewer):role>', 'assign_papers',
                     paper.RHAssignPapers, methods=('POST',), defaults=defaults)
    _bp.add_url_rule(prefix + '/unassign/<any(judge,content_reviewer,layout_reviewer):role>', 'unassign_papers',
                     paper.RHUnassignPapers, methods=('POST',), defaults=defaults)


@_bp.url_defaults
def _add_management_flag(endpoint, values):
    if ('management' not in values and
            endpoint.split('.')[0] == _bp.name and
            current_app.url_map.is_endpoint_expecting(endpoint, 'management')):
        # XXX: using getattr because the conference menu builds the url from an
        # RH without the management attribute
        values['management'] = getattr(g.rh, 'management', False)


# Legacy URLs
_compat_bp = fossirBlueprint('compat_papers', __name__, url_prefix='/event/<int:confId>')
# TODO...
