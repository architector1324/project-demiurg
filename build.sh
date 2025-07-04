#!/bin/bash

mkdir -p build

python -m venv ./build/venv
source ./build/venv/bin/activate

pip install --upgrade pip
pip install pyinstaller
pip install ollama openai

cp ./src/srge.py ./src/srge_core.py -t build/

cd build
pyinstaller --clean --onefile --collect-all ollama --collect-all openai --hidden-import srge_core --add-data="srge_core.py:." srge.py

cp dist/srge ../srge
