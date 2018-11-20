"""Main module includes all GUI classes and helper functions."""

import os
import shutil
import sys
# Import built-in modules
from functools import partial

# Import third-party modules
import nuke

try:
    from PySide import QtCore
    from PySide import QtGui
except ImportError:
    from PySide2 import QtCore
    from PySide2 import QtWidgets as QtGui

# List of Nuke node class which has a file knob.
READ_CLASSES = [
    'Read',
    'DeepRead',
    'ReadGeo2',
    'ReadGeo',
    'Camera2',
    'Vectorfield'
]


def get_all_nodes(cls=None):
    """Get all nodes from Nuke node tree, return nodes with specific
       class if cls parameter been set.

    Args:
        cls (str): Node class name. If set None then get all nodes from node
                   tree.

    Return:
        :obj: `list` of :ojb: `nuke.Node`: All needed nodes.

    """
    if cls:
        return nuke.allNodes(cls, recurseGroups=True)
    else:
        return nuke.allNodes(recurseGroups=True)


def get_read_nodes():
    """Get list of specific nodes that have file knob.

    Return:
        :obj: `list` of :ojb: `nuke.Node`: All specific nodes with file knob.

    """
    nodes = []
    for c in READ_CLASSES:
        nodes.extend(get_all_nodes(c))
    return nodes


def modify_path(node):
    """Modify file path in given node to use relative path.

    Args:
        node (nuke.Node): A specific node that hold file knob.

    """
    if node.Class() == 'Vectorfield':
        knob_name = 'vfield_file'
    else:
        knob_name = 'file'
    source = node[knob_name].value()
    basename = os.path.basename(source)

    if os.path.isfile(source):
        node[knob_name].setValue(
            '[file dirname [value root.name]]/sources/' + basename)
    else:
        node['file'].setValue(('[file dirname [value root.name]]/sources/'
                               '{}/{}').format(basename.split('.')[0],
                                               basename))


def frame_to_pattern(frame_path):
    """Convert frame count to frame pattern in an image file path.

    Args:
        frame_path (str): Path of an image file with frame count.

    Returns:
        str: Path of an image sequence with frame pattern.

    """
    name_list = frame_path.split('.')
    name_list[-2] = '%04d'
    return '.'.join(name_list).replace('\\', '/')


class NukePackageWrapper(object):
    """Worker class of packaging process."""

    def __init__(self, dest_root):
        """ Initialize packaging worker class.

        Args:
            dest_root (str): Path of destination root folder.

        """
        self.error_nodes = []
        self.single_results = []
        self.sequence_results = {}
        self.copy_files_count = 0
        self.dest_root = dest_root
        self.original_nk = nuke.Root().name()
        self.nodes = filter(self.check_node_error, get_read_nodes())

    def check_node_error(self, node):
        """Check if given node has error.

        Args:
            node (nuke.Node): A specific node.

        Returns:
            bool: True if there's no error on the given node, False if not.

        """
        if node.hasError():
            self.error_nodes.append(node.name())
            return False
        else:
            return True

    def get_sequence_source(self, node, source, pattern):
        """Get and store source information of an image sequence.

        Args:
            node (nuke.Node): A node holds an image sequence in its file knob.
            source (str): Source path pattern of the node's file knob.
            pattern (str): Sequence count pattern of the source path.

        """
        source_files = []
        first = node['first'].value()
        last = node['last'].value()
        for frame in range(first, last + 1):
            source_file = source.replace(pattern, str(frame).zfill(4))
            if os.path.isfile(source_file):
                source_files.append(source_file)
                self.copy_files_count += 1
        if source_files:
            basename = '.'.join(os.path.basename(source).split('.')[:-2])
            self.sequence_results[basename] = (node.name(),
                                               source_files,
                                               first,
                                               last)
        else:
            self.error_nodes.append(node.name())

    def get_node_source(self, node):
        """Get source information of a given node.

        Args:
            node (nuke.Node): A specific node that has file knob.

        """
        if node.Class() == 'Vectorfield':
            knob_name = 'vfield_file'
        else:
            knob_name = 'file'
        source = node[knob_name].value()
        if os.path.isfile(source):
            self.single_results.append((node.name(), source))
            self.copy_files_count += 1
        elif '%04d' in source:
            self.get_sequence_source(node, source, '%04d')
        elif '####' in source:
            self.get_sequence_source(node, source, '####')
        else:
            return

    def grab_source(self, index):
        """Grab sources information from specific nodes."""
        self.get_node_source(self.nodes[index])

    def modify_nodes_path(self):
        """Modify file knobs in specific nodes to use relative paths."""

        # We save the script to destination folder before modify it,
        # by this way we do not change anything in the original nk file.
        nuke.scriptSaveAs('{}/{}'.format(self.dest_root,
                                         os.path.basename(nuke.Root().name())),
                          1)
        for node in self.nodes:
            modify_path(node)
        nuke.scriptSaveAs('{}/{}'.format(self.dest_root,
                                         os.path.basename(nuke.Root().name())),
                          1)

        # Restore original nk file to let users continue to do their jobs.
        nuke.scriptClear()
        nuke.scriptOpen(self.original_nk)


