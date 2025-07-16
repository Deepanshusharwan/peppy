#!/usr/bin/env bash


# === config ===
APP_NAME="Peppy"
ICON_FILE="assets/peppy.icns"
EXECUTABLE_NAME="peppy"
DESKTOP_FILE="$HOME/.local/share/applications/$APP_NAME.desktop"


# === making the binary ===
echo "Making the binary"

pyinstaller --onedir --clean --strip \
  --optimize=1 \
  --name="$EXECUTABLE_NAME" \
  --windowed \
  --icon="$ICON_FILE" \
  --add-data "src/JetBrainsMonoNerdFont-Bold.ttf:." \
  --add-data "src/utils/app_lister_lib/mac/app_lister.so:." \
  src/main.py
