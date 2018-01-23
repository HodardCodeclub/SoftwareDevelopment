

from __future__ import unicode_literals

from fossir.modules.news.controllers import RHCreateNews, RHDeleteNews, RHEditNews, RHManageNews, RHNews, RHNewsSettings
from fossir.web.flask.wrappers import fossirBlueprint


_bp = fossirBlueprint('news', __name__, template_folder='templates', virtual_template_folder='news')

_bp.add_url_rule('/news', 'display', RHNews)
_bp.add_url_rule('/admin/news/', 'manage', RHManageNews)
_bp.add_url_rule('/admin/news/settings', 'settings', RHNewsSettings, methods=('GET', 'POST'))
_bp.add_url_rule('/admin/news/create', 'create_news', RHCreateNews, methods=('GET', 'POST'))
_bp.add_url_rule('/admin/news/<int:news_id>/', 'edit_news', RHEditNews, methods=('GET', 'POST'))
_bp.add_url_rule('/admin/news/<int:news_id>/delete', 'delete_news', RHDeleteNews, methods=('GET', 'POST'))
