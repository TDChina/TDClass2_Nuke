import PySide2.QtWidgets as QtGui
from threading import Thread
import subprocess


class platewidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setLayout(QtGui.QVBoxLayout())
        self.setMaximumHeight(360)
        self.setMinimumWidth(400)
        self.runbutton = QtGui.QPushButton()
        self.runbutton.setText("Run")
        self.abutton = QtGui.QPushButton("a")
        self.bbutton = QtGui.QPushButton("b")
        self.resultLabel = QtGui.QLabel('init')
        self.buttonLabel = QtGui.QLabel()
        self.runbutton.clicked.connect(self.runcommand)
        self.abutton.clicked.connect(self.ab)
        self.bbutton.clicked.connect(self.bb)
        self.layout().addWidget(self.runbutton)
        self.layout().addWidget(self.abutton)
        self.layout().addWidget(self.bbutton)
        self.layout().addWidget(self.resultLabel)
        self.layout().addWidget(self.buttonLabel)

    def runcommand(self):
        cmd = ['python', '/Volumes/Seagate/tdclass/TDClass2_Nuke/cases/lesson5/subp.py']
        s = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        t = Thread(target=self.th, args=(s,))
        self.resultLabel.setText('Copy Start!')
        t.start()

    def th(self, s):
        for line in iter(s.stdout.readline, ''):
            if "Finished!" in line:
                self.resultLabel.setText("Copy Finished!")

    def ab(self):
        self.buttonLabel.setText("aaa")

    def bb(self):
        self.buttonLabel.setText("bbb")


w = platewidget()
w.show()
