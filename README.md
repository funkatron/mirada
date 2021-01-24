# Mirada

A web server to make front-end web development easier.

## Motivation

Front-end web development has become a cacophony of complex, brittle tooling. Modern, effective web development with "Plain old HTML, CSS and JS" ("POHCJ") can be relatively straightforward, and __should require little or no tooling__.

Still, any tool is valuable for a project when the advantages make the added complexity wortwhile. Two areas where a tool would be useful in POHCJ:

1. Web browsers have security features in place to limit what can be loaded from the local file system. Having a simple web server that the web browser can make requests to fixes this issue.
2. HTML lacks any kind of code insertion or templating capabilities, which can mean a LOT of repeated code from file to file.

## What Mirada does

Mirada is a Python-based web application meant to be run on your development machine (__never use this in production__). It aims to provide the following features:

1. A simple web server to avoid security constraints on the local filesystem.
2. An easy to use, but full-featured templating system, that allows for dynamic on-request rendering during development.
3. WIP: Ability to write out static files, ready for deployment, with a single command.

## Current limitations

- Files that are not built on the fly must be served from the `/static/` directory and URI path

## Start using Mirada

WIP

### What Goes Where

- `_dist/`: Static builds of sites will be written here.
- `mirada/`: The python application that powers the web server. You can ignore this.
- `static/`: Anything not built from templates should be placed and served from here. This maps to the `/static/` URI path.
- `templates/`: Jinja2 templates to render HTML to the browser when a request is made.
    - `templates/layouts/`: Layouts for the pages to use.
    - `templates/pages/`: Files that content page content.

## Setup for Development _of_ Mirada

WIP. Tested only on MacOS at this time.

1. Install Python (3.7 or later)
2. Clone this repo
3. Open a Terminal window
4. `cd` to the base directory of the repo
5. Run `python3 -m venv ./venv`. Python will create a virtual environment in the `venv/` directory.
6. Run `source ./venv/bin/activate` to activate the virtual environment.
7. Run `pip install -r ./requirements.txt` to install project requirements.
8. Run `flask run`.  It should start the flask dev server on port 5000.
9. Visit http://0.0.0.0:5000.

### Building

1. `cd` to project base
2. Run `source ./venv/bin/activate` to activate the virtual environment.
3. Run `build-mirada-server.sh` (only on MacOS/Unices)
