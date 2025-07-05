import os
import sys
from importlib import reload

import maya.cmds as mc


def get_all_nodes():
    txt_path = rf'{os.path.dirname(__file__)}/Nodes.txt'
    node_names = []
    with open(txt_path, 'r') as f:
        for line in f:
            if len(line.strip()) < 2:
                continue
            node_names.append(line.strip())

    return node_names


def build_class(node_name, attrs):
    class_str = (f'class {node_name}(object):\n'
                 f'    __slots__ = {str(attrs)}')

    return class_str


def dev():
    attrs_out = []
    for node_name in get_all_nodes():
        node = mc.createNode(node_name)
        attrs = mc.listAttr(node)
        for attr in attrs:
            if attr in attrs_out or '.' in attr:
                continue
            # try:
            #     at_type = mc.getAttr(f'{node}.{attr}', type=True)
            #     if not at_type in attrs_out:
            #         attrs_out.append(at_type)
            # except:
            #     print(f'Failed to get {node}.{attr}')
            attrs_out.append(attr)
    print(attrs_out)
    return attrs_out


if __name__ == "__main__":
    pass
