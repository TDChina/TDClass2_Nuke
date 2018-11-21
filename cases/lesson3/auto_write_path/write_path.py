import os
import re

import nuke
import nukescripts

working_file_pattern = ('/Volumes/Seagate/vfxstorage/project/'
                        '(?P<project>[a-z][a-z0-9]{2})/shots/(?P<sequence>[0-9]{3})/'
                        '(?P<shot>[0-9]{4})/(?P<task_type>[a-z]+)/(?P<full_task>[a-z0-9-]+)/'
                        '(?P=project)_(?P=sequence)_(?P=shot)_(?P=full_task)_v(?P<version_number>[0-9]{3}).nk')

class WritePathPanel(nukescripts.PythonPanel):
    def __init__(self,n):
        nukescripts.PythonPanel.__init__(self,'Auto Write Path')
        self.setMinimumSize(550,160)
        self.rootname = n #n is current nuke script saving path

        self.projectKnob = nuke.String_Knob('proj','Project:')
        self.sequenceKnob = nuke.String_Knob('seq','Sequence:')
        self.sequenceKnob.clearFlag(nuke.STARTLINE)
        self.shotKnob = nuke.String_Knob('shot','Shot:')
        self.shotKnob.clearFlag(nuke.STARTLINE)
        self.taskKnob = nuke.String_Knob('task','Task Type:')
        self.versionKnob = nuke.String_Knob('version','Version:')
        self.versionKnob.clearFlag(nuke.STARTLINE)
        self.formatKnob = nuke.Enumeration_Knob('format','File Type:',['exr', 'jpg', 'mov'])
        self.formatKnob.clearFlag(nuke.STARTLINE)
        self.nameKnob = nuke.String_Knob('name','File Name:')
        self.pathKnob = nuke.File_Knob('path','Write Path:')
        self.formatKnob.setValue('exr')
        
        self.addKnob(self.projectKnob)
        self.addKnob(self.sequenceKnob)
        self.addKnob(self.shotKnob)
        self.addKnob(self.taskKnob)
        self.addKnob(self.versionKnob)
        self.addKnob(self.formatKnob)
        self.addKnob(self.nameKnob)
        self.addKnob(self.pathKnob)

        self.projectKnob.setEnabled(False)
        self.sequenceKnob.setEnabled(False)
        self.shotKnob.setEnabled(False)
        self.taskKnob.setEnabled(False)
        self.versionKnob.setEnabled(False)

        self.info = {}

        self.parseParameters()
        if self.match:
            self.knobChanged(self.formatKnob)

    def parseParameters(self):
        match = re.match(working_file_pattern, self.rootname)
        if match:
            self.info = match.groupdict()
            self.projectKnob.setValue(self.info['project'])
            self.sequenceKnob.setValue(self.info['sequence'])
            self.shotKnob.setValue(self.info['shot'])
            self.taskKnob.setValue(self.info['task_type'])
            self.versionKnob.setValue('v{}'.format(self.info['version_number']))
            self.match = True
        else:
            nuke.message('Unmatch')
            self.match = False
            

    def knobChanged(self,knob):
        if not self.info:
            return
        if knob == self.formatKnob:
            if self.formatKnob.value() == 'mov':
                self.info['resolution'] = 'proxy'
                self.info['file_name'] = os.path.basename(self.rootname).replace('.nk','.mov')
                self.nameKnob.setValue(self.info['file_name'])
            elif self.formatKnob.value() == 'exr':
                self.info['resolution'] = 'fullres'
                self.info['file_name'] = os.path.basename(self.rootname).replace('.nk','.%04d.exr')
                self.nameKnob.setValue(self.info['file_name'])
            elif self.formatKnob.value() == 'jpg':
                self.info['resolution'] = 'ref'
                self.info['file_name'] = os.path.basename(self.rootname).replace('.nk','.%04d.jpg')
                self.nameKnob.setValue(self.info['file_name'])

        if knob == self.nameKnob:
            self.info['file_name'] = self.nameKnob.value()
            
        writepath = ('/Volumes/Seagate/vfxstorage/element/'
                     '{project}/{sequence}/{shot}/{task_type}/{full_task}/v{version_number}/'
                     '{resolution}/{file_name}').format(**self.info)
        self.pathKnob.setValue(writepath)

    def showModalDialog(self):
        result = nukescripts.PythonPanel.showModalDialog(self)
        if result:
            n = nuke.selectedNode()
            write = nuke.nodes.Write()
            write.setInput(0,n)
            write['file'].fromUserText(self.pathKnob.value())
            if not os.path.isdir(os.path.dirname(write['file'].value())):
                os.makedirs(os.path.dirname(write['file'].value()))


def showAutoWritePath():
    n = nuke.root().name()
    if n[-3:] == '.nk':
        w = nuke.selectedNode()
        wp = WritePathPanel(n)
        if wp.match:
            wp.showModalDialog()
    else:
        nuke.message('Nuke script unsaved.')


showAutoWritePath()