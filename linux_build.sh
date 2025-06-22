#!/usr/bin/env bash


# === config ===
APP_NAME="Peppy"
ICON_FILE="peppy.svg"
EXECUTABLE_NAME="peppy"
DESKTOP_FILE="$HOME/.local/share/applications/$APP_NAME.desktop"


# === making the binary ===
echo "Making the binary"
# old pyinstaller command
#pyinstaller --onefile \
#  --name "$EXECUTABLE_NAME" \
#  --windowed \
#  --icon="$ICON_FILE" \
#  --add-data ".venv/lib/python3.13/site-packages/PyQt6/Qt6/plugins/platforms:PyQt6/Qt6/plugins/platforms" \
#  src/main.py

pyinstaller --onedir --clean --strip \
  --optimize=1 \
  --name="$EXECUTABLE_NAME" \
  --windowed \
  --icon="$ICON_FILE" \
  src/main.py

# === binary installation ===
echo "installing the binary"
mkdir -p "$HOME/.local/share/"
cp -r "dist/$EXECUTABLE_NAME" "$HOME/.local/share/"

#create a symbolic link of peppy exec in .local/bin/
mkdir -p "$HOME/.local/bin/"
ln -s "$HOME/.local/share/peppy/peppy" "$HOME/.local/bin/peppy"

# === .desktop file ===
echo "Creating .desktop file..."
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=$APP_NAME
GenericName=Application Launcher
Comment=Made with love and experiments
Exec=$HOME/.local/share/peppy/peppy
Icon=$HOME/.local/share/icons/$ICON_FILE
Terminal=false
Categories=Utility;System;
EOF


# === Install icon ===
echo "Installing icon..."
mkdir -p "$HOME/.local/share/icons"
cp "$ICON_FILE" "$HOME/.local/share/icons/"


# === Make .desktop file executable ===
chmod +x "$DESKTOP_FILE"

