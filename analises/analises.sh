#!/bin/bash

set -x  # debug
set -e  # exit on error

python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

ROOT_DIR=${PWD}
    python3 ${ROOT_DIR}/valores_analisados.py