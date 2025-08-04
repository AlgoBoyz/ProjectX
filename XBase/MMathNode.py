import logging
import pdb
from imp import reload

import sys

import maya.cmds as mc

from XBase.MConstant import AttrType
from XBase.MAttribute import MAttribute


class VirtualMathNode(object):
    __slots__ = ['input1', 'input2', 'output', 'operation', 'input1X', 'input1Y', 'input1Z', 'input2X', 'input2Y',
                 'input2Z', 'outputX', 'outputY', 'outputZ', 'floatA', 'floatB', 'outFloat', 'firstTerm', 'secondTerm',
                 'colorIfTrue', 'colorIfTrueR', 'colorIfTrueG', 'colorIfTrueB', 'colorIfFalse', 'colorIfFalseR',
                 'colorIfFalseG', 'colorIfFalseB', 'outColor', 'outColorR', 'outColorG', 'outColorB', 'inputMatrix',
                 'inputRotateOrder', 'outputTranslate', 'outputTranslateX', 'outputTranslateY', 'outputTranslateZ',
                 'outputRotate', 'outputRotateX', 'outputRotateY', 'outputRotateZ', 'outputScale', 'outputScaleX',
                 'outputScaleY', 'outputScaleZ', 'outputShear', 'outputShearX', 'outputShearY', 'outputShearZ',
                 'outputQuat', 'outputQuatX', 'outputQuatY', 'outputQuatZ', 'outputQuatW', 'matrixIn', 'matrixSum',
                 'colorA', 'colorAR', 'colorAG', 'colorAB', 'alphaA', 'colorB', 'colorBR', 'colorBG', 'colorBB',
                 'alphaB', 'outAlpha', 'blender', 'color1', 'color1R', 'color1G', 'color1B', 'color2', 'color2R',
                 'color2G', 'color2B', 'renderPassMode', 'outputR', 'outputG', 'outputB', 'matrix', 'normalizeOutput',
                 'value', 'valueX', 'valueY', 'valueZ', 'min', 'minX', 'minY', 'minZ', 'max', 'maxX', 'maxY', 'maxZ',
                 'oldMin', 'oldMinX', 'oldMinY', 'oldMinZ', 'oldMax', 'oldMaxX', 'oldMaxY', 'oldMaxZ', 'outValue',
                 'outValueX', 'outValueY', 'outValueZ', 'inputValue', 'inputMin', 'inputMax', 'outputMin', 'outputMax',
                 'value_Position', 'value_FloatValue', 'value_Interp', 'color', 'color_Position', 'color_Color',
                 'color_ColorR', 'color_ColorG', 'color_ColorB', 'color_Interp', 'input', 'inputX', 'inputY', 'inputZ',
                 'point1', 'point1X', 'point1Y', 'point1Z', 'inMatrix1', 'point2', 'point2X', 'point2Y', 'point2Z',
                 'inMatrix2', 'distance']


class MathNode(VirtualMathNode):
    _CREATE_STR = 'VirtualMathNode'

    def __init__(self, name, *args, **kwargs):

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

    def quick_connect(self, *args, **kwargs):
        return NotImplemented


class addDoubleLinear(MathNode):
    _CREATE_STR = 'addDoubleLinear'
    ALIAS = 'adl'
    if sys.version_info.minor == 11:
        _CREATE_STR = 'addDL'

    def __init__(self, name):
        super().__init__(name)


class multDoubleLinear(MathNode):
    _CREATE_STR = 'multDoubleLinear'
    ALIAS = 'mdl'
    if sys.version_info.minor == 11:
        _CREATE_STR = 'multDL'

    def __init__(self, name):
        super().__init__(name)


class multiplyDivide(MathNode):
    _CREATE_STR = 'multiplyDivide'

    ALIAS = 'mldv'
    MULTIPLY = 1
    DIVIDE = 2
    POWER = 3

    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)

    @classmethod
    def create(cls, name=None, **kwargs):
        instance = super().create(name)
        operation = kwargs.pop('operation', 1)
        instance.operation.set(operation)
        return cls(instance.name)

    def quick_connect(self, *args, **kwargs):
        """
        args: input1,input2
        kwargs:operation
        """
        operation = kwargs.pop('operation', 1)
        self.operation.set(operation)
        if not len(args) == 2:
            logging.error(f'multiplyDivide:Require 2 input,got {args} instead.')
        for i, attr_in in enumerate(args):
            target_attr = MAttribute(self.name, f'input{i + 1}')
            if isinstance(attr_in, int) or isinstance(attr_in, float):
                for axis in ['X', 'Y', 'Z']:
                    mc.setAttr(f'{target_attr.full_name}{axis}', attr_in)
            elif isinstance(attr_in, list) or isinstance(attr_in, tuple):
                if not len(attr_in) == 3:
                    logging.error(
                        f'multiplyDivide:Require list or tuple in length of 3,got {attr_in}({len(attr_in)}) instead')
                    raise RuntimeError(
                        f'multiplyDivide:Require list or tuple in length of 3,got {attr_in}({len(attr_in)}) instead')
                target_attr.set(attr_in)
            elif isinstance(attr_in, str):
                mattr = MAttribute.create_by_name(attr_in)
                mattr.connect(target_attr)
            elif isinstance(attr_in, MAttribute):
                attr_in.mount(target_attr)


