import os
import settings_handler
import requests
from bs4 import BeautifulSoup
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
import language
language.init_translation()
class main (qt.QDialog):
    def __init__(self,p):
        super().__init__(p)
        self.setWindowTitle(_("select category"))
        self.dicr={}
        self.p=p
        self.cat=qt.QComboBox()
        self.cat.setAccessibleName(_("select category"))
        self.online=qt.QPushButton(_("use the category online"))
        self.online.setDefault(True)
        self.online.clicked.connect(self.b1)
        self.file=qt.QPushButton(_("use the category offline"))
        self.file.setDefault(True)
        self.file.clicked.connect(self.b2)
        layout=qt.QVBoxLayout()
        layout.addWidget(self.cat)
        layout.addWidget(self.online)
        layout.addWidget(self.file)
        self.setLayout(layout)
        self.get()
    def get(self):
        r=requests.get("https://mesteranas.github.io/mesteranas/askFor/catagories/index.html").text
        soup=BeautifulSoup(r, "html.parser")
        t=soup.find("pre",id="catagories").getText().split(",")
        for i in t:
            q=i.split('":"')
            self.dicr[q[0].split('"')[1]]=q[1].split('"')[0]
        self.cat.addItems(self.dicr.keys())
    def b1(self):
        settings_handler.set("g","qu",self.dicr[self.cat.currentText()])
        self.p.getLink()
        self.close()
    def b2(self):
        r=requests.get(self.dicr[self.cat.currentText()]).text
        soup=BeautifulSoup(r, "html.parser")
        t=soup.find("pre",id="content").getText()
        with open(os.path.join(os.getenv('appdata'),settings_handler.appName,"ask.ask"),"w",encoding="utf-8") as file:
            file.write(t)
        settings_handler.set("g","qu","file")
        self.p.getLink()
        self.close()


