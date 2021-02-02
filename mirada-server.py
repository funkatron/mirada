#!/usr/bin/env python
import os

import click

from mirada import create_mirada_app

# for now, force this
os.environ['FLASK_ENV'] = 'development'

@click.group()
def cli():
    pass

@cli.command()
@click.option('--project_path', default=os.getcwd())
def run(project_path: str = None):
    if project_path is None:
        project_path = os.getcwd()

    click.echo("Creating and running miranda instance.")
    click.echo(f"Project path: {project_path}.")

    create_mirada_app(project_path).run(debug=True)

@cli.command()
@click.option('--project_path', default=os.getcwd())
def init(project_path: str = None):
    if project_path is None:
        project_path = os.getcwd()

    if not os.path.exists(project_path):
        click.echo(f"The project path {project_path} does not exist.")

    click.echo(f"Initializing project at {project_path}.")

    raise NotImplementedError


@cli.command()
@click.option('--project_path', default=os.getcwd())
@click.option('--output_path', default=os.path.join(os.getcwd(), '_dist'))
def freeze(project_path: str = None):
    """Freezes the project to the output path, generating a static HTML site."""
    if project_path is None:
        project_path = os.getcwd()
    raise NotImplementedError
    # create_mirada_app(project_path)


if __name__ == "__main__":
    cli()
