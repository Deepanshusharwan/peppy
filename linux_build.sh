#!/usr/bin/env bash

pyinstaller --onefile \
  --name peppy \
  --windowed \
  --icon=peppy.svg \
  --add-data ".venv/lib/python3.13/site-packages/PyQt6/Qt6/plugins/platforms:PyQt6/Qt6/plugins/platforms" \
  src/main.py
