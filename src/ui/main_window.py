from PyQt6.QtWidgets import (
    QWidget, QLineEdit, QScrollArea, QMainWindow,
    QApplication, QVBoxLayout, QSpacerItem, QSizePolicy,
    )
from PyQt6.QtCore import  Qt
#from PyQt6.QtGui import QKeySequence, QShortcut

import sys
import shlex
import subprocess

from .widget import AppButton

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

        #iterate the names, creating a new AppButton for 
        # each one, adding it to the layoout and
        # storing a reference in the self.widgets dict
        self.first_app = None
        count = 0
        for count in range(len(self.apps)):
            app_info = self.apps[count]
            name = app_info.get('name')
            item = AppButton(name,app_info)
            item.btn.setFocusPolicy(Qt.FocusPolicy.WheelFocus)
            if count == 0:
                self.first_app = item
                count += 1

            self.controlsLayout.addWidget(item)
            self.widgets.append(item)
        self.visible_widgets = self.widgets.copy()

        end_spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.controlsLayout.addItem(end_spacer)
        self.controls.setLayout(self.controlsLayout)

        # scroll area properties
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.scroll.setWidget(self.controls)

        # searchbar
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search application....")
        self.searchbar.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.searchbar.textChanged.connect(self.update_display)

        self.setWindowState(Qt.WindowState.WindowNoState)
        self.setFixedSize(900, 400)  # or use self.resize(w, h) if you want it resizable


        # TODO make the completer suggestions for autocompletion and display them as the
        # placeholder text in searchbar and pressing tab for autocompletion

        # adding the autocompleter
        #self.completer = QCompleter(widget_names)
        #self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        
        # shortcuts
        # window_close_key = QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_M)
        # self.shortcut = QShortcut(window_close_key, self)
        # self.shortcut.activated.connect(self.change_placeholder)
#             self.window_close_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
#             self.window_close_shortcut.activated.connect(self.close)
#     
#             self.text_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return),self.searchbar) # to open the top app
#             self.text_shortcut.activated.connect(self.launch_top_result)
#     
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


    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if self.searchbar.hasFocus():
                self.launch_top_result()

        elif event.key() == (Qt.Key.Key_Escape):
            self.close()
            
        elif self.searchbar.hasFocus():
            if event.key() == (Qt.Key.Key_Down): # changes the focus from searchbar to scrollarea to the widgets
                self.focusNextChild()
                self.focusNextChild()
            elif event.key() == Qt.Key.Key_Up:
                self.focusPreviousChild()
                
        elif self.scroll.hasFocus():
            self.searchbar.setFocus()
            
        elif event.key() == Qt.Key.Key_Up:
            self.focusPreviousChild()

        elif event.key() == Qt.Key.Key_Shift:
            pass

        elif event.key() == Qt.Key.Key_Up:
            if self.first_app.hasFocus():
                self.searchbar.setFocus()

        else:
            self.searchbar.setFocus()
            QApplication.sendEvent(self.searchbar,event)


    def update_display(self,text):
        self.first_app = None
        self.visible_widgets = []

        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                if self.first_app is None:
                    self.first_app = widget
                widget.show()
                self.visible_widgets.append(widget)
            else:
                widget.hide()

    def launch_top_result(self):
        if self.first_app:
            self.first_app.launch_application()
        else:
            command = shlex.split(self.searchbar.text(),posix=True)
            subprocess.Popen(command)


#    def change_placeholder(self):
#        self.searchbar.setPlaceholderText("changed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

