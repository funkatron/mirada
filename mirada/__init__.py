import logging
import os
import sys

from dotenv import load_dotenv
from flask import Flask

from mirada.blueprints.mirada_blueprint import bp as admin_bp
from mirada.blueprints.pages_blueprint import bp as pages_bp

IS_BUNDLED = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
# register the mirada admin blueprint
MIRADA_PROJ_PATH = os.path.abspath(os.path.dirname(__file__))
if IS_BUNDLED:
    MIRADA_PROJ_PATH = os.path.abspath(getattr(sys, '_MEIPASS'))


def create_app(name=__name__, template_folder: str = None, static_folder: str = None, debug: bool = None):
    # get the path to the directory where this file is located
    app = Flask(
        name,
        template_folder=template_folder,
        static_folder=static_folder,
    )
    app.logger.setLevel(logging.DEBUG if debug is True else logging.INFO)
    return app


def create_mirada_app(project_path: str = None):
    if project_path is None:
        project_path = os.getenv('MIRADA_CURRENT_PROJECT_PATH', os.getcwd())

    load_dotenv()

    # register the project page routing blueprint
    project_template_folder = os.path.join(project_path, 'templates')
    project_static_folder = os.path.join(project_path, 'static')
    mirada_app = create_app(name='mirada', template_folder=project_template_folder, static_folder=project_static_folder)

    mirada_app.logger.info(f'Mirada Server Startup')
    mirada_app.logger.info(f'project_path="{project_path}"')

    mirada_app.register_blueprint(
        pages_bp,
        url_prefix='/',
        template_folder=project_template_folder,
        static_folder=project_static_folder
    )

    mirada_app.logger.info(f'pages blueprint mounted to /')
    mirada_app.logger.info(f'template_folder="{project_template_folder}"')
    mirada_app.logger.info(f'static_folder="{project_static_folder}"')

    mirada_template_folder = os.path.join(MIRADA_PROJ_PATH, 'templates')
    mirada_static_folder = os.path.join(MIRADA_PROJ_PATH, 'static')
    mirada_app.register_blueprint(admin_bp, url_prefix='/_mirada', template_folder=mirada_template_folder, static_folder=mirada_static_folder)

    mirada_app.logger.debug(f'admin mounted to /_mirada')
    mirada_app.logger.debug(f'template_folder="{mirada_template_folder}"')
    mirada_app.logger.debug(f'static_folder="{mirada_static_folder}"')

    return mirada_app


