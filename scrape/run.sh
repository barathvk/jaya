#!/usr/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
source bin/activate; python scrape.py; deactivate
