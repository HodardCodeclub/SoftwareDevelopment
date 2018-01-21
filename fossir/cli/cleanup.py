

from __future__ import unicode_literals

from datetime import timedelta

import click

from fossir.core.config import config
from fossir.util.fs import cleanup_dir


def _print_files(files):
    if not files:
        click.echo(click.style('  nothing to delete', fg='green'))
        return
    for path in sorted(files):
        click.echo('  * ' + click.style(path, fg='yellow'))


def cleanup_cmd(temp=False, cache=False, assets=False, min_age=1, dry_run=False, verbose=False):
    if cache:
        if verbose:
            click.echo(click.style('cleaning cache ({})'.format(config.CACHE_DIR), fg='white', bold=True))
        deleted = cleanup_dir(config.CACHE_DIR, timedelta(days=min_age), dry_run=dry_run,
                              exclude=lambda x: x.startswith('webassets-'))
        if verbose:
            _print_files(deleted)
    if temp:
        if verbose:
            click.echo(click.style('cleaning temp ({})'.format(config.TEMP_DIR), fg='white', bold=True))
        deleted = cleanup_dir(config.TEMP_DIR, timedelta(days=min_age), dry_run=dry_run)
        if verbose:
            _print_files(deleted)
    if assets:
        if verbose:
            click.echo(click.style('cleaning assets ({})'.format(config.ASSETS_DIR), fg='white', bold=True))
        deleted = cleanup_dir(config.ASSETS_DIR, timedelta(days=min_age), dry_run=dry_run)
        if verbose:
            _print_files(deleted)
    if dry_run:
        click.echo(click.style('dry-run enabled, nothing has been deleted', fg='green', bold=True))
