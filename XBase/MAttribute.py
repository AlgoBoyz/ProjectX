import logging
from xml.sax.saxutils import XMLFilterBase

import maya.cmds as mc

from XBase.MBaseFunctions import get_list_types
from XBase.MConstant import AttrType, Sign


class MAttribute(object):
    VALUE_ACCURACY = 5  # 数值精确到小数点后几位

    def __init__(self, node, attr_name):
        self.node = node
        self.attr_name = attr_name
        self.full_name = f'{self.node}.{self.attr_name}'
        self.__check_exist()
        self.attr_type = mc.getAttr(self.full_name, type=True)

    def __repr__(self):
        return f'MAttribute: {self.full_name}'

    def __str__(self):
        return self.full_name

    def __getitem__(self, item):
        if not self.attr_type in ['matrix', 'double3']:
            raise RuntimeError(f'{self.attr_type} do not support index operation')
        try:
            res = mc.getAttr(f'{self.full_name}[{item}]')
        except Exception as e:
            logging.error(e)

    def __check_exist(self):
        exist = mc.objExists(self.full_name)
        if not exist:
            raise AttributeError(f'Attribute:({mc.objectType(self.node)}){self.full_name} do not exist!')

    @classmethod
    def create_by_name(cls, full_name: str):
        name, attr = full_name.split('.', maxsplit=1)
        if not mc.objExists(full_name):
            raise RuntimeError(f'{full_name} do not exist')
        return cls(name, attr)

    @property
    def value(self):
        v = mc.getAttr(self.full_name)
        if isinstance(v, tuple) or isinstance(v, list):
            lst_type = get_list_types(v)
            if lst_type == float:
                res = [round(i, self.VALUE_ACCURACY) for i in v]
                return res[0] if len(res) == 1 else res
            elif lst_type == list or lst_type == tuple and len(v) == 1:
                res = [round(i, self.VALUE_ACCURACY) for i in v[0]]
                return res
            else:
                return v
        else:
            return round(v, self.VALUE_ACCURACY) if isinstance(v, float) else v

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

    def connect(self, other, force=False):
        other_node = ''
        if isinstance(other, str):
            if not mc.objExists(other):
                raise RuntimeError(f'Can not connect attribute:{self.full_name} to {other}(do not exist)!')
            mc.connectAttr(self.full_name, other, force=force)
            logging.info(f'{self.full_name}>>{other}')
        elif isinstance(other, MAttribute):
            mc.connectAttr(self.full_name, other.full_name, force=force)
            other_node = other.node
            logging.info(f'{self.full_name}>>{other.full_name}')
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
        if isinstance(value, int) and self.attr_type in ['double', 'float', 'doubleLinear', 'doubleAngle']:
            logging.info(f'Assigning an int({value}) to a float or double ,convert the value to {float(value)}')
            value = float(value)
        if isinstance(value, MAttribute):
            value = value.value
        if self.attr_type in ['float3', 'double3', 'float2']:
            mc.setAttr(self.full_name, *value)
        elif self.attr_type in ['matrix']:
            mc.setAttr(self.full_name, value, type=self.attr_type)
        else:
            mc.setAttr(self.full_name, value)

    def get(self, raw=True):
        if raw:
            return mc.getAttr(self.full_name)
        else:
            return self.value

    def add(self, other, alias):
        pass

    def subtract(self, other, alias):
        pass

    def multiply(self, other, alias):
        pass

    def distance_to(self, other, alias):
        from XBase.MMathNode import distanceBetween
        dist_node = distanceBetween.create(f'{alias}_dist')
        dist_node.quick_connect(self, other)
        return dist_node

    def set_driven_key(self, driver_attr, driver_val, driven_val):
        driver_attr = driver_attr.full_name if isinstance(driver_attr, MAttribute) else driver_attr
        mc.setDrivenKeyframe(self.full_name,
                             currentDriver=driver_attr,
                             driverValue=driver_val,
                             value=driven_val)

    def as_condition(self, color_true, color_false):
        pass