class CollectThread(QtCore.QThread):
    """Worker thread to collect sources' information from node tree."""

    # Qt signal emitted when finish or stop this copy process.
    finish = QtCore.Signal()

    def __init__(self, dest_root):
        super(CollectThread, self).__init__()
        self.dest_root = dest_root
        self.run_flag = True

    def run(self):
        self.packaging_wrapper = NukePackageWrapper(self.dest_root)
        self.index = 0
        self.log = []
        while self.run_flag and self.index < len(self.packaging_wrapper.nodes):
            self.packaging_wrapper.grab_source(self.index)
            self.index += 1
        if self.packaging_wrapper.error_nodes:
            self.log.append('\n\nNodes with error:')
        for node in self.packaging_wrapper.error_nodes:
            self.log.append('\n{}'.format(node.name()))
        self.finish.emit()


class SequenceCopyThread(QtCore.QThread):
    """Worker thread to copy an image sequence."""

    # Qt signal emitted when finish or stop this copy process.
    finish = QtCore.Signal()
    # Qt signal emitted when one file been copied.
    copy_one_file = QtCore.Signal(str)

    def __init__(self, basename, sequence_info, dest_folder):
        """Initialize sequence copy worker thread.

        Args:
            basename (str): Image basename without frame count and format.
            sequence_info (tuple):
                (
                    image_sequence_folder_path,
                    first_frame_number,
                    last_frame_number,
                    file_format
                )
            dest_folder (str): Destination root folder path.

        """
        super(SequenceCopyThread, self).__init__()
        self.node_name = sequence_info[0]
        self.source_files = sequence_info[1]
        self.first = sequence_info[2]
        self.last = sequence_info[3]
        self.basename = basename
        self.dest_folder = '{}/sources/{}'.format(dest_folder, basename)
        self.running_flag = True
        self._mutex = QtCore.QMutex()

    def run(self):
        """Copy every frame into destination folder."""
        sequence_length = len(self.source_files)
        self.log = []
        if sequence_length < self.last - self.first + 1:
            self.log.append('\n\n{} (missing frame)'.format(self.node_name))
        else:
            self.log.append('\n\n{}'.format(self.node_name))
        self.index = 0

        if not os.path.isdir(self.dest_folder):
            os.makedirs(self.dest_folder)

        while self.running_flag and self.index < sequence_length:
            source = self.source_files[self.index]
            shutil.copy2(source, self.dest_folder)
            self._mutex.lock()
            self.copy_one_file.emit(source)
            self._mutex.unlock()
            self.index += 1
        if self.index == sequence_length - 1:
            self.log.append(
                '\n{} {}-{}'.format(frame_to_pattern(self.source_files[0]),
                                    self.first,
                                    self.last))
        elif self.index > 0:
            self.log.append(
                '\n{} {}-{}'.format(frame_to_pattern(self.source_files[0]),
                                    self.first,
                                    self.first + self.index))
        self.finish.emit()


class SingleCopyThread(QtCore.QThread):
    """Worker thread to copy a list of single file."""

    # Qt signal emitted when finish or stop this copy process.
    finish = QtCore.Signal()
    copy_one_file = QtCore.Signal(str)

    def __init__(self, source_list, dest_folder):
        """Initialize single file copy worker thread.

        Args:
            source_list (list): List of single file.
            dest_folder (str): Destionation root folder path.

        """
        super(SingleCopyThread, self).__init__()
        self.source_list = source_list
        self.dest_folder = '{}/sources'.format(dest_folder)
        self.running_flag = True
        self._mutex = QtCore.QMutex()

    def run(self):
        """Copy every single file into destination folder."""
        source_count = len(self.source_list)
        copy_count = 0
        source_iter = iter(self.source_list)
        if not os.path.isdir(self.dest_folder):
            os.makedirs(self.dest_folder)
        self.log = []
        while self.running_flag and copy_count < source_count:
            node_name, source = source_iter.next()
            shutil.copy2(source, self.dest_folder)
            self._mutex.lock()
            self.copy_one_file.emit(source)
            self.log.append('\n\n{}\n{}'.format(node_name, source))
            self._mutex.unlock()
            copy_count += 1
        self.finish.emit()


