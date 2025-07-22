import logging

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
        if not self.attr_type in AttrType.ValueType:
            logging.warning(f'{self.full_name} do not have sign!')
        if self.value > 0:
            return Sign.Positive
        elif self.value == 0:
            return Sign.Zero
        elif self.value < 0:
            return Sign.Negative
        else:
            return None

    def mount(self, other, force=False):
        """
        other:常数，字符串，字符串列表，数值列表，MAttribute
        """
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
            if other_type == str:
                for attr in other:
                    if not mc.objExists(attr):
                        raise RuntimeError(f'Attribute{attr} in attribute list:{other} do not exists!')
                    mc.connectAttr(self.full_name,attr)
            elif other_type == int or other_type == float:
                mc.setAttr(self.full_name,other,type=self.attr_type)
            else:
                raise RuntimeError(f'Not supported attribute list:{other}')
        elif isinstance(other,int) or isinstance(other,float):
            if self.attr_type in AttrType.ValueType:
                mc.setAttr(self.full_name,other)
            elif self.attr_type in AttrType.CompoundType:
                other = [other,other,other]
                mc.setAttr(self.full_name,other,type=self.attr_type)

        else:
            raise RuntimeError(f'Not supported attribute to connect')
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

    def set_driven_key(self, driver_attr, driver_val, driven_val):
        driver_attr = driver_attr.full_name if isinstance(driver_attr, MAttribute) else driver_attr
        mc.setDrivenKeyframe(self.full_name,
                             currentDriver=driver_attr,
                             driverValue=driver_val,
                             value=driven_val)

