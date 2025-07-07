import enum

import os

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


class AttrType(object):
    Message = 'message'
    Byte = 'byte'
    Tdatacompound = 'TdataCompound'
    Matrix = 'matrix'

    Bool = 'bool'
    Enum = 'enum'
    String = 'string'
    Short = 'short'
    Long = 'long'
    Int32array = 'Int32Array'

    Float = 'float'
    Float2 = 'float2'
    Float3 = 'float3'
    Double = 'double'
    Doubleangle = 'doubleAngle'
    Doublelinear = 'doubleLinear'
    Double3 = 'double3'

    ValueType = ['long', 'short', 'float', 'double', 'doubleAngle', 'doubleLinear']
    CompundType = ['float3', 'double3', 'matrix']


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


class WorldUpType(enum.Enum):
    Scene = 'scene'
    Object = 'object'
    Objectrotation = 'objectrotation'
    Vector = 'vector'
    none = 'none'


class Matrix(enum.Enum):
    IndentityMat = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0]]
