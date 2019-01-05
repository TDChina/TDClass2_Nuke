"""Module includes controller class of this tool."""

# Import built-in modules
import os
from functools import partial

# Import local modules
from nuke_vendor_package.threads import CollectThread
from nuke_vendor_package.threads import FinishThread
from nuke_vendor_package.threads import SequenceCopyThread
from nuke_vendor_package.threads import SingleCopyThread


class NukePackageController(object):
    """Controller class to add behaviors for the GUI and handle packaging
       process.

    """

    def __init__(self, view):
        """Initialize controller class and connect GUI signals to slots."""
        super(NukePackageController, self).__init__()
        self.view = view
        self.finish_log = []
        self.copy_count = 0
        self.total_copy_amount = 0
        self.packaging_wrapper = None
        self.mutex = self.view.mutex
        self.connect_signal_slot()

    def check_thread_pool(self):
        """Check if there's any worker thread remains in thread pool, if yes
           then restart the timer, if no then set close flag to True.

        """
        if len(self.view.thread_pool) <= 1:
            self.view.close_flag = True
            self.view.close_timer.stop()
            self.save_copy_log()
            self.view.refresh_ui()
            self.view.close()
        else:
            self.view.close_timer.start(1000)

    def connect_signal_slot(self):
        """Connect GUI signals to slots."""
        self.view.folder_button.clicked.connect(self.select_destionation)
        self.view.run_button.clicked.connect(self.run_packaging)
        self.view.close_timer.timeout.connect(self.check_thread_pool)

    def select_destionation(self):
        """Open explorer dialog to select a folder and update the folder path
           widget.

        """
        dest_folder = self.view.folder_explorer.getExistingDirectory()

        # PySide
        if isinstance(dest_folder, list) and os.path.isdir(dest_folder[0]):
            self.view.folder_line.setText(dest_folder[0])
        # PySide2
        if os.path.isdir(dest_folder):
            self.view.folder_line.setText(dest_folder)

    def check_dest_root(self):
        """Check if the folder line edit in UI holds a valid folder path.
           Will try to create the folder path if it not exists.

        Return:
            bool: True if get a valid folder path, False otherwise.

        """
        dest_root = self.view.folder_line.text()
        if not os.path.isdir(dest_root):
            try:
                os.makedirs(dest_root)
            except (WindowsError, TypeError):
                self.view.message.setText('Please input a valid folder path.')
                return False
        return True

    def run_packaging(self):
        """Create all worker thread and start packaging process."""
        if self.check_dest_root():
            self.view.show_message('Collecting source files information......')
            collect_thread = CollectThread(self.view.folder_line.text())
            collect_thread.finish.connect(partial(self.collect_finish,
                                                  collect_thread))
            self.view.thread_pool.append(collect_thread)
            collect_thread.start()

    def collect_finish(self, thread):
        """Get packaging wrapper result and prepare copy process.

        Save nuke script to destination folder and modify file knobs to
        use relative paths, remove collect thread from thread pool, start
        copy process.

        Args:
            thread (QtCore.QThread): Collector thread instance.

        """
        index = thread.index
        self.packaging_wrapper = thread.packaging_wrapper
        self.total_copy_amount = self.packaging_wrapper.copy_files_count
        self.thread_finish(thread)
        if index == len(self.packaging_wrapper.nodes):
            self.packaging_wrapper.modify_nodes_path()
            self.copy_process()

    def copy_process(self):
        """Create, store and run worker threads."""
        self.view.show_message('Starting packaging, please wait.')

        single_copy_thread = SingleCopyThread(
            self.packaging_wrapper.single_results,
            self.packaging_wrapper.dest_root,
            self.mutex)
        single_copy_thread.finish.connect(
            partial(self.thread_finish, single_copy_thread))
        single_copy_thread.copy_one_file.connect(self.show_copy_status)
        self.view.thread_pool.append(single_copy_thread)

        for basename in self.packaging_wrapper.sequence_results:
            sequence_copy_thread = SequenceCopyThread(
                basename,
                self.packaging_wrapper.sequence_results[basename],
                self.packaging_wrapper.dest_root,
                self.mutex)
            sequence_copy_thread.finish.connect(
                partial(self.thread_finish, sequence_copy_thread))
            sequence_copy_thread.copy_one_file.connect(self.show_copy_status)
            self.view.thread_pool.append(sequence_copy_thread)

        finish_thread = FinishThread(self.view)
        finish_thread.finish.connect(self.finish_copy)
        self.view.thread_pool.append(finish_thread)

        for thread in self.view.thread_pool:
            thread.start()

    def show_copy_status(self, source):
        """Show file been copying and update percentage of process bar."""
        self.view.show_message('Copy {}...'.format(os.path.basename(source)))
        self.copy_count += 1
        process = int(
            (float(self.copy_count) / float(self.total_copy_amount)) * 100)
        self.view.progress_bar.setValue(process)

    def thread_finish(self, thread):
        """Remove worker thread from thread pool when it finish running, and
           update the percentage of progress bar.

        Args:
            thread (QtCore.QThread): Worker thread instance.

        """
        if thread in self.view.thread_pool:
            self.finish_log.extend(thread.log)
            self.view.thread_pool.remove(thread)

    def save_copy_log(self):
        """Save copy log to destination root folder."""
        if self.packaging_wrapper and self.finish_log:
            with open('{}/copy_log.log'.format(self.packaging_wrapper.dest_root),
                      'w') as log_file:
                self.finish_log[0] = self.finish_log[0].replace('\n\n', '')
                log_file.writelines(self.finish_log)

    def finish_copy(self):
        """Save the copy log and show finish message."""
        self.save_copy_log()
        self.view.show_message('Finish packaging all sources.')
