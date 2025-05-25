import sys
from PyQt6 import QtWidgets
from ui import Ui_MainWindow  # Rename this if your file is named differently

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Example: connect a button
        self.ui.commandLinkButton.clicked.connect(self.on_button_click)

    def on_button_click(self):
        search_text = self.ui.plainTextEdit.toPlainText()
        print(f"Search text: {search_text}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

