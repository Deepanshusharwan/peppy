#!/usr/bin/env python3

import os
import sys
import subprocess
#from src.utils import app_lister
from utils import app_lister

apps = app_lister.application_lister()
for m in apps:
    print(m.get("name"))
    print("")
print(apps)
