#!/usr/bin/env python3
import sys
from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QLabel, QPushButton, QScrollArea, QMainWindow,
    QApplication, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
    )


#from src.utils import app_lister
from utils import app_lister

# from ui import main_window
from ui.main_window import MainWindow, QApplication


apps = app_lister.application_lister()

app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())
