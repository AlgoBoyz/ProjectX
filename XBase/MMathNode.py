from imp import reload

import sys

import maya.cmds as mc
from .MNodes import MNode


class addDoubleLinear(MNode):
    __slots__ = ['message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState', 'input1', 'input2', 'output',
                 'msg', 'cch', 'fzn', 'ihi', 'nds', 'i1', 'i2', 'o']
    _CREATE_STR = 'addDoubleLinear'
    if sys.version_info.minor == 11:
        _CREATE_STR = 'addDL'

    def __init__(self, name):
        super().__init__(name)


class multDoubleLinear(MNode):
    __slots__ = ['message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState', 'input1', 'input2', 'output',
                 'msg', 'cch', 'fzn', 'ihi', 'nds', 'i1', 'i2', 'o']
    _CREATE_STR = 'multDoubleLinear'
    if sys.version_info.minor == 11:
        _CREATE_STR = 'multDL'

    def __init__(self, name):
        super().__init__(name)
        self.sss = ''

class multiplyDivide(MNode):
    __slots__ = ['message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState', 'operation', 'input1',
                 'input1X', 'input1Y', 'input1Z', 'input2', 'input2X', 'input2Y', 'input2Z', 'output', 'outputX',
                 'outputY', 'outputZ', 'msg', 'cch', 'fzn', 'ihi', 'nds', 'op', 'i1', 'i1x', 'i1y', 'i1z', 'i2', 'i2x',
                 'i2y', 'i2z', 'o', 'ox', 'oy', 'oz']
    _CREATE_STR = 'multiplyDivide'

    def __init__(self, name):
        super().__init__(name)


class floatMath(MNode):
    __slots__ = ['message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState', 'floatA', 'floatB',
                 'outFloat', 'msg', 'cch', 'fzn', 'ihi', 'nds', '_fa', '_fb', 'of']
    _CREATE_STR = 'floatMath'

    def __init__(self, name):
        super().__init__(name)


class condition(MNode):
    __slots__ = ['message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState', 'operation', 'firstTerm',
                 'secondTerm', 'colorIfTrue', 'colorIfTrueR', 'colorIfTrueG', 'colorIfTrueB', 'colorIfFalse',
                 'colorIfFalseR', 'colorIfFalseG', 'colorIfFalseB', 'outColor', 'outColorR', 'outColorG', 'outColorB',
                 'msg', 'cch', 'fzn', 'ihi', 'nds', 'op', 'ft', 'st', 'ct', 'ctr', 'ctg', 'ctb', 'cf', 'cfr', 'cfg',
                 'cfb', 'oc', 'ocr', 'ocg', 'ocb']
    _CREATE_STR = 'condition'

    def __init__(self, name):
        super().__init__(name)
