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

    @property
    def default_value(self):
        dv = mc.addAttr(self.full_name, q=True, dv=True)
        return dv

    def mount(self, other, force=True, inverse=False):
        """
        挂载属性，可以挂载常数，常数列表，亦可挂载另一个属性，或者一个属性列表
        基本上就是将connectAttr跟setAttr合并起来，方便后续节点图的编写
        """
        if isinstance(other, str):
            if not mc.objExists(other):
                raise RuntimeError(f'Can not connect attribute:{self.full_name} to {other}(do not exist)!')
            if inverse:
                mc.connectAttr(other, self.full_name, force=force)
            else:
                mc.connectAttr(self.full_name, other, force=force)
            logging.info(f'{self.full_name}>>{other}')
        elif isinstance(other, MAttribute):
            if inverse:
                mc.connectAttr(other.full_name, self.full_name, force=force)
            else:
                mc.connectAttr(self.full_name, other.full_name, force=force)
            logging.info(f'{self.full_name}>>{other.full_name}')
        elif isinstance(other, list):
            other_type = get_list_types(other)
            if other_type == str:
                for attr in other:
                    if not mc.objExists(attr):
                        raise RuntimeError(f'Attribute{attr} in attribute list:{other} do not exists!')
                    mc.connectAttr(self.full_name, attr, force=force)
                    logging.info(f'{self.full_name}>>{attr}')
            elif other_type == int or other_type == float:
                if not self.attr_type in AttrType.CompoundType:
                    raise RuntimeError(f'Single value attribute can not be set to {other}')
                mc.setAttr(self.full_name, *other, type=self.attr_type)
                logging.info(f'{self.full_name}>>{other}')
            else:
                raise RuntimeError(f'Not supported attribute list:{other}')
        elif isinstance(other, int) or isinstance(other, float):
            if self.attr_type in AttrType.ValueType:
                mc.setAttr(self.full_name, other)
                logging.info(f'{self.full_name}>>{other}')
            elif self.attr_type in AttrType.CompoundType:
                other = [other, other, other]
                mc.setAttr(self.full_name, *other, type=self.attr_type)
                logging.info(f'{self.full_name}>>{other}')
            else:
                raise RuntimeError(
                    f'Not value type attribute{self.full_name}({self.attr_type}) can not be set to:{other}')
        else:
            raise RuntimeError(f'Not supported attribute to connect')

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

    def reset(self):
        single_axis_attrs = ['translateX', 'translateY', 'translateZ',
                             'rotateX', 'rotateY', 'rotateZ',
                             'tx', 'ty', 'tz',
                             'rx', 'ry', 'rz']
        single_axis_attrs2 = ['scaleX', 'scaleY', 'scaleZ', 'sx', 'sy', 'sz']
        if self.attr_name in ['translate', 'rotate', 't', 'r']:
            self.set([0, 0, 0])
        elif self.attr_name in ['scale', 's']:
            self.set([1, 1, 1])

        elif self.attr_name in single_axis_attrs:
            self.set(0)
        elif self.attr_name in single_axis_attrs2:
            self.set(1)
        elif self.attr_name in ['v', 'visibility']:
            self.set(1)
        else:
            self.set(self.default_value)

    def set_driven_key(self, driver_attr, driver_val, driven_val):
        driver_attr = driver_attr.full_name if isinstance(driver_attr, MAttribute) else driver_attr
        mc.setDrivenKeyframe(self.full_name,
                             currentDriver=driver_attr,
                             driverValue=driver_val,
                             value=driven_val)

    def lock(self, hide=True):
        channel_box = True if not hide else False
        mc.setAttr(self.full_name, lock=True, channelBox=channel_box)


def get_handler(value):
    if isinstance(value, int) or isinstance(value, float):
        return ConstantHandler(value)
    elif isinstance(value, list) or isinstance(value, tuple):
        return ListHandler(value)
    elif isinstance(value, str):
        return StringHandler(value)
    elif isinstance(value, MAttribute):
        return MAttributeHandler(value)
    else:
        raise RuntimeError(f'Unrecognized attribute type:{value}')


class ConstantHandler(object):
    def __init__(self, value, to_mount: MAttribute):
        self.value = value
        self.to_mount = to_mount

    def mount(self):
        if not self.to_mount.attr_type in AttrType.ValueType:
            if not self.to_mount.attr_type in AttrType.CompoundType:
                logging.error(f'ConstantHandler:Not matched type:{self.to_mount.attr_type}')
                raise RuntimeError(f'Can not mount value:{self.value} to attribute:{self.to_mount.full_name}')
            value = [self.value, self.value, self.value]
            self.to_mount.set(value)
            return True
        self.to_mount.set(self.value)
        return True


class StringHandler(object):
    def __init__(self, value, to_mount: MAttribute):
        self.value = value
        self.to_mount = to_mount

    def mount(self):
        if self.to_mount.attr_type == AttrType.String:
            self.to_mount.set(self.value)
            return True
        if '.' in self.value:
            exist = mc.objExists(self.value)
            if exist:
                mc.connectAttr(self.value, self.to_mount.full_name)
                return True
            else:
                logging.error(f'StringHandler:Try to connect a not exist attribute:{self.value}')
                raise RuntimeError(f'Failed to connect to {self.value},attribute do not exist')
        else:
            raise RuntimeError(f'Unrecognized Attribute:{self.value}')


class ListHandler(object):
    def __init__(self, value, to_mount: MAttribute):
        self.value = value
        self.to_mount = to_mount

    def mount(self):
        lst_type = get_list_types(self.value)
        if lst_type == int or lst_type == float:
            if self.to_mount.attr_type in AttrType.CompoundType:
                self.to_mount.set(self.value)
            else:
                raise RuntimeError(f'Failed to mount{self.value} to {self.to_mount.full_name}')
        elif lst_type == str:
            for attr in self.value:
                if not mc.objExists(attr):
                    logging.error(f'ListHandler:Attribute:{attr} in {self.value} do not exist!')
                    raise RuntimeError(f'Attribute:{attr} in {self.value} do not exist!')
                mc.connectAttr(attr, self.to_mount.full_name)


class MAttributeHandler(object):
    def __init__(self, value):
        self.value = value
