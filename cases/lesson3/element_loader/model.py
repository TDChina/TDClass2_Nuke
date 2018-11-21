import os
import re

import nuke

working_file_pattern = ('/Volumes/Seagate/vfxstorage/project/'
                        '(?P<project>[a-z][a-z0-9]{2})/shots/(?P<sequence>[0-9]{3})/'
                        '(?P<shot>[0-9]{4})/(?P<task_type>[a-z]+)/(?P<full_task>[a-z0-9-]+)/'
                        '(?P=project)_(?P=sequence)_(?P=shot)_(?P=full_task)_v(?P<version_number>[0-9]{3}).nk')

project_folder_pattern = '/Volumes/Seagate/vfxstorage/element/{project}/shots'


class ElementLoaderModel(object):
    def __init__(self, n):
        super(ElementLoaderModel, self).__init__()
        self.info = {}
        self.rootname = n

    def parse_context(self):
        match = re.match(working_file_pattern, self.rootname)
        if match:
            self.info = match.groupdict()
            self.match = True
        else:
            nuke.message('Unmatch')
            self.match = False


    def search_sequences(self):
        project_folder = project_folder_pattern.format(project=self.info['project'])
        sequences = [folder for folder in os.listdir(project_folder) if os.path.isdir('{}/{}'.format(project_folder, folder))]
        return sorted(sequences)

    def search_shots(self, sequence):
        project_folder = project_folder_pattern.format(project=self.info['project'])
        shots = [folder for folder in os.listdir('{}/{}'.format(project_folder, sequence)) if os.path.isdir('{}/{}/{}'.format(project_folder, sequence, folder))]
        return sorted(shots)

    def search_task(self, sequence, shot):
        shot_folder = '{}/{}/{}'.format(project_folder_pattern.format(project=self.info['project']), sequence, shot)
        tasks = [folder for folder in os.listdir(shot_folder) if os.path.isdir('{}/{}'.format(shot_folder, folder))]
        return sorted(tasks)

    def search_versions(self, sequence, shot, task):
        task_folder = '{}/{}/{}/{}'.format(project_folder_pattern.format(project=self.info['project']), sequence, shot, task)
        versions = [folder for folder in os.listdir(task_folder) if os.path.isdir('{}/{}'.format(task_folder, folder))]
        return sorted(versions).reverse()

    def search_resolution

