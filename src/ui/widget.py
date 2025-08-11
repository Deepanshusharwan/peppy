from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QTextEdit, QVBoxLayout,QApplication
from PyQt6.QtGui import QIcon, QFont, QFontDatabase
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtCore import Qt
import subprocess
import requests
import json
import sys
import os

from utils.app_history import increment_app_open_count


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
        increment_app_open_count(self.app_info["exec"])




class WordDictionary(QWidget):
    def __init__(self, word: str):
        super().__init__()
        self.word = word
        self.setWindowTitle(f"Dictionary - {word}")
        self.resize(600, 500)

        layout = QVBoxLayout(self)

        # QTextEdit for displaying formatted text
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setFrameStyle(QTextEdit.Shape.NoFrame)
        self.text_edit.setFont(QFont("Arial", 12))
        self.text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        self.get_word_data(word)

    def get_word_data(self, word):
        r = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        
        try:
            entries = r.json()
        except json.JSONDecodeError:
            self.text_edit.setHtml("<b>Error:</b> Could not parse JSON response.")
            return
        
        if isinstance(entries, dict) and "title" in entries:
            self.text_edit.setHtml(f"<b>Error:</b> {entries.get('message', 'No definition found.')}")
            return
        
        html_content = ""
        # Word heading
        html_content += f"<h1 style='color:white;'>{entries[0].get('word', 'N/A').title()}</h1>"
        html_content += f"<p style='color:#8424e3;'><b>Phonetic:</b> {entries[0].get('phonetic', 'N/A')}</p>"
        
        # Phonetics list
        if entries[0].get("phonetics"):
            html_content += "<p><b>Phonetics:</b></p><ul>"
            for p in entries[0]["phonetics"]:
                text = p.get("text")
                audio = p.get("audio")
                if text:
                    html_content += f"<li>{text}</li>"
                if audio:
                    html_content += f"<li><a href='{audio}' style='color:rgb(36,141,227);'>Audio</a></li>"
            html_content += "</ul>"
            

        for entry in entries:

            # Meanings
            for meaning in entry.get("meanings", []):
                html_content += f"<h3 style='color:darkgreen;'>{meaning.get('partOfSpeech', 'N/A')}</h3>"
                
                if meaning.get("synonyms"):
                    html_content += f"<p><b>Synonyms:</b> {', '.join(meaning['synonyms'])}</p>"
                if meaning.get("antonyms"):
                    html_content += f"<p><b>Antonyms:</b> {', '.join(meaning['antonyms'])}</p>"
                
                for definition in meaning.get("definitions", []):
                    html_content += f"<p style='font-size:14px;'><b>Definition:</b> {definition.get('definition', 'N/A')}</p>"
                    
                    if definition.get("example"):
                        html_content += f"<p style='font-size:11px; font-style:italic; color:gray;'>Example: {definition['example']}</p>"
                    
                    if definition.get("synonyms"):
                        html_content += f"<p><b>Synonyms:</b> {', '.join(definition['synonyms'])}</p>"
                    if definition.get("antonyms"):
                        html_content += f"<p><b>Antonyms:</b> {', '.join(definition['antonyms'])}</p>"
            
            # Source URLs
            if entry.get("sourceUrls"):
                html_content += "<p style='color: rgb(36, 141, 227);'><b>Source URLs:</b></p><ul>"
                for url in entry["sourceUrls"]:
                    html_content += f"<li><a href='{url}' style='color:rgb(36,141,227);'>{url}</a></li>"
                html_content += "</ul>"

        self.text_edit.setHtml(html_content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WordDictionary("hi")
    win.show()
    sys.exit(app.exec())