class FinishThread(QtCore.QThread):
    """Monitor thread to check whether all copy processes are complete."""

    # Qt signal emitted when finish or stop this copy process.
    finish = QtCore.Signal()

    def __init__(self, obj):
        """Initialize monitor thread.

        Args:
            obj (QtGui.QWidget): Tool's main UI instance.

        """
        super(FinishThread, self).__init__()
        self.obj = obj
        self.running_flag = True

    def run(self):
        """Check whether all copy processes are complete."""
        while self.running_flag and len(self.obj.thread_pool) > 1:
            continue
        self.finish.emit()


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

        self.folder_button.clicked.connect(self.select_destionation)
        self.run_button.clicked.connect(self.run_packaging)

        self.close_flag = False
        self.close_timer = QtCore.QTimer()
        self.close_timer.timeout.connect(self.check_thread_pool)

        self.packaging_wrapper = None
        self.thread_pool = []
        self.finish_log = []
        self.copy_count = 0

    def check_thread_pool(self):
        """Check if there's any worker thread remains in thread pool, if yes
           then restart the timer, if no then set close flag to True.

        """
        if len(self.thread_pool) <= 1:
            self.close_flag = True
            self.close_timer.stop()
            self.save_copy_log()
            self.refresh_ui()
            self.close()
        else:
            self.close_timer.start(1000)

    def refresh_ui(self):
        """Reset and clear widgets value.

        Because we use global parameter to store UI instance, we need to
        refresh it before closing.

        """
        self.progress_bar.reset()
        self.message.clear()
        self.folder_line.clear()

    def closeEvent(self, event):
        """Override closeEvent functionality to stop all worker thread before
           closing the GUI.

        Args:
            event (QtCore.QEvent): Close widget event emitted by Qt.

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

    def select_destionation(self):
        """Open explorer dialog to select a folder and update the folder path
           widget.

        """
        dest_folder = QtGui.QFileDialog().getExistingDirectory()

        # PySide
        if isinstance(dest_folder, list) and os.path.isdir(dest_folder[0]):
            self.folder_line.setText(dest_folder[0])
        # PySide2
        if os.path.isdir(dest_folder):
            self.folder_line.setText(dest_folder)

    def check_dest_root(self):
        """Check if the folder line edit in UI holds a valid folder path.
           Will try to create the folder path if it not exists.

        Return:
            bool: True if get a valid folder path, False otherwise.

        """
        dest_root = self.folder_line.text()
        if not os.path.isdir(dest_root):
            try:
                os.makedirs(dest_root)
            except:
                self.message.setText('Please input a valid folder path.')
                return False
        return True

    def thread_finish(self, thread):
        """Remove worker thread from thread pool when it finish running, and
           update the percentage of progress bar.

        Args:
            thread (QtCore.QThread): Worker thread instance.

        """
        if thread in self.thread_pool:
            self.finish_log.extend(thread.log)
            self.thread_pool.remove(thread)

    def collect_finish(self, thread):
        """Get packaging wrapper result and prepare copy process.

        Save nuke script to destination folder and modify file knobs to
        use relative paths, remove collect thread from thread pool, start
        copy process.

        """
        index = thread.index + 1
        self.packaging_wrapper = thread.packaging_wrapper
        self.total_copy_amount = self.packaging_wrapper.copy_files_count
        self.thread_finish(thread)
        if index == len(self.packaging_wrapper.nodes):
            self.packaging_wrapper.modify_nodes_path()
            self.copy_process()

    def show_copy_status(self, source):
        """Show file been copying and update percentage of process bar."""
        self.message.setText('Copy {}......'.format(os.path.basename(source)))
        self.copy_count += 1
        process = int((float(self.copy_count) / float(self.total_copy_amount)) * 100)
        self.progress_bar.setValue(process)

    def copy_process(self):
        """Create, store and run worker threads."""
        self.message.setText('Starting packaging, please wait.')

        single_copy_thread = SingleCopyThread(self.packaging_wrapper.single_results,
                                              self.packaging_wrapper.dest_root)
        single_copy_thread.finish.connect(partial(self.thread_finish, single_copy_thread))
        single_copy_thread.copy_one_file.connect(self.show_copy_status)
        self.thread_pool.append(single_copy_thread)

        for basename in self.packaging_wrapper.sequence_results:
            sequence_copy_thread = SequenceCopyThread(basename,
                                                      self.packaging_wrapper.sequence_results[basename],
                                                      self.packaging_wrapper.dest_root)
            sequence_copy_thread.finish.connect(partial(self.thread_finish, sequence_copy_thread))
            sequence_copy_thread.copy_one_file.connect(self.show_copy_status)
            self.thread_pool.append(sequence_copy_thread)

        finish_thread = FinishThread(self)
        finish_thread.finish.connect(self.show_finish)
        self.thread_pool.append(finish_thread)

        for thread in self.thread_pool:
            thread.start()

    def run_packaging(self):
        """Create and run collector thread and start."""
        if self.check_dest_root():
            self.message.setText('Collecting source files information......')
            collect_thread = CollectThread(self.folder_line.text())
            collect_thread.finish.connect(partial(self.collect_finish,
                                                  collect_thread))
            self.thread_pool.append(collect_thread)
            collect_thread.start()

    def save_copy_log(self):
        """Save copy log to destination root folder."""
        if self.packaging_wrapper and self.finish_log:
            with open('{}/copy_log.log'.format(self.packaging_wrapper.dest_root),
                      'w') as f:
                self.finish_log[0] = self.finish_log[0].replace('\n\n', '')
                f.writelines(self.finish_log)

    def show_finish(self):
        """Save the copy log and show finish message."""
        self.save_copy_log()
        self.message.setText('Finish copying all sources.')


# Use global variable to prevent the GUI instance disappears immediately after
# showing.
p = PackagingUI()


def delivery_package():
    """Show GUI of vendor package tool."""
    p.show()


if __name__ == '__main__':
    delivery_package()
