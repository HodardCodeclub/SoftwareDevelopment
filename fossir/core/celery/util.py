

from __future__ import unicode_literals

from functools import wraps

from celery import current_task

from fossir.core.logger import Logger
from fossir.legacy.common.cache import GenericCache


def locked_task(f):
    """Decorator to prevent a task from running multiple times at once."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        cache = GenericCache('task-locks')
        name = current_task.name
        if cache.get(name):
            Logger.get('celery').warning('Task %s is locked; not executing it. '
                                         'To manually unlock it, run `fossir celery unlock %s`',
                                         name, name)
            return
        cache.set(name, True, 86400)
        try:
            return f(*args, **kwargs)
        finally:
            cache.delete(name)
    return wrapper


def unlock_task(name):
    """Unlock a locked task.

    :return: ``True`` if the task has been unlocked; ``False`` if it was not locked.
    """
    cache = GenericCache('task-locks')
    if not cache.get(name):
        return False
    cache.delete(name)
    return True
