from imp import reload

import sys

import maya.cmds as mc
from .MNodes import MNode


class addDoubleLinear(MNode):
    _CREATE_STR = 'addDoubleLinear'
    if sys.version_info.minor == 11:
        _CREATE_STR = 'addDL'

    def __init__(self, name):
        super().__init__(name)


class multDoubleLinear(MNode):
    _CREATE_STR = 'multDoubleLinear'
    if sys.version_info.minor == 11:
        _CREATE_STR = 'multDL'

    def __init__(self, name):
        super().__init__(name)
        self.sss = ''


class multiplyDivide(MNode):
    _CREATE_STR = 'multiplyDivide'

    def __init__(self, name):
        super().__init__(name)


class floatMath(MNode):
    _CREATE_STR = 'floatMath'

    def __init__(self, name):
        super().__init__(name)


class condition(MNode):
    _CREATE_STR = 'condition'

    def __init__(self, name):
        super().__init__(name)


class decomposeMatrix(MNode):
    _CREATE_STR = 'decomposeMatrix'

    def __init__(self, name):
        super().__init__(name)


class multMatrix(MNode):
    _CREATE_STR = 'multMatrix'

    def __init__(self, name):
        super().__init__(name)


class colorMath(MNode):
    _CREATE_STR = 'colorMath'

    def __init__(self, name):
        super().__init__(name)


class dotProduct(MNode):
    _CREATE_STR = 'dotProduct'

    def __init__(self, name):
        super().__init__(name)


class setRange(MNode):
    _CREATE_STR = 'setRange'

    def __init__(self, name):
        super().__init__(name)


class remapValue(MNode):
    _CREATE_STR = 'remapValue'

    def __init__(self, name):
        super().__init__(name)
