"""Module includes the GUI class of this tool."""

# Import third-party modules
# pylint: disable=import-error
try:
    from PySide import QtCore
    from PySide import QtGui
except ImportError:
    from PySide2 import QtCore
    from PySide2 import QtWidgets as QtGui


class PackagingUI(QtGui.QWidget):
    """GUI class of this tool."""

    def __init__(self):
        """Initialize GUI and connect signal/slot."""
        super(PackagingUI, self).__init__(None, QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Packaging Nuke Script')
        self.setLayout(QtGui.QVBoxLayout())
        self.setFixedWidth(400)
        self.folder_layout = QtGui.QHBoxLayout()
        self.folder_label = QtGui.QLabel('Destination Folder:')
        self.folder_line = QtGui.QLineEdit()
        self.folder_button = QtGui.QPushButton('Select')
        self.folder_explorer = QtGui.QFileDialog()
        self.folder_layout.addWidget(self.folder_label)
        self.folder_layout.addWidget(self.folder_line)
        self.folder_layout.addWidget(self.folder_button)
        self.run_button = QtGui.QPushButton('Package Now!')
        self.progress_bar = QtGui.QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.message = QtGui.QLabel()
        self.layout().addLayout(self.folder_layout)
        self.layout().addWidget(self.run_button)
        self.layout().addWidget(self.progress_bar)
        self.layout().addWidget(self.message)

        self.close_timer = QtCore.QTimer()
        self.close_flag = False
        self.mutex = QtCore.QMutex()
        self.thread_pool = []

    def closeEvent(self, event):
        """Override closeEvent functionality to stop all worker thread before
           closing the GUI.

        Args:
            event (QtCore.QCloseEvent): Close widget event emitted by Qt.

        """
        if not self.thread_pool:
            self.refresh_ui()
            event.accept()
        else:
            for thread in self.thread_pool:
                thread.running_flag = False
            if not self.close_flag:
                self.close_timer.start(1000)
                event.ignore()
            else:
                event.accept()

    def refresh_ui(self):
        """Reset and clear widgets value.

        Because we use global parameter to store UI instance, we need to
        refresh it before closing.

        """
        self.progress_bar.reset()
        self.message.clear()
        self.folder_line.clear()

    def show_message(self, msg):
        """Update message text in the GUI."""
        self.message.setText(msg)
