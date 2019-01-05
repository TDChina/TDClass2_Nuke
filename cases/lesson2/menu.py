import copy
import getpass
import os

import nuke

import user_toolkit

menu = nuke.menu('Nuke')
menu.addCommand('Toolkit/Add User Template',
                lambda: user_toolkit.run(),
                'Shift+Alt+R')

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


def add_user_template(menu, root_folder):
    folders = [folder for folder in os.listdir(root_folder) if os.path.isdir('{}/{}'.format(root_folder, folder))]
    for folder in folders:
        templates = [i for i in os.listdir('{}/{}'.format(root_folder, folder)) if i.endswith('.nk')]
        if templates:
            submenu = menu.addMenu(folder)
            for template in templates:
                template_name = copy.deepcopy(os.path.basename(template).split('.')[0])
                submenu.addCommand('{}/{}'.format(template_name, template_name), lambda: nuke.scriptReadFile('{}/{}/{}'.format(root_folder, folder, template)))
                submenu.addCommand('{}/remove'.format(template_name), lambda: remove_template(template_name))
        add_user_template(submenu, '{}/{}'.format(root_folder, folder))

add_user_template(menu.findItem('Toolkit'), TOOLKIT_ROOT)
