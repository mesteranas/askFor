import sys
from custome_errors import *
sys.excepthook = my_excepthook
import catagories
import os
import settings_handler
import requests
from bs4 import BeautifulSoup
from winsound import PlaySound
from random import sample,choice
from webbrowser import open as openLink
import language
import app
import PyQt6.QtWidgets as qt
import PyQt6.QtGui as qt1
from PyQt6.QtCore import Qt,QTimer
language.init_translation()
class main (qt.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(app.name + _("version : ") + str(app.version))
        self.qutext=""
        self.timer=QTimer()
        self.trueAnser=None
        self.scor=qt.QLabel(_("scor :0"))
        self.anser=qt.QLabel(_("true ansers:0"))
        self.rong=qt.QLabel(_("false ansers :0"))
        self.rmaining=qt.QLabel(_("remaining time :60"))
        self.qu=qt.QLineEdit()
        self.qu.setAccessibleName(_("question"))
        self.qu.setReadOnly(True)
        self.ansers=qt.QComboBox()
        self.ansers.setAccessibleName(_("select anser"))
        self.sub=qt.QPushButton(_("submit"))
        self.sub.setDefault(True)
        self.sub.clicked.connect(self.fsub)
        self.cat=qt.QPushButton(_("select category"))
        self.cat.setDefault(True)
        self.cat.clicked.connect(lambda:catagories.main(self).exec())
        self.timer.timeout.connect(self.uptime)
        layout=qt.QVBoxLayout()
        layout.addWidget(self.scor)
        layout.addWidget(self.anser)
        layout.addWidget(self.rong)
        layout.addWidget(self.rmaining)
        layout.addWidget(self.qu)
        layout.addWidget(self.ansers)
        layout.addWidget(self.sub)
        layout.addWidget(self.cat)
        w=qt.QWidget()
        w.setLayout(layout)
        self.setCentralWidget(w)
        self.getLink()
        mb=self.menuBar()
        help=mb.addMenu(_("help"))
        cus=help.addMenu(_("contact us"))
        telegram=qt1.QAction("telegram",self)
        cus.addAction(telegram)
        telegram.triggered.connect(lambda:openLink("https://t.me/mesteranasm"))
        telegramc=qt1.QAction(_("telegram channel"),self)
        cus.addAction(telegramc)
        telegramc.triggered.connect(lambda:openLink("https://t.me/tprogrammers"))
        donate=qt1.QAction(_("donate"),self)
        help.addAction(donate)
        donate.triggered.connect(lambda:openLink("https://www.paypal.me/AMohammed231"))
        about=qt1.QAction(_("about"),self)
        help.addAction(about)
        about.triggered.connect(lambda:qt.QMessageBox.information(self,_("about"),_("{} version: {} description: {} developer: {}").format(app.name,str(app.version),app.description,app.creater)))
        self.setMenuBar(mb)
    def updateQu(self):
        try:
            self.rmaining.setText(_("remaining time :60"))
            self.timer.stop()
        except:
            pass
        text=choice(self.qutext.split("\n")).split('":"')
        self.qu.setText(text[0])
        self.trueAnser=text[1]
        text.remove(text[0])
        self.ansers.clear()
        self.ansers.addItems(sample(text,len(text)))
        self.qu.setFocus()
        self.timer.start(1000)
    def fsub(self):
        if self.ansers.currentText()==self.trueAnser:
            self.num(1)
            PlaySound("data/sounds/1.wav",1)
        else:
            self.num(2)
            qt.QMessageBox.information(self,_("info"),_("your anser is false  , the true anser is {}".format(self.trueAnser)))
        self.updateQu()
    def num(self,int1):
        scor=int(self.scor.text().split(":")[1])
        truean=int(self.anser.text().split(":")[1])
        falsean=int(self.rong.text().split(":")[1])
        if int1==1:
            scor=int(scor+3)
            truean=int(truean+1)
        elif int1==2:
            scor=int(scor-1)
            falsean=int(falsean+1)
        elif int1==3:
            scor=int(scor-3)
            falsean=int(falsean+1)
        self.scor.setText(str(_("scor :{}".format(scor))))
        self.anser.setText(str(_("true ansers:{}".format(truean))))
        self.rong.setText(str(_("false ansers :{}".format(falsean))))
    def uptime(self):
        t=int(self.rmaining.text().split(":")[1])
        t-=1
        if t==0:
            self.timer.stop()
            self.rmaining.setText(_("remaining time :60"))
            qt.QMessageBox.information(self,_("alert"),_("the time has been ended you'll go to next question"))
            self.num(3)
            self.updateQu()
        else:
            self.rmaining.setText(str(_("remaining time :{}".format(t))))
    def getLink(self):
        try:
            l=settings_handler.get("g","qu")
            if l=="file":
                with open(os.path.join(os.getenv('appdata'),settings_handler.appName,"ask.ask"),"r",encoding="utf-8") as file:
                    self.qutext=file.read()
            else:
                r=requests.get(l).text
                soup=BeautifulSoup(r, "html.parser")
                self.qutext=soup.find("pre",id="content").getText()
            self.updateQu()
        except Exception as e:
            qt.QMessageBox.information(self,"error",_("server or file error please restart the program and try after 5minutes") + str(e))
            sys.exit()

App=qt.QApplication([])
w=main()
w.show()
App.exec()