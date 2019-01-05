"""Module includes data model class."""

# Import built-in modules
import os

# Import third-party modules
import nuke  # pylint: disable=import-error

# Import local modules
from nuke_vendor_package import utils


class NukePackageWrapper(object):
    """Worker class of packaing process."""

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
        self.nodes = [node for node in utils.get_read_nodes() if
                      self.check_node_error(node)]

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

    def grab_source(self, index):
        """Grab sources information from specific nodes.

        Args:
            index (int): Index of the nodes list.
        """
        self.get_node_source(self.nodes[index])

    def modify_nodes_path(self):
        """Modify file knobs in specific nodes to use relative paths."""
        # We save the script to destination folder before modify it,
        # by this way we do not change anything in the original nk file.
        nuke.scriptSaveAs('{}/{}'.format(self.dest_root,
                                         os.path.basename(nuke.Root().name())),
                          1)
        for node in self.nodes:
            utils.modify_path(node)
        nuke.scriptSaveAs('{}/{}'.format(self.dest_root,
                                         os.path.basename(nuke.Root().name())),
                          1)

        # Restore original nk file to let users continue to do their jobs.
        nuke.scriptClear()
        nuke.scriptOpen(self.original_nk)
