from typing import Iterator

import maya.cmds as mc
from XBase.MNodes import MNode
from XBase.MAttribute import MAttribute
from XBase.MConstant import AttrType

class AttributeOperation(object):

    def __init__(self):
        pass

    @staticmethod
    def _parse_attr_type(*args):
        attr_type = []
        for i in args:
            if isinstance(i, float) or isinstance(i, int):
                attr_type.append('raw_scalar')
                continue
            elif isinstance(i, list) or isinstance(i, tuple):
                attr_type.append('raw_vector')
                continue

            mattr = None
            if isinstance(i, str):
                mattr = MAttribute.create_by_name(i)
            elif isinstance(i, MAttribute):
                mattr = i

            if not mattr:
                raise RuntimeError(f'Unrecognized attribute:{i}({mattr.attr_type})')

            if mattr.attr_type in AttrType.ValueType:
                attr_type.append('scalar')
            elif mattr.attr_type in AttrType.CompoundType:
                attr_type.append('vector')
            elif mattr.attr_type == 'matrix':
                attr_type.append('matrix')
            else:
                raise RuntimeError(f'Unrecognized attribute:{i}({mattr.attr_type})')
        return attr_type

    def multiply(self,attr1,attr2):
        pass

    def subtract(self,attr1,attr2):
        pass

    def divide(self,attr1,att2):
        pass

    def add(self,attr1,attr2):
        pass

    def distance_to(self):
        pass

    def as_condition(self):
        pass

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