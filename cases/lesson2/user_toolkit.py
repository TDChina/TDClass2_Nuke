import getpass
import os

import nuke

from PySide2 import QtCore, QtWidgets

TOOLKIT_ROOT = '/Volumes/Seagate/tdclass/TDClass2_Nuke/cases/lesson2/toolkit'

user_name = getpass.getuser()

def remove_template(template_name):
    root_menu = nuke.menu('Nuke')
    template_menu = root_menu.findItem('Toolkit/{}/{}'.format(user_name, template_name))
    if template_menu:
        template_menu.removeItem(template_name)
        template_menu.removeItem('remove')
        root_menu.removeItem(template_name)
        if os.path.isfile('{}/{}/{}.nk'.format(TOOLKIT_ROOT, user_name, template_name)):
            os.remove('{}/{}/{}.nk'.format(TOOLKIT_ROOT, user_name, template_name))


def add_template(template_name):
    root_menu = nuke.menu('Nuke')
    template_menu = 'Toolkit/{}/{}'.format(user_name, template_name)
    if not root_menu.findItem(template_menu):
        if not os.path.isdir('{}/{}'.format(TOOLKIT_ROOT, user_name)):
            os.makedirs('{}/{}'.format(TOOLKIT_ROOT, user_name))
        nuke.nodeCopy('{}/{}/{}.nk'.format(TOOLKIT_ROOT, user_name, template_name))
        root_menu.addCommand('Toolkit/{}/{}/{}'.format(user_name, template_name, template_name),
                             lambda: nuke.scriptReadFile('{}/{}/{}.nk'.format(TOOLKIT_ROOT,
                                                                              user_name,
                                                                              template_name)))
        root_menu.addCommand('Toolkit/{}/{}/remove'.format(user_name, template_name),
                             lambda: remove_template(template_name))


class AddScriptPanel(QtWidgets.QDialog):
    def __init__(self):
        super(AddScriptPanel, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setMaximumHeight(100)
        self.setMinimumWidth(400)

        self.name_layout = QtWidgets.QHBoxLayout()
        self.tool_name_label = QtWidgets.QLabel('Template Name:')
        self.tool_name_edit = QtWidgets.QLineEdit()
        self.name_layout.addWidget(self.tool_name_label)
        self.name_layout.addWidget(self.tool_name_edit)

        self.button_layout = QtWidgets.QHBoxLayout()
        self.add_button = QtWidgets.QPushButton('Add')
        self.cancel_button = QtWidgets.QPushButton('Cancel')
        self.button_layout.addWidget(self.add_button)
        self.button_layout.addWidget(self.cancel_button)

        self.layout().addLayout(self.name_layout)
        self.layout().addLayout(self.button_layout)

        self.user_name = getpass.getuser()
        self.add_button.clicked.connect(self.add_template)
        self.cancel_button.clicked.connect(self.reject)

    def add_template(self):
        nodes = nuke.selectedNodes()
        if not nodes:
            nuke.message('No nodes been selected.')
            self.reject()
        template_name = self.tool_name_edit.text()
        if not template_name:
            nuke.message('You should input a template name.')
        else:
            add_template(template_name)
            self.tool_name_edit.clear()
            self.accept()

ui = AddScriptPanel()
def run():
    ui.exec_()