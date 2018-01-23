

from __future__ import unicode_literals

from datetime import timedelta

from flask import flash, redirect, request, session

from fossir.core.db import db
from fossir.modules.admin import RHAdminBase
from fossir.modules.news import logger, news_settings
from fossir.modules.news.forms import NewsForm, NewsSettingsForm
from fossir.modules.news.models.news import NewsItem
from fossir.modules.news.util import get_recent_news
from fossir.modules.news.views import WPManageNews, WPNews
from fossir.util.date_time import now_utc
from fossir.util.i18n import _
from fossir.web.flask.util import url_for
from fossir.web.forms.base import FormDefaults
from fossir.web.rh import RH
from fossir.web.util import jsonify_data, jsonify_form


class RHNews(RH):
    @staticmethod
    def _is_new(item):
        days = news_settings.get('new_days')
        if not days:
            return False
        return item.created_dt.date() >= (now_utc() - timedelta(days=days)).date()

    def _process(self):
        news = NewsItem.query.order_by(NewsItem.created_dt.desc()).all()
        return WPNews.render_template('news.html', news=news, _is_new=self._is_new)


class RHManageNewsBase(RHAdminBase):
    pass


class RHManageNews(RHManageNewsBase):
    def _process(self):
        news = NewsItem.query.order_by(NewsItem.created_dt.desc()).all()
        return WPManageNews.render_template('admin/news.html', 'news', news=news)


class RHNewsSettings(RHManageNewsBase):
    def _process(self):
        form = NewsSettingsForm(obj=FormDefaults(**news_settings.get_all()))
        if form.validate_on_submit():
            news_settings.set_multi(form.data)
            get_recent_news.clear_cached()
            flash(_('Settings have been saved'), 'success')
            return jsonify_data()
        return jsonify_form(form)


class RHCreateNews(RHManageNewsBase):
    def _process(self):
        form = NewsForm()
        if form.validate_on_submit():
            item = NewsItem()
            form.populate_obj(item)
            db.session.add(item)
            db.session.flush()
            get_recent_news.clear_cached()
            logger.info('News %r created by %s', item, session.user)
            flash(_("News '{title}' has been posted").format(title=item.title), 'success')
            return jsonify_data(flash=False)
        return jsonify_form(form)


class RHManageNewsItemBase(RHManageNewsBase):
    def _process_args(self):
        RHManageNewsBase._process_args(self)
        self.item = NewsItem.get_one(request.view_args['news_id'])


class RHEditNews(RHManageNewsItemBase):
    def _process(self):
        form = NewsForm(obj=self.item)
        if form.validate_on_submit():
            old_title = self.item.title
            form.populate_obj(self.item)
            db.session.flush()
            get_recent_news.clear_cached()
            logger.info('News %r modified by %s', self.item, session.user)
            flash(_("News '{title}' has been updated").format(title=old_title), 'success')
            return jsonify_data(flash=False)
        return jsonify_form(form)


class RHDeleteNews(RHManageNewsItemBase):
    def _process(self):
        db.session.delete(self.item)
        get_recent_news.clear_cached()
        flash(_("News '{title}' has been deleted").format(title=self.item.title), 'success')
        logger.info('News %r deleted by %r', self.item, session.user)
        return redirect(url_for('news.manage'))
