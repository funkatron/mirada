import os

from flask import Flask, jsonify
from flask.templating import render_template
from dotenv import load_dotenv

# get the path to the directory where this file is located
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
PROJ_PATH = os.path.abspath(os.path.join(BASE_PATH, '../'))
load_dotenv(os.path.join(PROJ_PATH, '.env'))


app = Flask(
    __name__,
    template_folder=os.path.join(PROJ_PATH, 'templates'),
    static_folder=os.path.join(PROJ_PATH, 'static'),
)


@app.route('/_ping')
def ping():
    return jsonify({'response': 'pong'})

@app.route('/')
@app.route('/<path:path_str>')
def render_page(path_str: str = ''):
    # This implements a "catch-all" route that renders HTML pages.
    # URI paths are routed to template pages using this rule:
    #   path/name -> templates/pages/path/name.html

    # remove trailing slash, if present
    path_str = path_str.rstrip('/')

    if not path_str:
        # the "empty" path is mapped to 'index'
        path_str = 'index'

    # @TODO we need to make sure path_str is sanitized
    return render_template(f'pages/{path_str}.html')
