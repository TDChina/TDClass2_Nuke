import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtGui


class VersionComboBox(QtGui.QComboBox):
    versionChanged = QtCore.Signal(dict)

    def __init__(self, parent=None):
        QtGui.QComboBox.__init__(self, parent)

    def set_value(self, row, task):

        self._row = row
        self._task = task

        self.activated.connect(self.itemChanged)

    def itemChanged(self):
        info = {
            'task': self._task,
            'version': self.currentText(),
            'row': self._row
        }
        self.versionChanged.emit(info)


class ElementLoaderView(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ElementLoaderView, self).__init__()
        self.setLayout(QtGui.QVBoxLayout())
        self.setWindowTitle("Element Loader")

        self.project_label = QtGui.QLabel("Project:")
        self.project_name = QtGui.QLineEdit()
        self.project_name.setFixedWidth(70)
        self.sequence_label = QtGui.QLabel("sequence:")
        self.sequence_list = QtGui.QComboBox()
        self.sequence_list.setFixedWidth(70)
        self.shot_label = QtGui.QLabel("shot:")
        self.shot_list = QtGui.QComboBox()
        self.shot_list.setFixedWidth(90)

        self.shot_layout = QtGui.QHBoxLayout()
        self.shot_layout.addWidget(self.project_label)
        self.shot_layout.addWidget(self.project_name)
        self.shot_layout.addWidget(self.sequence_label)
        self.shot_layout.addWidget(self.sequence_list)
        self.shot_layout.addWidget(self.shot_label)
        self.shot_layout.addWidget(self.shot_list)

        self.layout().addLayout(self.shot_layout)

        self.element_table = QtGui.QTableWidget(0, 3)
        self.element_table.setHorizontalHeaderLabels(['task', 'version', 'format'])
        self.select_all_button = QtGui.QPushButton('Select All')
        self.unselect_all_button = QtGui.QPushButton('Unselect All')
        self.load_button = QtGui.QPushButton('Load')

        self.button_layout = QtGui.QVBoxLayout()
        self.button_layout.addWidget(self.select_all_button)
        self.button_layout.addWidget(self.unselect_all_button)
        self.button_layout.addWidget(self.load_button)

        self.load_layout = QtGui.QHBoxLayout()
        self.load_layout.addWidget(self.element_table)
        self.load_layout.addLayout(self.button_layout)

        self.layout().addLayout(self.load_layout)

        self.message_box = QtGui.QMessageBox()

    def set_project(self, project_name):
        self.project_name.setText(project_name)

    def set_sequence(self, sequences):
        self.sequence_list.clear()
        self.sequence_list.addItems(sequences)

    def set_shot(self, shots):
        self.shot_list.clear()
        self.shot_list.addItems(shots)

    def clear_table(self):
        for i in range(0, self.element_table.rowCount()):
            self.element_table.removeRow(0)

    def set_task(self, row_count, task):
        self.element_table.insertRow(row_count)
        element_item = QtGui.QTableWidgetItem(task)
        element_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
        element_item.setCheckState(QtCore.Qt.Checked)
        self.element_table.setItem(row_count, 0, element_item)
        #self.element_table.setCellWidget(row_count, 1, version_combo)
