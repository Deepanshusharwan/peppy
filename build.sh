#!/usr/bin/env bash

# === config ===
APP_NAME = "Peppy"
ICON_FILE = "peppy.svg"
EXECUTABLE_NAME = "peppy"
DESKTOP_FILE = "/usr/share/applications/"

git clone "https://github.com/Deepanshusharwan/peppy"

cd peppy/

# === Setting up the enviroment ===
python -m venv .venv
source .venv/bin/activate
echo "Current Virtual Enviroment is:"
pip -V
pip install uv
uv pip install .
pip install pyinstaller

# === building the exec ===
if [[ $OSTYPE == "linux-gnu" ]]; then
  ./linux_build.sh

else
  command
  
fi


