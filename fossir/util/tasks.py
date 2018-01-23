

"""
This module contains very generic Celery tasks which are not specific
to any other module.  Please add tasks in here only if they are generic
enough to be possibly useful somewhere else.  If you need to import
anything from `fossir.modules`, your task most likely does not belong
in here but in your module instead.
"""

from __future__ import unicode_literals

from datetime import timedelta

from celery.schedules import crontab

from fossir.core.celery import celery
from fossir.util.fs import cleanup_dir


def _log_deleted(logger, msg, files):
    for name in sorted(files):
        logger.info(msg, name)


@celery.periodic_task(name='temp_cleanup', run_every=crontab(minute='0', hour='4'))
def temp_cleanup():
    """Cleanup temp/cache dirs"""
    from fossir.core.config import config
    from fossir.core.logger import Logger
    logger = Logger.get()
    deleted = cleanup_dir(config.CACHE_DIR, timedelta(days=1),
                          exclude=lambda x: x.startswith('webassets-'))
    _log_deleted(logger, 'Deleted from cache: %s', deleted)
    deleted = cleanup_dir(config.TEMP_DIR, timedelta(days=1))
    _log_deleted(logger, 'Deleted from temp: %s', deleted)
