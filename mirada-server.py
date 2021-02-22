#!/usr/bin/env python
import os
import shutil
import subprocess
import sys
from typing import List

import click
from dotenv import load_dotenv

from flask.cli import pass_script_info
from flask_frozen import Freezer

from mirada import create_mirada_app

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
def freeze(project_path: str = None, output_path: str = None):
    """Freezes the project to the output path, generating a static HTML site."""
    if project_path is None:
        project_path = os.getcwd()
    if output_path is None:
        output_path = os.path.join(project_path, '_dist')

    click.echo(f'Freezing site to {os.path.abspath(output_path)}...')

    app = create_mirada_app(project_path, include_debug_toolbar=False, include_mirada_admin_bp=False)
    app.config['FREEZER_DESTINATION'] = output_path
    app.config['DEBUG'] = False
    freezer = Freezer(
        app,
        with_no_argument_rules=False,
        log_url_for=False,
    )

    @freezer.register_generator
    def page_uri_path_generator():
        pages_folder = os.path.join(app.template_folder, 'pages')
        for template_path in get_page_template_paths(pages_folder):
            yield 'mirada.blueprints.pages_blueprint.render_page', dict(path_str=f'{template_path.replace(pages_folder, "")}')

    with click.progressbar(freezer.freeze_yield(), item_show_func=lambda p: p.url if p else 'Done!') as urls:
        for url in urls:
            # everything is already happening, just pass
            pass

    click.echo(f'Finished generating site in {os.path.abspath(app.config["FREEZER_DESTINATION"])}')


def get_page_template_paths(template_root_path: str = None, template_paths: List[str] = None) -> List[str]:
    if template_paths is None:
        template_paths = []
    for root, folders, files in os.walk(template_root_path):
        template_paths.extend([
            os.path.join(root, filename)
            for filename in files
        ])
        for folder in folders:
            template_paths.extend(
                get_page_template_paths(template_root_path=os.path.join(root, folder), template_paths=template_paths)
            )
    return template_paths


if __name__ == "__main__":
    load_dotenv(verbose=True)

    cli()
