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
    for node_name in get_all_nodes():
        node = mc.createNode(node_name)
        attrs = mc.listAttr(node, connectable=True)
        short_attrs = mc.listAttr(node, shortNames=True, connectable=True)
        attrs.extend(short_attrs)
        valid_attrs = [i for i in attrs if '.' not in i]
        res = build_class(node_name, valid_attrs)
        mc.delete(node)
        print(res)


if __name__ == "__main__":
    pass
