from PyQt6.QtWidgets import (
    QWidget, QLineEdit,QTextEdit, QScrollArea, QMainWindow,
    QApplication, QVBoxLayout, QSpacerItem, QSizePolicy,
    )
from PyQt6.QtCore import  Qt
from PyQt6.QtGui import QFont, QFontDatabase
#from PyQt6.QtGui import QKeySequence, QShortcut

import sys
import os

from .widget import AppButton
from utils.command_worker import WorkerThread

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

        #font 
        font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'..','JetBrainsMonoNerdFont-Bold.ttf'))
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        font = QFont(font_family, 10)

        # btn stylesheet 
        self.first_app_stylesheet = '''QPushButton{ text-align: left; padding-left: 9px; border: 2px solid #8a92c5;border-radius:5px; background-color: #1e1e2e; color: #bf9de9; outline:none;}'''
        self.btn_stylesheet = '''QPushButton { border: none;text-align: left; padding-left: 9px }
        QPushButton:hover { background-color: #1e1e2e; color: #bf9de9; outline:none;} 
        QPushButton:focus { border: 2px solid #8a92c5;border-radius:7x; background-color: #1e1e2e; color: #bf9de9; outline:none;}'''

        
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
        self.first_app.btn.setStyleSheet(self.first_app_stylesheet)

        # output area for the shell output
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setFrameStyle(QTextEdit.Shape.NoFrame)
        self.output_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.controlsLayout.addWidget(self.output_area,stretch=1)
        self.output_area.setStyleSheet('padding:9px')
        self.output_area.setFont(font)
        self.output_area.hide()

        # small output area for various functions
        self.display_box = QLineEdit()
        self.display_box.setReadOnly(True)
        self.controlsLayout.addWidget(self.display_box,stretch=1)
        self.display_box.hide()

        end_spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.controlsLayout.addItem(end_spacer)
        self.controls.setLayout(self.controlsLayout)

        # scroll area properties
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        self.scroll.setStyleSheet('''
        Qs
        ''')
        self.scroll.setWidget(self.controls)

        # searchbar
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText("Search application....")
        self.searchbar.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.searchbar.setContentsMargins(10,10,10,0)
        self.searchbar.setStyleSheet('''QLineEdit {padding-left:9px;padding-top:7px;padding-bottom:7px;outline:none;}
        QLineEdit:focus {padding-left:9px;padding-top:7px;padding-bottom:7px;outline:none; border: none;}
        ''')
        font2 = QFont(font_family,12)
        self.searchbar.setFont(font2)
        self.searchbar.textChanged.connect(self.update_display)

        self.setWindowState(Qt.WindowState.WindowNoState)
        self.setFixedSize(900, 400)  # or use self.resize(w, h) if you want it resizable
        self.setStyleSheet("background-color: #1e1e2e; color: #a5aad1")




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
#             self.text_shortcut.activated.connect(self.process_search_input)
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
                self.process_search_input()

        elif event.key() == (Qt.Key.Key_Escape):
            self.close()

        # FIXIT this keyPressEvent doesn't work currently for some unknown reasons
        elif event.key() == Qt.Key.Key_C and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
           if hasattr(self, 'worker') and self.worker:
               self.worker.stop()
               self.output_area.append("<span style='color:red'>[Process terminated with Ctrl+C]</span>")
                           
        elif self.searchbar.hasFocus():
            if event.key() == (Qt.Key.Key_Down): # changes the focus from searchbar to scrollarea to the widgets
                self.focusNextChild()
                self.focusNextChild()
                self.first_app.btn.setStyleSheet(self.btn_stylesheet)
            elif event.key() == Qt.Key.Key_Up:
                self.focusPreviousChild()

        elif self.scroll.hasFocus():
            self.searchbar.setFocus()
            QApplication.sendEvent(self.searchbar,event)
            
        elif event.key() == Qt.Key.Key_Up:
            self.focusPreviousChild()

        elif event.key() == Qt.Key.Key_Up:
            if self.first_app.hasFocus():
                self.searchbar.setFocus()

        elif event.key() == Qt.Key.Key_Shift:
            pass

        else:
            self.searchbar.setFocus()
            QApplication.sendEvent(self.searchbar,event)


    def update_display(self,text):
        if self.first_app:
            self.first_app.btn.setStyleSheet(self.btn_stylesheet)
        self.first_app = None
        self.visible_widgets = []

        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                if self.first_app is None:
                    self.first_app = widget
                    self.first_app.btn.setStyleSheet(self.first_app_stylesheet)
                widget.show()
                self.visible_widgets.append(widget)
                self.display_box.hide()
                self.output_area.hide()
            else:
                widget.hide()

    def process_search_input(self):
        if self.first_app:
            self.first_app.launch_application()

        elif self.searchbar.text().strip().startswith('/'): # for commands
            command = self.searchbar.text().strip().removeprefix('/').strip()
            self.output_area.append(f"<span style='color:green'>$ {command}</span>")

            self.output_area.show()
            self.worker = WorkerThread(command)
            self.worker.output_signal.connect(self.display_shell_output)
            self.worker.error_signal.connect(self.display_shell_error)
            self.worker.finished_signal.connect(self.on_shell_finished)
            self.worker.start()

        elif self.searchbar.text().strip().startswith('#'): # for colour codes
            colour = self.searchbar.text().strip()

            if "rgb" in self.searchbar.text().lower():
                colour = colour.removeprefix('#')
                # TODO add a regex to check if the hex and rgb colours are valid 
            else:
                colour_split = colour.split()
                colour = ''
                for m in colour_split:
                    colour +=m

            self.display_box.show()
            self.display_box.setStyleSheet('background-color: #ffffff;')
            #self.display_box.setText(f"Invalid colour {colour}")  # TODO this text should appear when the 

            self.display_box.setStyleSheet(f"background-color: {colour};")

    def display_shell_output(self, output: str):
        self.output_area.append(output)

    def display_shell_error(self, error: str):
        self.output_area.append(f"<span style='color:red'>{error}</span>")

    def on_shell_finished(self):
        self.worker = None
        self.searchbar.setText('/ ')

#    def change_placeholder(self):
#        self.searchbar.setPlaceholderText("changed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


