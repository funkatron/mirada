#!/usr/bin/env python
import os
import shutil
import subprocess
import sys

import click
from dotenv import load_dotenv

from flask.cli import pass_script_info

IS_BUNDLED = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
# register the mirada admin blueprint
MIRADA_PROJ_PATH = os.path.abspath(os.path.dirname(__file__))
if IS_BUNDLED:
    MIRADA_PROJ_PATH = os.path.abspath(getattr(sys, '_MEIPASS'))

# for now, force this
os.environ['FLASK_ENV'] = 'development'
os.environ['EXPLAIN_TEMPLATE_LOADING'] = '1'

@click.group()
def cli():
    pass


@cli.command()
@click.option('--project-path', default=os.getcwd())
def run(*args, **kwargs):
    os.environ['MIRADA_CURRENT_PROJECT_PATH'] = kwargs.pop('project_path', os.getcwd())

    click.echo("Creating and running Mirada instance.")
    click.echo(f"Project path: {os.environ['MIRADA_CURRENT_PROJECT_PATH']}.")

    # @TODO map kwargs to CLI args for flask run
    cmd = ['flask', 'run']

    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, universal_newlines=True, env=os.environ)
    while popen.poll() is None:
        for read_data in iter(lambda: bytes(popen.stdout.read(1), encoding='UTF8'), ''):
            sys.stdout.buffer.write(read_data)
            sys.stdout.buffer.flush()
    sys.stdout.buffer.flush()
    click.echo("Flask app process complete.\n\n")


@cli.command()
@click.option('--project_path', default=os.getcwd())
@pass_script_info
def init(script_info, project_path: str = None):
    if project_path is None:
        project_path = os.getcwd()

    if not os.path.exists(project_path):
        click.echo(f"The project path {project_path} does not exist.")

    click.echo(f"Initializing project at {project_path}.")

    static_path = os.path.join(project_path, 'static')
    templates_path = os.path.join(project_path, 'templates')

    if not os.path.exists(static_path):
        os.mkdir(static_path)
        shutil.copy()

    raise NotImplementedError


@cli.command()
@click.option('--project_path', default=os.getcwd())
@click.option('--output_path', default=os.path.join(os.getcwd(), '_dist'))
@pass_script_info
def freeze(script_info, project_path: str = None):
    """Freezes the project to the output path, generating a static HTML site."""
    if project_path is None:
        project_path = os.getcwd()
    raise NotImplementedError
    # create_mirada_app(project_path)


if __name__ == "__main__":
    load_dotenv(verbose=True)

    cli()
