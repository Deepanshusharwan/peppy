#!/usr/bin/env python3

import platform
import os
from configparser import ConfigParser


def application_lister():
    operating_system = platform.system()
    app = []

    if operating_system == "Linux":
        home_path = os.environ.get("HOME")
        dir_paths = [
            "/usr/share/applications/",
            f"{home_path}/.local/share/applications",
        ]
        try:
            for dir in dir_paths:
                for file in os.listdir(dir):
                    config = ConfigParser(interpolation=None)
                    if not file.endswith(".desktop"):
                        continue

                    config.read(os.path.join(dir,file),encoding = "utf-8")
                    entry = config["Desktop Entry"]
                    if is_gui_app(entry):
                        app.append(
                            {
                                "name": entry.get("Name"),
                                "icon": entry.get("Icon"),
                                "exec": entry.get("Exec"),
                            }
                        )
        except Exception as e:
            print(f"failed to read {file}: {e}")

    elif operating_system == "Darwin":
        from .mac import app_lister_mac
        app = app_lister_mac.mac_apps
        


    app.sort(key= lambda x : x.get("name").lower())
    return app

def is_gui_app(entry):  # to filter out all the terminal executables from the gui applications
    if entry.get("Type") != "Application":
        return False

    if entry.get("Terminal", "false") == "true":
        return False

    if entry.get("NoDisplay", "false").lower() == "true":
        return False

    if not entry.get("Exec"):
        return False

    return True

if __name__ == "__main__":
    app = application_lister()
    
    for m in app:
        print(m.get("name"))
        print("")
        print(m)
        print("")
        print("")
