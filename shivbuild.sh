#!/usr/bin/env bash
rm -rf dist

poetry export -f requirements.txt -o requirements.txt --without-hashes
pip install -r requirements.txt --target dist/

cp -r \
    -t dist \
    utils orts.py main_view.enaml

# finally, build!
shiv \
    --site-packages dist \
    --compressed \
    -p '/usr/bin/env python3' \
    -o orts.pyz \
    -e orts.main