class floatMath(MathNode):
    _CREATE_STR = 'floatMath'
    ALIAS = 'flm'

    def __init__(self, name):
        super().__init__(name)


class condition(MathNode):
    _CREATE_STR = 'condition'
    ALIAS = 'cdtn'

    def __init__(self, name):
        super().__init__(name)


class decomposeMatrix(MathNode):
    _CREATE_STR = 'decomposeMatrix'
    ALIAS = 'dcpm'

    def __init__(self, name):
        super().__init__(name)


class multMatrix(MathNode):
    _CREATE_STR = 'multMatrix'
    __slots__ = ['multMatrix', 'message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState',
                 'binMembership', 'matrixIn', 'matrixSum']
    ALIAS = 'mltmtx'

    def __init__(self, name):
        super().__init__(name)


class colorMath(MathNode):
    _CREATE_STR = 'colorMath'
    ALIAS = 'clrm'

    def __init__(self, name):
        super().__init__(name)


class blendColors(MathNode):
    _CREATE_STR = 'blendColors'
    ALIAS = 'bldclr'

    def __init__(self, name):
        super().__init__(name)

    def quick_connect(self, *args, **kwargs):
        input1 = args[0]
        input2 = args[1]
        self.color1.mount(input1)
        self.color2.mount(input2)


class dotProduct(MathNode):
    _CREATE_STR = 'dotProduct'
    ALIAS = 'dot'

    def __init__(self, name):
        super().__init__(name)


class vectorProduct(MathNode):
    _CREATE_STR = 'vectorProduct'
    ALIAS = 'vecprd'

    def __init__(self, name):
        super().__init__(name)

    def dot(self, other1, other2):
        self.operation.set(1)
        normal_node1 = normalize.create(f'{other1.name}_normalize')
        normal_node2 = normalize.create(f'{other2.name}_normalize')
        other1.outColor.connect(normal_node1.input)
        other2.outColor.connect(normal_node2.input)
        normal_node1.output.mount(self.input1)
        normal_node2.output.mount(self.input2)


class setRange(MathNode):
    _CREATE_STR = 'setRange'
    ALIAS = 'sr'

    def __init__(self, name):
        super().__init__(name)


class remapValue(MathNode):
    _CREATE_STR = 'remapValue'
    ALIAS = 'rmv'

    def __init__(self, name):
        super().__init__(name)


class normalize(MathNode):
    _CREATE_STR = 'normalize'
    ALIAS = 'normalize'

    def __init__(self, name):
        super().__init__(name)


class distanceBetween(MathNode):
    _CREATE_STR = 'distanceBetween'
    ALIAS = 'dist'

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
            target_attr.mount(point)
        if isinstance(point, str):
            point = MAttribute.create_by_name(point)
        point.mount(target_attr)


class MMultiply(object):
    # todo 1：自动适应maya版本，选择不同的节点（适应版本的工作交到具体的节点类，此处只做调用）
    # todo 2：自动根据数值，挑选合适的节点类型进行创建
    # todo 3: 自动连接属性

    # attribute types:constant,scalar,vector,matrix

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

    def __init__(self, alias, input1, input2):
        self.alias = alias
        self.input_attr_types = ''
        self.input1 = input1
        self.input2 = input2
        self.parse_input()
        self.build()

    def parse_input(self):
        attr_type = []
        for i in [self.input1, self.input2]:
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
        self.input_attr_types = '*'.join(attr_type)

    def build(self):
        try:
            cls_name = self.SUPPORTED_DICT[self.input_attr_types]
            cls = globals()[cls_name]
            name = f'{self.alias}_{cls.ALIAS}'
            mult_node: MathNode = cls.create(name)
            mult_node.quick_connect(self.input1, self.input2)

        except Exception as e:
            logging.error(f'Failed to initialize multiply node due to:{e}')
