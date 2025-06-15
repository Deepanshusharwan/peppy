#!/usr/bin/env bash

# === config ===
APP_NAME="Peppy"
ICON_FILE="peppy.svg"
EXECUTABLE_NAME="peppy"
DESKTOP_FILE="$HOME/.local/share/applications/$APP_NAME.desktop"


git clone "https://github.com/Deepanshusharwan/peppy"

cd peppy || { echo "Failed to enter directory"; exit 1; }

# === Setting up the enviroment ===
python -m venv .venv
source .venv/bin/activate
echo "Current Virtual Enviroment is:"
pip -V
pip install uv
uv pip install .
pip install pyinstaller

# === building the exec ===
if [[ $OSTYPE == "linux-gnu"* ]]; then
  ./linux_build.sh

else
  echo "Looks like your system isn't yet supported by peppy."
  echo "Please create an issue on the below link with you system name and version."
  echo "https://github.com/Deepanshusharwan/peppy/issues/new"
  
fi

# === removing the repo ===
cd ../ 
rm -rf peppy/

echo ""
echo ""
echo "The install is complete!"



