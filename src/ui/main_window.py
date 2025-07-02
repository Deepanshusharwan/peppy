from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QScrollArea, QMainWindow,
    QApplication, QVBoxLayout, QSpacerItem, QSizePolicy
    )
from PyQt6.QtCore import  Qt

import sys

from .widget import OnOffWidget

class MainWindow(QMainWindow):

    def __init__(self,applications,*args, **kwargs):
        super().__init__(*args,**kwargs)

        self.apps = applications # list of applications in the format
        # [  {name: xxx, icon: xxx, exec: xxx},
        #    {name2: xxx, icon2:xxx, exec2: xxx}  ]

        self.controls = QWidget() # controls container widget
        self.controlsLayout = QVBoxLayout() # controls container layout
        self.controlsLayout.setSpacing(0)
        self.controlsLayout.setContentsMargins(0, 0, 0, 0)

        self.widgets = []

        #iterate thee names, creating a new OnOffWidget for 
        # each one, adding it to the layoout and
        # storing a reference in the self.widgets dict
        first_app = None
        count = 0
        for count in range(len(self.apps)):
            app_info = self.apps[count]
            name = app_info.get('name')
            if count == 0:
                first_app = app_info.get(name)
                count += 1

            item = OnOffWidget(name,app_info)
            self.controlsLayout.addWidget(item)
            self.widgets.append(item)

        end_spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.controlsLayout.addItem(end_spacer)
        self.controls.setLayout(self.controlsLayout)

        # scroll area properties
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.controls)

        # searchbar
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search application....")
        self.searchbar.textChanged.connect(self.update_display)

        self.setFixedSize(900, 400)  # or use self.resize(w, h) if you want it resizable


        # TODO make the completer suggestions for autocompletion and display them as the
        # placeholder text in searchbar and pressing tab for autocompletion

        # adding the autocompleter
        #self.completer = QCompleter(widget_names)
        #self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        
        #add the items to vboxlayout (applied to the container widget)
        # which encompasses the whole window
        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.setSpacing(20)
        containerLayout.addWidget(self.searchbar)
        containerLayout.addWidget(self.scroll)
        container.setLayout(containerLayout)

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        self.setWindowTitle("Peppy")       

    def update_display(self,text):

        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                widget.show()
            else:
                widget.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

