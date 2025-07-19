import pdb
from imp import reload

import sys

import maya.cmds as mc
from .MNodes import MNode, MAttribute


class VitualMathNode(object):
    __slots__ = ['input1', 'input2', 'output', 'operation', 'input1X', 'input1Y', 'input1Z', 'input2X', 'input2Y',
                 'input2Z', 'outputX', 'outputY', 'outputZ', 'floatA', 'floatB', 'outFloat', 'firstTerm', 'secondTerm',
                 'colorIfTrue', 'colorIfTrueR', 'colorIfTrueG', 'colorIfTrueB', 'colorIfFalse', 'colorIfFalseR',
                 'colorIfFalseG', 'colorIfFalseB', 'outColor', 'outColorR', 'outColorG', 'outColorB', 'inputMatrix',
                 'inputRotateOrder', 'outputTranslate', 'outputTranslateX', 'outputTranslateY', 'outputTranslateZ',
                 'outputRotate', 'outputRotateX', 'outputRotateY', 'outputRotateZ', 'outputScale', 'outputScaleX',
                 'outputScaleY', 'outputScaleZ', 'outputShear', 'outputShearX', 'outputShearY', 'outputShearZ',
                 'outputQuat', 'outputQuatX', 'outputQuatY', 'outputQuatZ', 'outputQuatW', 'matrixIn', 'matrixSum',
                 'colorA', 'colorAR', 'colorAG', 'colorAB', 'alphaA', 'colorB', 'colorBR', 'colorBG', 'colorBB',
                 'alphaB', 'outAlpha', 'matrix', 'normalizeOutput', 'value', 'valueX', 'valueY', 'valueZ', 'min',
                 'minX', 'minY', 'minZ', 'max', 'maxX', 'maxY', 'maxZ', 'oldMin', 'oldMinX', 'oldMinY', 'oldMinZ',
                 'oldMax', 'oldMaxX', 'oldMaxY', 'oldMaxZ', 'outValue', 'outValueX', 'outValueY', 'outValueZ',
                 'inputValue', 'inputMin', 'inputMax', 'outputMin', 'outputMax', 'value_Position', 'value_FloatValue',
                 'value_Interp', 'color', 'color_Position', 'color_Color', 'color_ColorR', 'color_ColorG',
                 'color_ColorB', 'color_Interp', 'input', 'inputX', 'inputY', 'inputZ', 'point1', 'point1X', 'point1Y',
                 'point1Z', 'inMatrix1', 'point2', 'point2X', 'point2Y', 'point2Z', 'inMatrix2', 'distance']


class MathNode(VitualMathNode):
    _CREATE_STR = 'VitualMathNode'

    def __init__(self, name):

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
        if mc.nodeType(node) == 'unknown':
            raise RuntimeError(f'Failed to create node:{name},type:{cls._CREATE_STR}')
        return cls(node)

    def attr(self, attr_name):
        return MAttribute(self.name, attr_name)


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


class vectorProduct(MathNode):
    _CREATE_STR = 'vectorProduct'

    def __init__(self, name):
        super().__init__(name)

    def dot(self, other1, other2):
        self.operation.set(1)
        normal_node1 = normalize.create(f'{other1.name}_normalize')
        normal_node2 = normalize.create(f'{other2.name}_normalize')
        other1.outColor.connect(normal_node1.input)
        other2.outColor.connect(normal_node2.input)
        normal_node1.output.connect(self.input1)
        normal_node2.output.connect(self.input2)


class setRange(MathNode):
    _CREATE_STR = 'setRange'

    def __init__(self, name):
        super().__init__(name)


class remapValue(MathNode):
    _CREATE_STR = 'remapValue'

    def __init__(self, name):
        super().__init__(name)


class normalize(MathNode):
    _CREATE_STR = 'normalize'

    def __init__(self, name):
        super().__init__(name)


class distanceBetween(MathNode):
    _CREATE_STR = 'distanceBetween'

    def __init__(self, name):
        super().__init__(name)
        self.out_plug = self.distance

    def quick_connect(self, point1, point2):
        self.set_point(1, point1)
        self.set_point(2, point2)

    def set_point(self, idx, point):
        target_attr = self.attr(f'point{idx}')
        if isinstance(point, list) or isinstance(point, tuple):
            if not len(point) == 3:
                raise RuntimeError(f'Not legal point({point}) to calculate distance.')
            target_attr.set(point)
        if isinstance(point, str):
            point = MAttribute.create_by_name(point)
        point.connect(target_attr)


class Mmultiply(object):
    # todo 1：自动适应maya版本，选择不同的节点
    # todo 2：自动根据数值，挑选合适的节点类型进行创建
    # todo 3: 自动连接属性

    def __init__(self):
        pass

    def create(self, name):
        pass
