import enum

import os
from re import split
from PySide6.QtWidgets import QLineEdit, QSpinBox

PROJECT_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
print(PROJECT_BASE_DIR)


class Sign(enum.Enum):
    Negative = -1
    Zero = 0
    Positive = 1


class ConditionOperation(enum.Enum):
    Equal = 0
    NotEqual = 1
    GreaterThan = 3
    GreaterOrEqual = 4
    LessThan = 5
    LessOrEqual = 6


class AttributeTypes(enum.Enum):
    float3 = 'float3'
    short2 = 'short2'
    short3 = 'short3'
    long2 = 'long2'


class XSpace(object):
    transform_root = ''
    joint_root = ''
    locator_root = ''
    attrs = ['transform_root', 'joint_root', 'locator_root']

    @classmethod
    def set_root(cls, root):
        for attr_name in cls.attrs:
            setattr(cls, attr_name, root)

    @classmethod
    def reset_root(cls):
        for attr_name in cls.attrs:
            setattr(cls, attr_name, '')


class Axis(enum.Enum):
    X = (1, 0, 0)
    Y = (0, 1, 0)
    Z = (0, 0, 1)

    NX = (-1, 0, 0)
    NY = (0, -1, 0)
    NZ = (1, 0, -1)

    XY = (0, 0, 1)
    XZ = (0, 1, 0)
    YZ = (1, 0, 0)
