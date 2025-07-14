from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QIcon, QFont, QFontDatabase
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtCore import Qt
import subprocess
import os


class AppButton(QWidget):

    def __init__(self,name:str,app_info: dict):
        super().__init__()

        self.name = name # Name of the widget used for searching
        self.app_info = app_info

        self.btn = QPushButton(text = name)
        # self.btn = QPushButton(text = name, icon=QIcon(app_info.get('icon')))
        self.btn.setFixedHeight(35)
        
        font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','JetBrainsMonoNerdFont-Bold.ttf'))
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 11)
        self.btn.setFont(font)
        self.hbox = QHBoxLayout() # a horizontal layout to encapsulate the above
        self.hbox.addWidget(self.btn)
        self.setLayout(self.hbox)
        
        self.btn.pressed.connect(self.launch_application)


    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.launch_application()
        else:
            super().keyPressEvent(event)

    
    def launch_application(self):
        args = self.app_info.get("exec")
        desktop_exec_field_codes = [
    "%f",  # single file
    "%F",  # multiple files
    "%u",  # single URL
    "%U",  # multiple URLs
    "%i",  # icon placeholder (e.g., expands to --icon <icon>)
    "%c",  # application name
    "%k",  # path to the .desktop file itself
]
        for m in desktop_exec_field_codes:
            if m in args:
                args = args.replace(m,"")
        print(args)
        subprocess.Popen(args,
                         shell=True,
                         text=True)
        QCoreApplication.quit()


    def update_button_state(self):
        """
        update the appearance of the control buttons (On/Off)
        """
        if self.is_on:
            self.btn_on.setStyleSheet("background-color:  #4CAF50; color: #fff;")
            self.btn_off.setStyleSheet("background-color: none; color: none;")

        else:
            self.btn_on.setStyleSheet("background-color: none; color: none;")
            self.btn_off.setStyleSheet("background-color: #D32F2F; color: #fff;")



