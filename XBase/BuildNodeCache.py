import os
import sys
from importlib import reload
from XBase.MConstant import PROJECT_BASE_DIR
import maya.cmds as mc
from maya.internal.nodes.blendfalloff.action import PRIMITIVE_ICON

txt_path = rf'{os.path.dirname(__file__)}/Nodes.txt'
math_node_path = os.path.join(PROJECT_BASE_DIR, 'XBase', 'MathNodes')


def get_all_nodes(path):
    node_names = []
    with open(path, 'r') as f:
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
    for node_name in get_all_nodes(txt_path):
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


def build_math_node_cache():
    import XBase.MMathNode as mm
    attrs_out = []
    for node_name in get_all_nodes(math_node_path):
        node = mc.createNode(node_name)
        print(f'Node:{node} created!')
        attrs = mc.listAttr(node)
        for attr in attrs:
            if attr in attrs_out or '.' in attr:
                continue
            attrs_out.append(attr)
        attrs_out.append(attr)
    return attrs_out


if __name__ == "__main__":
    pass
