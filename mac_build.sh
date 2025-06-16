#!/usr/bin/env bash


# === config ===
APP_NAME="Peppy"
ICON_FILE="peppy.svg"
EXECUTABLE_NAME="peppy"
DESKTOP_FILE="$HOME/.local/share/applications/$APP_NAME.desktop"


# === making the binary ===
echo "Making the binary"
pyinstaller --onefile \
  --name "$EXECUTABLE_NAME" \
  --windowed \
  --icon="$ICON_FILE" \
  --add-data ".venv/lib/python3.13/site-packages/PyQt6/Qt6/plugins/platforms:PyQt6/Qt6/plugins/platforms" \
  src/main.py

