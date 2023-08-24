from . import download
from googletrans import LANGUAGES
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
import language
language.init_translation()
class main (qt.QDialog):
    def __init__(self,p):
        super().__init__(p)
        self.setWindowTitle(_("select questions language"))
        self.lang=qt.QComboBox()
        self.lang.setAccessibleName(_("questions language"))
        lang1=[]
        for code, name in LANGUAGES.items():
            lang1.append(name)
        self.lang.addItems(lang1)
        self.change=qt.QPushButton(_("change language"))
        self.change.setDefault(True)
        self.change.clicked.connect(lambda:download.main(self,self.lang.currentText()).exec())
        layout=qt.QVBoxLayout()
        layout.addWidget(self.lang)
        layout.addWidget(self.change)
        self.setLayout(layout)
