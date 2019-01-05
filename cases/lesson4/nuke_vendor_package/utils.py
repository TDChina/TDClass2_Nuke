"""Module includes helper functions to work with Nuke node tree."""

# Import built-in modules
import os

# Import third-party modules
import nuke

# Import local modules
from nuke_vendor_package import constants


def get_all_nodes(node_class=None):
    """Get all nodes from Nuke node tree, return nodes with specific
       class if node_class parameter been set.

    Args:
        node_class (str): Node class name. If set None then get all nodes from
            node tree.

    Return:
        :obj: `list` of :obj: `nuke.Node`: All needed nodes.

    """
    if node_class:
        return nuke.allNodes(node_class, recurseGroups=True)
    else:
        return nuke.allNodes(recurseGroups=True)


def get_read_nodes():
    """Get list of specific nodes that have file knob.

    Return:
        :obj: `list` of :obj: `nuke.Node`: All specific nodes with file knob.

    """
    nodes = []
    for node_class in constants.READ_CLASSES:
        nodes.extend(get_all_nodes(node_class))
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
