from imp import reload

import sys

import maya.cmds as mc
from .MNodes import MNode, MAttribute


class VitualMathNode(object):
    __slots__ = ['matrixIn', 'matrixSum', 'matrixSum', 'inputMatrix', 'inputRotateOrder', 'outputTranslate',
                 'outputTranslateX',
                 'outputTranslateY', 'outputTranslateZ', 'outputRotate', 'outputRotateX', 'outputRotateY',
                 'outputRotateZ', 'outputScale', 'outputScaleX', 'outputScaleY', 'outputScaleZ', 'outputShear',
                 'outputShearX', 'outputShearY', 'outputShearZ', 'outputQuat', 'outputQuatX', 'outputQuatY',
                 'outputQuatZ', 'outputQuatW', 'outputQuatW', 'binMembership', 'input1', 'input2', 'output', 'output',
                 'binMembership', 'output', 'operation', 'input1X', 'input1Y', 'input1Z', 'input2X', 'input2Y',
                 'input2Z', 'outputX', 'outputY', 'outputZ', 'outputZ', 'binMembership', 'binMembership', 'firstTerm',
                 'secondTerm', 'colorIfTrue', 'colorIfTrueR', 'colorIfTrueG', 'colorIfTrueB', 'colorIfFalse',
                 'colorIfFalseR', 'colorIfFalseG', 'colorIfFalseB', 'outColor', 'outColorR', 'outColorG', 'outColorB',
                 'outColorB', 'inputValue', 'inputMin', 'inputMax', 'outputMin', 'outputMax', 'value', 'color',
                 'outValue', 'outColorB', 'valueX', 'valueY', 'valueZ', 'min', 'minX', 'minY', 'minZ', 'max', 'maxX',
                 'maxY', 'maxZ', 'oldMin', 'oldMinX', 'oldMinY', 'oldMinZ', 'oldMax', 'oldMaxX', 'oldMaxY', 'oldMaxZ',
                 'outValueX', 'outValueY', 'outValueZ', 'outValueZ', 'output']


class MathNode(VitualMathNode):

    def __init__(self, name):
        if name is None:
            raise RuntimeError(f'Can not initialize from None')
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


class addDoubleLinear(MathNode):
    _CREATE_STR = 'addDoubleLinear'

    if sys.version_info.minor == 11:
        _CREATE_STR = 'addDL'

    def __init__(self, name):
        super().__init__(name)


class multDoubleLinear(MathNode):
    _CREATE_STR = 'multDoubleLinear'

    if sys.version_info.minor == 11:
        _CREATE_STR = 'multDL'

    def __init__(self, name):
        super().__init__(name)
        self.sss = ''


class multiplyDivide(MathNode):
    _CREATE_STR = 'multiplyDivide'

    def __init__(self, name):
        super().__init__(name)


class floatMath(MathNode):
    _CREATE_STR = 'floatMath'

    def __init__(self, name):
        super().__init__(name)


class condition(MathNode):
    _CREATE_STR = 'condition'

    def __init__(self, name):
        super().__init__(name)


class decomposeMatrix(MathNode):
    _CREATE_STR = 'decomposeMatrix'

    def __init__(self, name):
        super().__init__(name)


class multMatrix(MathNode):
    _CREATE_STR = 'multMatrix'
    __slots__ = ['multMatrix', 'message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState',
                 'binMembership', 'matrixIn', 'matrixSum']

    def __init__(self, name):
        super().__init__(name)


class colorMath(MathNode):
    _CREATE_STR = 'colorMath'

    def __init__(self, name):
        super().__init__(name)


class dotProduct(MathNode):
    _CREATE_STR = 'dotProduct'

    def __init__(self, name):
        super().__init__(name)


class setRange(MathNode):
    _CREATE_STR = 'setRange'

    def __init__(self, name):
        super().__init__(name)


class remapValue(MathNode):
    _CREATE_STR = 'remapValue'

    def __init__(self, name):
        super().__init__(name)
