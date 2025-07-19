from typing import Iterator

import maya.cmds as mc
from XBase.MNodes import MNode


class MNodeGraph(object):
    pass


class MFormula(object):
    """
    x.rx+y.rz+z.tx
    x.ty
    """

    def __init__(self):
        self.nodes = []

    def __getitem__(self, idx) -> 'MNode':
        return self.nodes[idx]

    def __iter__(self) -> Iterator['MNode']:
        return iter(self.nodes)

    def register(self):
        pass

    def execute(self):
        pass

    def get_node_from_type(self):
        pass

    def get_node_from_name(self):
        pass

    def insert(self, idx,in_attr,out_attr):
        pass


class MGraphCommand(object):

    def __init__(self):
        pass
