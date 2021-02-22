import os

from flask import Blueprint, render_template, request, current_app
from jinja2 import TemplateNotFound

bp = Blueprint(name=__name__, import_name='pages_blueprint')


@bp.route('/', defaults={'path_str': 'index'})
@bp.route('/<path:path_str>')
def render_page(path_str: str = ''):
    # This implements a "catch-all" route that renders HTML pages.
    # URI paths are routed to template pages using this rule:
    #   path/name -> templates/pages/path/name.html

    current_app.logger.debug(f"Got path_str '{path_str}' to render as page.")

    # remove trailing slash, if present
    path_str = path_str.rstrip('/')

    # split out filepath and file extension
    path_str, path_ext = os.path.splitext(path_str)

    # if no oath_ext, use .html for the template
    template_path = f'pages/{path_str}{path_ext or ".html"}'

    full_template_path = os.path.join(current_app.template_folder, template_path)

    current_app.logger.debug(f"Mapping '{path_str}{path_ext}' to template at {full_template_path}")

    try:
        # @TODO we need to make sure path_str is sanitized
        rendered_template = render_template(template_path, request=request)
    except TemplateNotFound as e:
        # @TODO don't inline this. Use a nicer looking template
        rendered_template = f"""
        <!doctype html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
                <meta http-equiv="X-UA-Compatible" content="ie=edge">
                <title>Template Not Found!</title>
            </head>
            <body>
                <h1>Oops</h1>
                <p>We couldn't map the path you gave to a template.</p>
                <strong>path:</strong> {path_str}{path_ext}<br>
                <strong>mapped template path (which I could not find):</strong> {full_template_path}<br>
            </body>
        </html>
        """
        current_app.logger.warning(f"Could not map '{path_str}{path_ext}' to template at {full_template_path}")

    return rendered_template

