#!/bin/bash

mkdir -p build

python -m venv ./build/venv
source ./build/venv/bin/activate

pip install --upgrade pip
pip install pyinstaller
pip install ollama openai

cp ./src/demi.py ./src/demi_core.py -t build/

cd build
pyinstaller --clean --onefile --collect-all ollama --collect-all openai --hidden-import demi_core --add-data="demi_core.py:." demi.py

cp dist/demi ../demi
