from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import QCoreApplication
import subprocess


class OnOffWidget(QWidget):

    def __init__(self,name:str,app_info: dict):
        super().__init__()

        self.name = name # Name of the widget used for searching
        self.app_info = app_info

        self.btn = QPushButton(name) # making the button
        self.btn.setFixedHeight(30)
       
        self.hbox = QHBoxLayout() # a horizontal layout to encapsulate the above
        self.hbox.addWidget(self.btn)
        self.setLayout(self.hbox)
        
        self.btn.clicked.connect(self.launch_application)

    
    def launch_application(self):
        args = self.app_info.get("exec").split()
        subprocess.Popen(args)
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


