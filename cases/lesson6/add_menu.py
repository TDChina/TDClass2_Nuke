import hiero.core as hcore
from PySide2 import QtWidgets


class TestWidget1(QtWidgets.QWidget):
    def __init__(self):
        super(TestWidget1, self).__init__()
        self.setWindowTitle('Test1')


class TestWidget2(QtWidgets.QWidget):
    def __init__(self):
        super(TestWidget2, self).__init__()
        self.setWindowTitle('Test2')


class NukeStudioMenu(object):
    def __init__(self):
        super(NukeStudioMenu, self).__init__()
        hcore.events.registerInterest("kShowContextMenu/kTimeline", self.create_menu)

    def create_menu(self, event):
        menu = QtWidgets.QMenu('TD')
        menu.addAction('Test1', self.show_test1)
        menu.addAction('Test2', self.show_test2)
        event.menu.addMenu(menu)

    def show_test1(self):
        self.widget1 = TestWidget1()
        self.widget1.show()

    def show_test2(self):
        self.widget2 = TestWidget2()
        self.widget2.show()


NukeStudioMenu()
