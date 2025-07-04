#!/usr/bin/env python3
import sys


#from src.utils.app_lister_lib import app_lister
from utils.app_lister_lib import app_lister

# from ui import main_window
from ui.main_window import MainWindow, QApplication


apps = app_lister.application_lister()

app = QApplication(sys.argv)
w = MainWindow(apps)
w.show()
sys.exit(app.exec())
