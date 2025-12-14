import enum

import os
import sys

PROJECT_BASE_DIR = os.path.dirname(os.path.dirname(__file__))
print(PROJECT_BASE_DIR)


class Sign(enum.Enum):
    Negative = -1
    Zero = 0
    Positive = 1


class ConditionOperation(object):
    Equal = 0
    NotEqual = 1
    GreaterThan = 2
    GreaterOrEqual = 3
    LessThan = 4
    LessOrEqual = 5


class ControllerPrototype(object):
    Cube = 0
    Circle = 1
    ForwardCircle = 2
    SquareCircle = 3


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

    ValueType = ['long', 'short', 'float', 'double', 'doubleAngle', 'doubleLinear', 'enum']
    CompoundType = ['float3', 'double3']


class ParentType(object):
    point_constraint = 'point_constraint'
    hierarchy = 'hierarchy'
    parent_constraint = 'parent_constraint'


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
    IdentityMat = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 0]]


class GlobalConfig(object):
    transform_root = ''
    locator_root = ''

    attrs = ['transform_root', 'locator_root']

    @classmethod
    def set_root(cls, root):
        for attr_name in cls.attrs:
            setattr(cls, attr_name, root)

    @classmethod
    def reset_root(cls):
        for attr_name in cls.attrs:
            setattr(cls, attr_name, '')

    SUPPORTED_DICT = {
        'scalar*raw_scalar': 'multDoubleLinear',  # 常数*单通道属性
        'scalar*scalar': 'multDoubleLinear',  # 单通道*单通道

        'scalar*raw_vector': 'multiplyDivide',  # 单通道属性*向量

        'vector*raw_scalar': 'multiplyDivide',  # 常数*向量属性

        'vector*scalar': 'multiplyDivide',  # 单通道属性*向量属性

        'vector*vector': 'vectorProduct',

        'raw_scalar*matrix': NotImplemented,  # 暂时没想到用处，需要的时候再写

        'matrix*vector': NotImplemented  # 矩阵左乘向量，之后也许会用到

    }
    if sys.version_info.minor == 11:
        SUPPORTED_DICT['vector*vector'] = 'dotProduct'
