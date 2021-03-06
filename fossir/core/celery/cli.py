

from __future__ import unicode_literals

import os
import sys

from celery.bin.base import Command
from celery.bin.celery import CeleryCommand, command_classes

from fossir.core.celery import celery
from fossir.core.celery.util import unlock_task
from fossir.core.config import config
from fossir.modules.oauth.models.applications import OAuthApplication, SystemAppType
from fossir.util.console import cformat
from fossir.web.flask.util import url_for


def celery_cmd(args):
    # remove the celery shell command
    next(funcs for group, funcs, _ in command_classes if group == 'Main').remove('shell')
    del CeleryCommand.commands['shell']

    if args and args[0] == 'flower':
        # Somehow flower hangs when executing it using CeleryCommand() so we simply exec it directly.
        # It doesn't really need the celery config anyway (besides the broker url)

        try:
            import flower
        except ImportError:
            print cformat('%{red!}Flower is not installed')
            sys.exit(1)

        app = OAuthApplication.find_one(system_app_type=SystemAppType.flower)
        if not app.redirect_uris:
            print cformat('%{yellow!}Authentication will fail unless you configure the redirect url for the {} OAuth '
                          'application in the administration area.').format(app.name)

        print cformat('%{green!}Only fossir admins will have access to flower.')
        print cformat('%{yellow}Note that revoking admin privileges will not revoke Flower access.')
        print cformat('%{yellow}To force re-authentication, restart Flower.')
        auth_args = ['--auth=^fossir Admin$', '--auth_provider=fossir.core.celery.flower.FlowerAuthHandler']
        auth_env = {'fossir_FLOWER_CLIENT_ID': app.client_id,
                    'fossir_FLOWER_CLIENT_SECRET': app.client_secret,
                    'fossir_FLOWER_AUTHORIZE_URL': url_for('oauth.oauth_authorize', _external=True),
                    'fossir_FLOWER_TOKEN_URL': url_for('oauth.oauth_token', _external=True),
                    'fossir_FLOWER_USER_URL': url_for('users.authenticated_user', _external=True)}
        args = ['celery', '-b', config.CELERY_BROKER] + args + auth_args
        env = dict(os.environ, **auth_env)
        os.execvpe('celery', args, env)
    elif args and args[0] == 'shell':
        print cformat('%{red!}Please use `fossir shell`.')
        sys.exit(1)
    else:
        CeleryCommand(celery).execute_from_commandline(['fossir celery'] + args)


class UnlockCommand(Command):
    """Unlock a locked task.

    Use this if your celery worker was e.g. killed by your kernel's
    oom-killer and thus a task never got unlocked.

    Examples:

        fossir celery unlock event_reminders
    """

    def run(self, name, **kwargs):
        if unlock_task(name):
            print cformat('%{green!}Task {} unlocked').format(name)
        else:
            print cformat('%{yellow}Task {} is not locked').format(name)
