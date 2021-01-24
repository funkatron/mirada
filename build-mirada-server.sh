#!/usr/bin/env bash
pyinstaller \
-c -F \
--add-data "templates:templates" \
--add-data "static:static" \
mirada-server.py \
mirada-server.spec
