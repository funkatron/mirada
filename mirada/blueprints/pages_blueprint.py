from flask import Blueprint, render_template

bp = Blueprint(name=__name__, import_name='pages_blueprint')


@bp.route('/', defaults={'path_str': 'index'})
@bp.route('/<path:path_str>')
def render_page(path_str: str = ''):
    # This implements a "catch-all" route that renders HTML pages.
    # URI paths are routed to template pages using this rule:
    #   path/name -> templates/pages/path/name.html

    # remove trailing slash, if present
    path_str = path_str.rstrip('/')

    # @TODO we need to make sure path_str is sanitized
    return render_template(f'pages/{path_str}.html')
