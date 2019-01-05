from PySide2 import QtCore
from PySide2 import QtWidgets

# import generate_tag
# import get_selection
# import parse_trackitem
# import directory_folder
# import update_shotgun_element
# import render_process
# 
# import subprocess
# from threading import Thread


class PlateIngestionUI(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PlateIngestionUI, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setMinimumHeight(600)
        self.setFixedWidth(550)
        self.setWindowTitle("Plate Ingestion")

        self.showNameLabel = QtWidgets.QLabel("Project Name:")
        self.showNameEdit = QtWidgets.QLineEdit()
        self.showTypeLabel = QtWidgets.QLabel("Project Type:")
        self.showTypeList = QtWidgets.QComboBox()
        self.showTypeList.addItems(["Feature Film", "TV Series", "Commercial"])
        self.showLayout = QtWidgets.QHBoxLayout()
        self.showLayout.addWidget(self.showNameLabel)
        self.showLayout.addWidget(self.showNameEdit)
        self.showLayout.addWidget(self.showTypeLabel)
        self.showLayout.addWidget(self.showTypeList)

        self.episodeLabel = QtWidgets.QLabel("Episode:")
        self.episodeEdit = QtWidgets.QLineEdit()
        self.seqLabel = QtWidgets.QLabel("Sequence:")
        self.seqEdit = QtWidgets.QLineEdit()
        self.fromLabel = QtWidgets.QLabel("From:")
        self.fromEdit = QtWidgets.QLineEdit("0010")

        self.stepLabel = QtWidgets.QLabel("Step:")
        self.stepEdit = QtWidgets.QLineEdit("10")
        self.tagInfoLayout = QtWidgets.QHBoxLayout()
        self.tagInfoLayout.addWidget(self.episodeLabel)
        self.tagInfoLayout.addWidget(self.episodeEdit)
        self.tagInfoLayout.addWidget(self.seqLabel)
        self.tagInfoLayout.addWidget(self.seqEdit)
        self.tagInfoLayout.addWidget(self.fromLabel)
        self.tagInfoLayout.addWidget(self.fromEdit)
        self.tagInfoLayout.addWidget(self.stepLabel)
        self.tagInfoLayout.addWidget(self.stepEdit)

        self.tagButton = QtWidgets.QPushButton("Generate Tag")
        self.tagTextButton = QtWidgets.QPushButton("Tag From Text")
        self.shotcodeLayout = QtWidgets.QHBoxLayout()
        self.shotcodeLayout.addWidget(self.tagButton)
        self.shotcodeLayout.addWidget(self.tagTextButton)

        self.shotCodeForm = QtWidgets.QTableWidget(0, 2)
        self.shotCodeForm.setHorizontalHeaderLabels(["Shot Code", "Status"])
        self.shotCodeForm.setColumnWidth(0, 254)  # set shot number column's width
        self.shotCodeForm.setColumnWidth(1, 254)

        self.shotInfoButton = QtWidgets.QPushButton("Shot Edit Info")
        self.tag_key_label = QtWidgets.QLabel("Tag Name:")
        self.tag_key_edit = QtWidgets.QLineEdit()
        self.tag_value_label = QtWidgets.QLabel("Tag Value:")
        self.tag_value_edit = QtWidgets.QLineEdit()
        self.add_tag_button = QtWidgets.QPushButton("Update")
        self.tag_layout = QtWidgets.QHBoxLayout()
        self.tag_layout.addWidget(self.shotInfoButton)
        self.tag_layout.addWidget(self.tag_key_label)
        self.tag_layout.addWidget(self.tag_key_edit)
        self.tag_layout.addWidget(self.tag_value_label)
        self.tag_layout.addWidget(self.tag_value_edit)
        self.tag_layout.addWidget(self.add_tag_button)

        self.fpsLabel = QtWidgets.QLabel("FPS:")
        self.fpsList = QtWidgets.QComboBox()
        self.fpsList.addItems(['24', '25'])
        self.fpsList.setFixedWidth(80)
        self.fpsList.setCurrentIndex(1)
        self.watermarkLabel = QtWidgets.QLabel("Watermark Place:")
        self.watermarkLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.watermarkLabel.setFixedWidth(140)
        self.watermarkPlace = QtWidgets.QComboBox()
        self.watermarkPlace.addItems(["Left Top", "Left Bottom", "Right Top", "Right Bottom"])
        self.watermarkPlace.setFixedWidth(120)
        self.watermarkButton = QtWidgets.QPushButton("Render Demo")
        self.watermarkButton.setFixedWidth(120)

        self.watermarkLayout = QtWidgets.QHBoxLayout()
        self.watermarkLayout.addWidget(self.fpsLabel)
        self.watermarkLayout.addWidget(self.fpsList)
        self.watermarkLayout.addWidget(self.watermarkLabel)
        self.watermarkLayout.addWidget(self.watermarkPlace)
        self.watermarkLayout.addWidget(self.watermarkButton)

        self.shotSnapButton = QtWidgets.QPushButton("Shot Snap")
        self.elementSnapButton = QtWidgets.QPushButton("Element Snap")
        self.editInfoButton = QtWidgets.QPushButton("Element Edit Info")
        self.shotInfoLayout = QtWidgets.QHBoxLayout()
        self.shotInfoLayout.addWidget(self.shotSnapButton)
        self.shotInfoLayout.addWidget(self.elementSnapButton)
        self.shotInfoLayout.addWidget(self.editInfoButton)

        self.headHandleLabel = QtWidgets.QLabel("Head Handle:")
        self.headHandleEdit = QtWidgets.QLineEdit("10")
        self.tailHandleLabel = QtWidgets.QLabel("Tail Handle:")
        self.tailHandleEdit = QtWidgets.QLineEdit("10")
        self.versionLabel = QtWidgets.QLabel('Version:')
        self.versionEdit = QtWidgets.QLineEdit("v001")
        self.copyButton = QtWidgets.QPushButton("Copy Plate")
        self.copyLayout = QtWidgets.QHBoxLayout()
        self.copyLayout.addWidget(self.headHandleLabel)
        self.copyLayout.addWidget(self.headHandleEdit)
        self.copyLayout.addWidget(self.tailHandleLabel)
        self.copyLayout.addWidget(self.tailHandleEdit)
        self.copyLayout.addWidget(self.versionLabel)
        self.copyLayout.addWidget(self.versionEdit)
        self.copyLayout.addWidget(self.copyButton)

        self.plateInfoButton = QtWidgets.QPushButton("Element Plate Info")
        self.retimeInfoButton = QtWidgets.QPushButton("Generate Retime Info")
        self.cutInfoButton = QtWidgets.QPushButton("Generate Cut Info")
        self.infoLayout = QtWidgets.QHBoxLayout()
        self.infoLayout.addWidget(self.plateInfoButton)
        self.infoLayout.addWidget(self.retimeInfoButton)
        self.infoLayout.addWidget(self.cutInfoButton)

        self.msgBox = QtWidgets.QMessageBox()

        self.messageLabel = QtWidgets.QLabel()

        self.layout().addLayout(self.showLayout)
        self.layout().addLayout(self.tagInfoLayout)
        self.layout().addLayout(self.shotcodeLayout)
        self.layout().addWidget(self.messageLabel)
        self.layout().addWidget(self.shotCodeForm)
        self.layout().addLayout(self.tag_layout)
        self.layout().addLayout(self.watermarkLayout)
        self.layout().addLayout(self.shotInfoLayout)
        self.layout().addLayout(self.copyLayout)
        self.layout().addLayout(self.infoLayout)

        self.showTypeList.currentIndexChanged.connect(self.unlock_episode_setting)
        # self.tagButton.clicked.connect(self.generate_tag)
        # self.tagTextButton.clicked.connect(self.tag_from_text)
        # self.watermarkButton.clicked.connect(self.pre_render_demo)
        # self.shotSnapButton.clicked.connect(lambda: self.pre_snap("shot"))
        # self.elementSnapButton.clicked.connect(lambda: self.pre_snap("element"))
        # self.shotInfoButton.clicked.connect(self.generate_shot_info)
        # self.editInfoButton.clicked.connect(self.generate_element_edit_info)
        # self.copyButton.clicked.connect(self.pre_copy)
        # self.plateInfoButton.clicked.connect(self.generate_element_plate_info)
        # self.retimeInfoButton.clicked.connect(self.computing_retime)
        # self.cutInfoButton.clicked.connect(self.generate_cut_info)
        # self.add_tag_button.clicked.connect(self.add_tag)

        self.element_dict = {}
        self.shot_dict = {}

    def show_message(self, message):
        self.msgBox.setText(message)
        self.msgBox.exec_()
    # 
    def unlock_episode_setting(self):
        if self.showTypeList.currentText() == "TV Series":
            self.episodeLabel.setEnabled(True)
            self.episodeEdit.setEnabled(True)
            self.fpsList.setCurrentIndex(1)
        else:
            self.episodeLabel.setEnabled(False)
            self.episodeEdit.setEnabled(False)
            self.fpsList.setCurrentIndex(0)

    def set_shotcode_list(self, trackitems):
        for trackitem in trackitems:
            rowCount = self.shotCodeForm.rowCount()
            self.shotCodeForm.insertRow(rowCount)  # insert one row for current trackitem
            for i in trackitem.tags():
                if "plate" in i.note():  # parse sequence and shot information
                    try:
                        platetag = i.note().split(" ")[1]
                        seq = platetag.split("#")[1]
                        shot = platetag.split("#")[2]
                        type = platetag.split("#")[3].rstrip("\n").rstrip(" ")
                    except:
                        self.shotCodeForm.setItem(rowCount, 0, QtWidgets.QTableWidgetItem("plate tag missing"))
                    self.shotCodeForm.setItem(rowCount, 0,
                                              QtWidgets.QTableWidgetItem("%s %s %s" % (seq, shot, type)))
                else:
                    self.shotCodeForm.setItem(rowCount, 0, QtWidgets.QTableWidgetItem("plate tag missing"))
    # 
    # def check_duplicate(self):
    #     flag = True
    #     tags = []
    #     for i in range(self.shotCodeForm.rowCount()):
    #         try:
    #             tag = str(self.shotCodeForm.item(i, 0).text())
    #             tags.append(tag)
    #         except:
    #             self.show_message("You haven\'t generate tags.")
    #             return False
    #     tags.sort()
    #     for i in range(len(tags) - 1):
    #         if tags[i] == tags[i + 1]:
    #             print tags[i]
    #             self.messageLabel.setText("Duplicate tags founded, please check.")
    #             flag = False
    #             break
    #     return flag
    # 
    # def check_gui_input(self):
    #     if str(self.seqEdit.text()) == "" or str(self.fromEdit.text()) == "" or str(self.stepEdit.text()) == "":
    #         self.show_message('shot information missing.\n please check edit fields.')
    #         return False
    #     elif self.showTypeList.currentText() == "TV series" and str(self.episodeEdit.text()) == "":
    #         self.show_message('shot information missing.\n please check edit fields.')
    #         return False
    #     else:
    #         return True
    # 
    # def create_shot(self):
    #     self.Finished_Count = 0
    #     self.Failed_Count = 0
    #     reload(sgCreater)
    #     if self.check_gui_input() and self.check_duplicate():
    #         self.messageLabel.setText("Start creating shots on shotgun ......")
    #         try:
    #             show = str(self.showNameEdit.text()).upper()
    #             sequence = str(self.seqEdit.text())
    #             if self.showTypeList.currentText() == "TV Series":
    #                 episode = str(self.episodeEdit.text())
    #             create_shot_dicts = []
    #             for i in range(0, self.shotCodeForm.rowCount()):
    #                 shot = str(self.shotCodeForm.item(i, 0).text().split(" ")[1])
    #                 shot_dict = dict(show=show, sequence=sequence, shot=shot, episode=episode)
    #                 create_shot_dicts.append(shot_dict)
    #             create_shot_thread = Thread(target=self.create_shot_process, args=(create_shot_dicts,))
    #             create_shot_thread.setDaemon(True)
    #             create_shot_thread.start()
    #             finishedStatusThread = Thread(target=self.finished_status, args=())
    #             finishedStatusThread.setDaemon(True)
    #             finishedStatusThread.start()
    #         except:
    #             self.show_message('shot information wrong.\n please check edit fields.')
    # 
    # def create_shot_process(self, shot_dicts):
    #     for i in range(0, len(shot_dicts)):
    #         try:
    #             sgCreater.createSGshot(**shot_dicts[i])
    #             self.setResultItem(i, "create shot successfully")
    #             self.Finished_Count += 1
    #         except:
    #             self.setResultItem(i, "create shot failed")
    #             self.Failed_Count += 1
    # 
    # def generate_demo_folder_path(self):
    #     show = str(self.showNameEdit.text())
    #     return "%s/%s/editorial/edit_client" % (config.ws, show)
    # 
    # def pre_render_demo(self):
    #     reload(render_process)
    #     if self.check_gui_input() and self.check_duplicate():
    #         demo_saving_dialog = QtWidgets.QFileDialog()
    #         demo_saving_dialog.setDirectory(self.generate_demo_folder_path())
    #         demo_saving_path = str(demo_saving_dialog.getSaveFileName(filter=".mov")[0])
    #         demo_saving_folder = os.path.dirname(demo_saving_path)
    #         if not render_process.create_temp_folder(demo_saving_folder):
    #             self.messageLabel.setText("Can't create destination folder.")
    #             return False
    #     temp_path = "%s/temp" % demo_saving_folder
    #     if render_process.copy_ffmpeg(temp_path):
    #         self.messageLabel.setText("Start rendering, please wait......")
    #         self.renderDemoThread = Thread(target=self.render_demo_process, args=(temp_path, demo_saving_path,))
    #         self.renderDemoThread.setDaemon(True)
    #         self.renderDemoThread.start()
    # 
    # def render_demo_process(self, temp_path, demo_saving_path):
    #     f = open("%s/shotcode.ass" % temp_path, 'r')
    #     ass_template = f.readlines()
    #     f.close()
    #     part_count = 1
    #     fps = float(self.fpsList.currentText())
    #     position = str(self.watermarkPlace.currentText()).split(" ")[0][0] + \
    #                str(self.watermarkPlace.currentText()).split(" ")[1][0]
    #     log = open("%s/log.txt" % temp_path, 'a')
    #     show = str(self.showNameEdit.text())
    #     ep = str(self.episodeEdit.text())
    #     try:
    #         for trackitem in self.trackitems:
    #             clip_source = trackitem.source().mediaSource().metadata().value('foundry.source.fullpath')
    #             start_time = hieroCore.Timecode.framesToHMSF(trackitem.sourceIn(), int(fps), 0)
    #             start_second = start_time[0] * 3600.0 + start_time[1] * 60.0 + float(start_time[2]) + float(
    #                 start_time[3]) / fps
    #             duration = int(trackitem.sourceOut() - trackitem.sourceIn() + 1)
    #             ass_frame = 0
    #             in_time = hieroCore.Timecode.framesToHMSF(ass_frame, int(fps), 0)
    #             ass_frame += duration
    #             out_time = hieroCore.Timecode.framesToHMSF(ass_frame, int(fps), 0)
    #             start = "%s:%s:%s.%s" % (str(in_time[0]).zfill(2), str(in_time[1]).zfill(2), str(in_time[2]).zfill(2),
    #                                      str(in_time[3] / fps).split('.')[-1][:2].ljust(2,
    #                                                                                     '0'))  # only support 2 decimal places without rounding
    #             end = "%s:%s:%s.%s" % (str(out_time[0]).zfill(2), str(out_time[1]).zfill(2), str(out_time[2]).zfill(2),
    #                                    str(out_time[3] / fps).split('.')[-1][:2].ljust(2, '0'))
    #             seq = str(self.shotCodeForm.item(self.trackitems.index(trackitem), 0).text()).split(" ")[0]
    #             shot = str(self.shotCodeForm.item(self.trackitems.index(trackitem), 0).text()).split(" ")[1]
    # 
    #             if ep == "":
    #                 shotcode = "%s_%s" % (seq, shot)
    #                 shot_yaml = "%s/%s/editorial/shotgun_info/%s_shot.yml" % (config.ws, show, show)
    #             else:
    #                 shotcode = "%s_%s_%s" % (ep, seq, shot)
    #                 shot_yaml = "%s/%s/editorial/shotgun_info/%s_%s_shot.yml" % (
    #                     config.ws, show, show, ep)
    #             shot_yaml_dict = update_shotgun_element.read_yaml(shot_yaml)
    # 
    #             f = open("%s/shotcode.ass" % temp_path, 'a')
    # 
    #             f.write("\nDialogue: 0,%s,%s,%s,,0,0,0,,%s" % (start, end, position, shotcode))
    #             shot_code_key = "%s_%s" % (show, shotcode)
    #             for key in shot_yaml_dict[shot_code_key]:
    #                 if 'tag' in key:
    #                     f.write("\nDialogue: 0,%s,%s,%s,,0,0,0,,%s" % (
    #                     start, end, position, shot_yaml_dict[shot_code_key][key]))
    #             f.close()
    # 
    #             ass_file = "%s/shotcode.ass" % temp_path
    #             ass_file = ass_file.replace("\\", "/").replace(":", "\\:")
    #             dest_file = "%s/temp-%s.mov" % (temp_path, str(part_count))
    #             convert_command = "%s/ffmpeg -ss %s -i \"%s\" -s 1280x720 -vframes %s -pix_fmt yuv420p -vf \"ass=\'%s\'\" -f mov %s" % (
    #                 temp_path, str(start_second), clip_source, str(duration), ass_file, dest_file)
    #             # convertCMD = "%s/ffmpeg -ss %s -i \"%s\" -s 1280x720 -vframes %s %s" % (
    #             # tempPath, str(startSecond), clipSource, str(duration), destFile.replace(".mov",".%04d.jpg"))
    #             log.write("%s\n\n" % convert_command)
    #             os.system(convert_command)
    #             f = open("%s/shotcode.ass" % temp_path, 'w')
    #             f.writelines(ass_template)
    #             f.close()
    #             part_count += 1
    #         log.close()
    #         txt_file = "%s/files.txt" % temp_path
    #         f = open(txt_file, 'w')
    #         for i in range(1, part_count):
    #             f.write("file \'temp-" + str(i) + ".mov" + "\'\n")
    #         f.close()
    #         if config._os == "Windows":
    #             merge_command = "cd /d %s && ffmpeg -f concat -i files.txt -c copy -y %s" % (
    #                 temp_path.replace('/', '\\'), os.path.basename(demo_saving_path))
    #         elif config._os in ("Darwin", "Linux"):
    #             merge_command = "cd %s && ./ffmpeg -f concat -i files.txt -c copy -y %s" % (
    #                 temp_path, os.path.basename(demo_saving_path))
    #         os.system(merge_command)
    #         shutil.move("%s/%s" % (temp_path, os.path.basename(demo_saving_path)), os.path.dirname(demo_saving_path))
    #         shutil.rmtree(temp_path)
    #         self.messageLabel.setText("Demo video convertion finished.")
    #     except:
    #         self.messageLabel.setText("Demo video convertion failed.")
    # 
    # def pre_snap(self, type):
    #     reload(config)
    #     self.Finished_Count = 0
    #     self.Failed_Count = 0
    #     if self.check_gui_input() and self.check_duplicate():
    #         self.messageLabel.setText("Start snaping, please wait......")
    #         reload(parse_trackitem)
    #         self.status = parse_trackitem.check_missing_info(self.trackitems)
    #         count = len(self.trackitems)
    #         for i in range(0, count):
    #             self.shotCodeForm.setItem(i, 1, QtWidgets.QTableWidgetItem(self.status[i]))
    #             if self.status[i] == "":
    #                 snap_path = self.parse_snap_path(i, type)
    #                 if not os.path.exists(os.path.dirname(snap_path)):
    #                     try:
    #                         os.makedirs(os.path.dirname(snap_path))
    #                     except:
    #                         self.setResultItem(i, "create folder failed")
    #                         self.Failed_Count += 1
    #                         return False
    #                 self.snapProcessThread = Thread(target=self.snap_process, args=(i, type))
    #                 self.snapProcessThread.setDaemon(True)
    #                 self.snapProcessThread.start()
    #             else:
    #                 self.Failed_Count += 1
    #         finishedStatusThread = Thread(target=self.finished_status, args=())
    #         finishedStatusThread.setDaemon(True)
    #         finishedStatusThread.start()
    # 
    # def parse_snap_path(self, row, snap_type):
    #     # TODO get snap path from directory_structure
    #     show = self.showNameEdit.text()
    #     ep = self.episodeEdit.text()
    #     seq = str(self.shotCodeForm.item(row, 0).text()).split(" ")[0]
    #     shot = str(self.shotCodeForm.item(row, 0).text()).split(" ")[1]
    #     type = str(self.shotCodeForm.item(row, 0).text()).split(" ")[2]
    #     if snap_type == "element":
    #         if ep == "" or self.showTypeList.currentText() != "TV Series":
    #             snap_path = "%s/%s/editorial/element_snap/%s/%s_%s.jpg" % (config.ws, show, seq, shot, type)
    #         else:
    #             snap_path = "%s/%s/editorial/element_snap/%s/%s/%s_%s.jpg" % (config.ws, show, ep, seq, shot, type)
    #     elif snap_type == "shot":
    #         if ep == "" or self.showTypeList.currentText() != "TV Series":
    #             snap_path = "%s/%s/editorial/shot_snap/%s/%s_%s.jpg" % (config.ws, show, seq, shot, type)
    #         elif show == 'dph':
    #             snap_path = "%s/%s/editorial/shot_snap/%s/%s/%s_%s_%s.jpg" % (
    #             config.ws, show, ep, seq, ep.upper(), seq.upper(), shot)
    #         elif show == 'shd':
    #             snap_path = "%s/%s/editorial/shot_snap/%s/%s_%s_%s.jpg" % (
    #             config.ws, show, ep, ep.upper(), seq.upper(), shot)
    #     return snap_path
    # 
    # def snap_process(self, i, type):
    #     trackitem = self.trackitems[i]
    #     snap_path = self.parse_snap_path(i, type)
    #     # if os.path.exists(snap_path) and os.path.isfile(snap_path):
    #     #     self.setResultItem(i, "snap successfully")
    #     #     self.Finished_Count += 1
    #     #     return True
    #     snap_frame = int((int(trackitem.sourceIn()) + int(trackitem.sourceOut())) / 2)
    #     frame_second = str(float(snap_frame) / int(self.fpsList.currentText()))
    #     trackitem_source = trackitem.source().mediaSource().metadata().value('foundry.source.fullpath').replace(
    #         " ", "@")
    #     snap_command = "%s -ss %s -i \"%s\" -f image2 -y -vframes 1 %s" % (
    #     config.ffmpeg_path, frame_second, trackitem_source, snap_path)
    #     try:
    #         p = os.system(snap_command)
    #         if p == 0:
    #             self.setResultItem(i, "snap successfully")
    #             self.Finished_Count += 1
    #             return True
    #         else:
    #             self.setResultItem(i, "snap failed")
    #             self.Failed_Count += 1
    #             return False
    #     except:
    #         self.setResultItem(i, "snap failed")
    #         self.Failed_Count += 1
    #         return False
    # 
    # def pre_copy(self):
    #     self.Finished_Count = 0
    #     self.Failed_Count = 0
    #     if self.check_gui_input():
    #         self.messageLabel.setText("Start copying, please wait......")
    #         reload(parse_trackitem)
    #         self.status = parse_trackitem.check_missing_info(self.trackitems)
    #         self.head_handle = self.headHandleEdit.text()
    #         self.tail_handle = self.tailHandleEdit.text()
    #         count = len(self.trackitems)
    #         for i in range(0, count):
    #             self.shotCodeForm.setItem(i, 1, QtWidgets.QTableWidgetItem(self.status[i]))
    #             if self.status[i] == "":
    #                 self.dest = self.parse_dest_path(i)
    #                 self.copy_plate(i)
    #             else:
    #                 self.Failed_Count += 1
    #         finishedStatusThread = Thread(target=self.finished_status, args=())
    #         finishedStatusThread.setDaemon(True)
    #         finishedStatusThread.start()
    # 
    # def parse_dest_path(self, row):
    #     dest_pattern = ["", ""]
    #     show = self.showNameEdit.text()
    #     ep = self.episodeEdit.text()
    #     seq = str(self.shotCodeForm.item(row, 0).text()).split(" ")[0]
    #     shot = str(self.shotCodeForm.item(row, 0).text()).split(" ")[1]
    #     type = str(self.shotCodeForm.item(row, 0).text()).split(" ")[2]
    #     version = self.versionEdit.text()
    #     if ep == "" or self.showTypeList.currentText() != "TV Series":
    #         destpath = "%s/%s/%s" % (
    #             directory_folder.create_plate_path_from_dict({'show': show, 'sequence': seq, 'shot': shot}),
    #             type, version)
    #         dest_pattern[1] = "%s_%s_%s_%s_%s" % (show, seq, shot, type, version)
    #     else:
    #         destpath = "%s/%s/%s" % (
    #         directory_folder.create_plate_path_from_dict({'show': show, 'sequence': seq, 'shot': shot, 'episode': ep}),
    #         type, version)
    #         dest_pattern[1] = "%s_%s_%s_%s_%s_%s" % (show, ep, seq, shot, type, version)
    #     dest_pattern[0] = destpath
    #     return dest_pattern
    # 
    # def copy_plate(self, i):
    #     trackitem = self.trackitems[i]
    #     plate_frames = parse_trackitem.get_plate_frames(trackitem)
    #     plate_format = os.path.splitext(plate_frames[0])[1].lower().replace(".", "")
    #     self.dest[0] = "%s/%s" % (self.dest[0], plate_format)
    #     if not (os.path.exists(self.dest[0]) and os.path.isdir(self.dest[0])):
    #         try:
    #             os.makedirs(self.dest[0])
    #         except:
    #             self.setResultItem(i, "destination missing")
    # 
    #     plate_frames_string = "@".join(plate_frames)
    #     cmd = ['python',
    #            '%s/copy_process.py' % os.path.dirname(os.path.realpath(__file__)),
    #            str(self.dest[0]), str(self.dest[1]), str(self.head_handle), str(self.tail_handle), plate_frames_string]
    #     s = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    # 
    #     copy_status_thread = Thread(target=self.copy_status, args=(s, i,))
    #     copy_status_thread.setDaemon(True)
    #     copy_status_thread.start()
    # 
    # def copy_status(self, s, row):
    #     # get copy results from subprocess' stdout
    #     for line in iter(s.stdout.readline, ''):
    #         if "Copy Finished!" in line:
    #             self.setResultItem(row, 'copy finished')
    #             self.Finished_Count += 1
    #         else:
    #             self.setResultItem(row, 'copy failed')
    #             self.Failed_Count += 1
    # 
    # def generate_shot_info(self):
    #     reload(update_shotgun_element)
    #     if self.check_gui_input() and self.check_duplicate():
    #         try:
    #             show = str(self.showNameEdit.text())
    #             ep = str(self.episodeEdit.text())
    #         except:
    #             self.show_message("wrong show info, please check.")
    #             return False
    #         count = len(self.trackitems)
    #         for i in range(0, count):
    #             trackitem = self.trackitems[i]
    # 
    #             cut_duration = str(trackitem.duration())
    #             # speed = str(trackitem.playbackSpeed())
    #             try:
    #                 seq = str(self.shotCodeForm.item(i, 0).text()).split(" ")[0]
    #                 shot = str(self.shotCodeForm.item(i, 0).text()).split(" ")[1]
    #             except:
    #                 self.show_message("wrong shotcode, please check.")
    #                 return False
    #             if ep == "":
    #                 shot_name = "%s_%s_%s" % (show, seq, shot)
    #             else:
    #                 shot_name = "%s_%s_%s_%s" % (show, ep, seq, shot)
    # 
    #             info_dict = dict(
    #                 show=show,
    #                 ep="",
    #                 seq=seq,
    #                 shot=shot,
    #                 cut_duration=cut_duration,
    #                 # speed = speed,
    #             )
    #             if self.showTypeList.currentText() == "TV Series" and ep != "":
    #                 info_dict['ep'] = ep
    #             update_shotgun_element.insert_info(self.shot_dict, shot_name, info_dict)
    #         if ep == "":
    #             yaml_saving_path = "%s/%s/editorial/shotgun_info/%s_shot.yml" % (config.ws, show, show)
    #         else:
    #             yaml_saving_path = "%s/%s/editorial/shotgun_info/%s_%s_shot.yml" % (
    #                 config.ws, show, show, ep)
    #         update_shotgun_element.save_dict_to_yaml(yaml_saving_path, self.shot_dict)
    #         self.messageLabel.setText("Generate shot info finished.")
    # 
    # def add_tag(self):
    #     if self.check_gui_input() and self.check_duplicate():
    #         try:
    #             show = str(self.showNameEdit.text())
    #             ep = str(self.episodeEdit.text())
    #         except:
    #             self.show_message("wrong show info, please check.")
    #             return False
    #         if self.tag_key_edit.text() != "" and self.tag_value_edit.text() != "":
    #             tag_value = str(self.tag_value_edit.text())
    #             tag_key = str(self.tag_key_edit.text())
    #             tag_info_dict = {
    #                 tag_key: tag_value,
    #             }
    #         else:
    #             self.show_message("please fill tag information.")
    #             return False
    #         count = len(self.trackitems)
    #         for i in range(0, count):
    #             trackitem = self.trackitems[i]
    # 
    #             cut_duration = str(trackitem.duration())
    #             # speed = str(trackitem.playbackSpeed())
    #             try:
    #                 seq = str(self.shotCodeForm.item(i, 0).text()).split(" ")[0]
    #                 shot = str(self.shotCodeForm.item(i, 0).text()).split(" ")[1]
    #             except:
    #                 self.show_message("wrong shotcode, please check.")
    #                 return False
    #             if ep == "":
    #                 shot_name = "%s_%s_%s" % (show, seq, shot)
    #             else:
    #                 shot_name = "%s_%s_%s_%s" % (show, ep, seq, shot)
    #             update_shotgun_element.insert_info(self.shot_dict, shot_name, tag_info_dict)
    #         if ep == "":
    #             shot_yaml = "%s/%s/editorial/shotgun_info/%s_shot.yml" % (config.ws, show, show)
    #         else:
    #             shot_yaml = "%s/%s/editorial/shotgun_info/%s_%s_shot.yml" % (
    #                 config.ws, show, show, ep)
    #         update_shotgun_element.save_dict_to_yaml(shot_yaml, self.shot_dict)
    #         self.messageLabel.setText("Update shot info finished.")
    # 
    # def generate_element_edit_info(self):
    #     reload(update_shotgun_element)
    #     if self.check_gui_input() and self.check_duplicate():
    #         show = str(self.showNameEdit.text())
    #         ep = str(self.episodeEdit.text())
    #         # TODO auto version
    #         version = str(self.versionEdit.text())
    #         count = len(self.trackitems)
    #         for i in range(0, count):
    #             trackitem = self.trackitems[i]
    # 
    #             cut_duration = str(trackitem.duration())
    #             # speed = str(trackitem.playbackSpeed())
    # 
    #             seq = str(self.shotCodeForm.item(i, 0).text()).split(" ")[0]
    #             shot = str(self.shotCodeForm.item(i, 0).text()).split(" ")[1]
    #             type = str(self.shotCodeForm.item(i, 0).text()).split(" ")[2]
    #             snap_path = str(self.parse_snap_path(i, "element"))
    # 
    #             if ep == "":
    #                 plate_name = "%s_%s_%s_%s_%s" % (show, seq, shot, type, version)
    #             else:
    #                 plate_name = "%s_%s_%s_%s_%s_%s" % (show, ep, seq, shot, type, version)
    # 
    #             info_dict = dict(
    #                 show=show,
    #                 ep=ep,
    #                 seq=seq,
    #                 shot=shot,
    #                 type=type,
    #                 version=version,
    #                 cut_duration=cut_duration,
    #                 snap_path=snap_path,
    #             )
    # 
    #             update_shotgun_element.insert_info(self.element_dict, plate_name, info_dict)
    #         if ep == "":
    #             yaml_saving_path = "%s/%s/editorial/shotgun_info/%s_element.yml" % (config.ws, show, show)
    #         else:
    #             yaml_saving_path = "%s/%s/editorial/shotgun_info/%s_%s_element.yml" % (
    #                 config.ws, show, show, ep)
    #         update_shotgun_element.save_dict_to_yaml(yaml_saving_path, self.element_dict)
    #         self.messageLabel.setText("Generate edit info finished.")
    # 
    # def generate_element_plate_info(self):
    #     reload(update_shotgun_element)
    #     if self.check_gui_input() and self.check_duplicate():
    #         show = str(self.showNameEdit.text())
    #         ep = str(self.episodeEdit.text())
    #         version = str(self.versionEdit.text())
    #         count = len(self.trackitems)
    #         for i in range(0, count):
    #             seq = str(self.shotCodeForm.item(i, 0).text()).split(" ")[0]
    #             shot = str(self.shotCodeForm.item(i, 0).text()).split(" ")[1]
    #             type = str(self.shotCodeForm.item(i, 0).text()).split(" ")[2]
    #             trackitem = self.trackitems[i]
    #             source_duration = str(int(trackitem.sourceDuration()))
    # 
    #             if type != "blank" and parse_trackitem.check_missing_frame(trackitem) == "":
    #                 fps = int(self.fpsList.currentText())
    #                 source_in = hieroCore.Timecode.framesToHMSF(
    #                     int(trackitem.source().mediaSource().metadata().value('foundry.source.starttime')) + int(
    #                         trackitem.sourceIn()), fps, 0)
    #                 source_in_tc = "%s:%s:%s:%s" % (
    #                 str(source_in[0]).zfill(2), str(source_in[1]).zfill(2), str(source_in[2]).zfill(2),
    #                 str(source_in[3]).zfill(2))
    #                 source_out = hieroCore.Timecode.framesToHMSF(
    #                     int(trackitem.source().mediaSource().metadata().value('foundry.source.starttime')) + int(
    #                         trackitem.sourceOut()), fps, 0)
    #                 source_out_tc = "%s:%s:%s:%s" % (
    #                     str(source_out[0]).zfill(2), str(source_out[1]).zfill(2), str(source_out[2]).zfill(2),
    #                     str(source_out[3]).zfill(2))
    # 
    #                 ori_plate_path = parse_trackitem.get_plate_path(trackitem)
    #                 source_name = str(trackitem.name())
    #                 plate_format = os.path.splitext(ori_plate_path)[1].lower().replace(".", "")
    #                 if ep == "":
    #                     plate_name = "%s_%s_%s_%s_%s.####.%s" % (show, seq, shot, type, version, plate_format)
    #                 else:
    #                     plate_name = "%s_%s_%s_%s_%s_%s.####.%s" % (show, ep, seq, shot, type, version, plate_format)
    #                 dest_plate_path = "%s/%s/%s" % (str(self.parse_dest_path(i)[0]), plate_format, plate_name)
    # 
    #                 info_dict = dict(
    #                     show=show,
    #                     ep=ep,
    #                     seq=seq,
    #                     shot=shot,
    #                     type=type,
    #                     version=version,
    #                     head_handle="",
    #                     tail_handle="",
    #                     source_duration=source_duration,
    #                     source_in=source_in_tc,
    #                     source_out=source_out_tc,
    #                     source_name=source_name,
    #                     plate_format=plate_format,
    #                     plate_path=""
    #                 )
    #                 head_handle, tail_handle = update_shotgun_element.get_plate_handle(dest_plate_path, source_duration,
    #                                                                                    plate_format)
    #                 if head_handle != "error" and tail_handle != "error":
    #                     info_dict['head_handle'] = head_handle
    #                     info_dict['tail_handle'] = tail_handle
    #                     info_dict['plate_path'] = dest_plate_path
    #                 else:
    #                     info_dict['head_handle'] = ""
    #                     info_dict['tail_handle'] = ""
    #                     info_dict['plate_path'] = ""
    #                 update_shotgun_element.insert_info(self.element_dict, plate_name.split(".")[0], info_dict)
    #             else:
    #                 info_dict = dict(
    #                     show=show,
    #                     ep=ep,
    #                     seq=seq,
    #                     shot=shot,
    #                     type=type,
    #                     version=version,
    #                     head_handle="",
    #                     tail_handle="",
    #                     source_duration=source_duration,
    #                     source_in="",
    #                     source_out="",
    #                     source_name="",
    #                     plate_format="",
    #                     plate_path=""
    #                 )
    #                 if ep == "":
    #                     plate_name = "%s_%s_%s_%s_%s" % (show, seq, shot, type, version)
    #                 else:
    #                     plate_name = "%s_%s_%s_%s_%s_%s" % (show, ep, seq, shot, type, version)
    #                 update_shotgun_element.insert_info(self.element_dict, plate_name, info_dict)
    #         if ep == "":
    #             yaml_saving_path = "%s/%s/editorial/shotgun_info/%s_element.yml" % (config.ws, show, show)
    #         else:
    #             yaml_saving_path = "%s/%s/editorial/shotgun_info/%s_%s_element.yml" % (config.ws, show, show, ep)
    #         update_shotgun_element.save_dict_to_yaml(yaml_saving_path, self.element_dict)
    #         self.messageLabel.setText("Generate plate info finished.")
    # 
    # def computing_retime(self):
    #     if self.check_gui_input():
    #         show = str(self.showNameEdit.text())
    #         ep = str(self.episodeEdit.text())
    #     if ep == "":
    #         element_yaml_path = "%s/%s/editorial/shotgun_info/%s_element.yml" % (config.ws, show, show)
    #     else:
    #         element_yaml_path = "%s/%s/editorial/shotgun_info/%s_%s_element.yml" % (config.ws, show, show, ep)
    # 
    #     if update_shotgun_element.generate_retime_info(element_yaml_path):
    #         self.messageLabel.setText("Computing retime info finished.")
    #     else:
    #         self.show_message("Some info missing in yml files.")
    # 
    # def generate_cut_info(self):
    #     reload(update_shotgun_element)
    #     if self.check_gui_input():
    #         show = str(self.showNameEdit.text())
    #         ep = str(self.episodeEdit.text())
    #         shot_yaml = "%s/%s/editorial/shotgun_info/%s_%s_shot.yml" % (config.ws, show, show, ep)
    #         element_yaml = "%s/%s/editorial/shotgun_info/%s_%s_element.yml" % (config.ws, show, show, ep)
    #         cut_yaml = "%s/%s/editorial/shotgun_info/%s_%s_cut.yml" % (config.ws, show, show, ep)
    #         if update_shotgun_element.generate_cut_info(shot_yaml, element_yaml, cut_yaml):
    #             self.messageLabel.setText("Generate cut info finished.")
    #         else:
    #             self.show_message("Some info missing in yml files.")
    # 
    # def setResultItem(self, row, result):
    #     self.shotCodeForm.setItem(int(row), 1, QtWidgets.QTableWidgetItem(result))
    # 
    # def finished_status(self):
    #     while True:
    #         if self.Finished_Count + self.Failed_Count == self.shotCodeForm.rowCount():
    #             break
    #     if self.Finished_Count == self.shotCodeForm.rowCount():
    #         self.messageLabel.setText("All shots have been successfully processed!")
    #     else:
    #         self.messageLabel.setText("Please check all failed shots!")