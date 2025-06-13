from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout

class OnOffWidget(QWidget):

    def __init__(self,name):
        super().__init__()

        self.name = name # Name of the widget used for searching
        self.is_on = False # current state (ON,OFF)

        self.lbl = QLabel(self.name)
        self.btn_on = QPushButton("ON")
        self.btn_off = QPushButton("OFF")
        
        self.hbox = QHBoxLayout() # a horizontal layout to encapsulate the above
        self.hbox.addWidget(self.lbl) # add the label to the layout
        self.hbox.addWidget(self.btn_on)
        self.hbox.addWidget(self.btn_off)
        self.setLayout(self.hbox)

        self.btn_off.clicked.connect(self.off)
        self.btn_on.clicked.connect(self.on)
        self.update_button_state()

    
    def off(self):
        self.is_on = False
        self.update_button_state()

    def on(self):
        self.is_on = True
        self.update_button_state()

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


