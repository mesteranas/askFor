import threading
import os
import settings_handler
from googletrans import Translator
from bs4 import BeautifulSoup
import requests
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt
import language
language.init_translation()
class main (qt.QDialog):
    def __init__(self,p,language):
        super().__init__(p)
        self.setWindowTitle(_("translating"))
        self.s=language
        self.z=qt.QLineEdit()
        self.z.setAccessibleName(_("translating"))
        self.z.setReadOnly(True)
        self.z.setText(_("translating questions "))
        lat=qt.QVBoxLayout()
        lat.addWidget(self.z)
        self.setLayout(lat)
        self.q()

    def q(self):
        try:
            l=settings_handler.get("g","qu")
            if l=="file":
                with open(os.path.join(os.getenv('appdata'),settings_handler.appName,"ask.ask"),"r",encoding="utf-8") as file:
                    qutext=file.read()
            else:
                r=requests.get(l).text
                soup=BeautifulSoup(r, "html.parser")
                qutext=soup.find("pre",id="content").getText()
            translator = Translator()
            From=translator.detect(qutext).lang
            ss=self.split_text_into_lists(qutext,20)
            a=[]
            for i in ss:
                a.append(translator.translate(i,src=From,dest=self.s).text.replace('": "','":"'))
            with open(os.path.join(os.getenv('appdata'),settings_handler.appName,"ask.ask"),"w",encoding="utf-8") as file:
                file.write("""
                           """.join(a))
            settings_handler.set("g","qu","file")
        except Exception as e:
            qt.QMessageBox.information(self,"error",_("server or file error please restart the program and try after 5minutes") + str(e))
    def split_text_into_lists(self,text, lines_per_list):
        lines = text.split('\n')
        lists = [lines[i:i+lines_per_list] for i in range(0, len(lines), lines_per_list)]
        l=[]
        for i in lists:
            l.append("\n".join(i))
        return l

