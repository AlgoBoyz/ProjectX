import pdb

import maya.cmds as mc
from .MConstant import Sign
from .MBaseFunctions import get_list_types


class MNode(object):
    _CREATE_STR = 'MNodeBase'

    def __init__(self, name):
        if isinstance(name, self.__class__):
            print(f'Initializing from {self.__class__}')
            self.name = name.name
        else:
            self.name = name
        self.__check_exist()

    def __repr__(self):
        return f'{self.__class__.__name__} object in name of :{self.name}'

    def __getattr__(self, item):
        return MAttribute(self.name, item)

    def __str__(self):
        return self.name

    def __check_exist(self):
        if '.' in self.name:
            raise RuntimeError(f'Wrong format of node name:{self.name}')
        exist = mc.objExists(self.name)
        if not self.name:
            raise RuntimeError(f'Node name can not be empty!')
        if not exist:
            raise RuntimeError(f'Node:{self.name} do not exist!')

    @classmethod
    def create(cls, name=None, **kwargs):
        if not name:
            name = cls._CREATE_STR
        node = mc.createNode(cls._CREATE_STR, name=name)
        under = kwargs.pop('under', None)
        match = kwargs.pop('match', None)
        pos = kwargs.pop('posisition', kwargs.pop('pos', None))
        if kwargs:
            raise ValueError(f'Parameter:{kwargs} is not supported!')
        if under:
            if isinstance(under, str):
                mc.parent(node, under)
            elif isinstance(under, cls):
                mc.parent(node, under.name)
        if match:
            pass
        return cls(node)

    @property
    def connected_attrs(self, **kwargs):
        connected = mc.listConnections(self.name, **kwargs)
        if connected:
            return connected
        else:
            return None

    @property
    def history(self):
        return mc.listHistory(self.name)

    def add_attr(self, attr_name: str, **kwargs):
        mc.addAttr(self.name, **kwargs)
        return MAttribute(self.name, attr_name)

    def add_to_set(self, set_name):
        pass

    def rename(self, new_name):
        mc.rename(self.name, new_name)


class MAttribute(object):

    def __init__(self, node, attr_name):
        self.node = node
        self.attr_name = attr_name
        self.full_name = f'{self.node}.{self.attr_name}'
        self.__check_exist()

    def __repr__(self):
        return f'MAttribue: {self.full_name}'

    def __str__(self):
        return self.full_name

    def __check_exist(self):
        exist = mc.objExists(self.full_name)
        if not exist:
            raise AttributeError(f'Attribute:{self.full_name} do not exist!')

    @staticmethod
    def validate_attr(attr: str):
        if '.' not in attr:
            raise AttributeError(f'Wrong format of attribute:{attr}')
        if not mc.objExists(attr):
            raise AttributeError(f'Attibute:{attr} do not exist')
        splited = attr.split('.')
        if not splited or len(splited) != 2:
            raise AttributeError(f'Wrong format of attribute:{attr}')
        return splited

    @classmethod
    def create_by_name(cls, full_name: str):
        splited = cls.validate_attr(full_name)
        return cls(splited[0], splited[1])

    @property
    def value(self):
        v = mc.getAttr(self.full_name)
        if isinstance(v, tuple) or isinstance(v, list) and len(v) == 1:
            return v[0]
        else:
            return v

    @property
    def sign(self):
        if not self.attr_type in ['float', 'double', 'int']:
            return None
        if self.value > 0:
            return Sign.Positive
        elif self.value == 0:
            return Sign.Zero
        elif self.value < 0:
            return Sign.Negative
        else:
            return None

    @property
    def attr_type(self):
        t = mc.getAttr(self.full_name, type=True)
        # print(f'{self.full_name}--Attribute type:{t}')
        return t

    def connect(self, other, force=False):
        other_node = ''
        if isinstance(other, str):
            node, attr = self.validate_attr(other)
            other_node = node
            mc.connectAttr(self.full_name, other, force=force)
            print(f'{self.full_name}>>{other}')
        elif isinstance(other, MAttribute):
            mc.connectAttr(self.full_name, other.full_name, force=force)
            other_node = other.node
            print(f'{self.full_name}>>{other.full_name}')
        elif isinstance(other, list):
            other_type = get_list_types(other)
            if not other_type != str and other_type != MAttribute:
                raise AttributeError(f'Wrong format of list of attibutes:{other}')
            for attr in other:
                self.connect(attr, force=force)
        else:
            raise RuntimeError(f'Not supported attibute to connect')
        return other_node

    def disconnect(self):
        pass

    def set(self, value):
        if isinstance(value, MAttribute):
            value = value.value
        if self.attr_type in ['float3', 'double3']:
            mc.setAttr(self.full_name, *value)
        else:
            mc.setAttr(self.full_name, value)
