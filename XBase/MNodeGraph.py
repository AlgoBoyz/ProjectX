from typing import Iterator, Optional

import maya.cmds as mc
from XBase.MNodes import MNode
from XBase.MAttribute import MAttribute
from XBase.MConstant import AttrType


class AttributeOperation(object):

    def __init__(self):
        pass

    @staticmethod
    def _parse_attr_type(*args):
        attr_type = []
        for i in args:
            if isinstance(i, float) or isinstance(i, int):
                attr_type.append('raw_scalar')
                continue
            elif isinstance(i, list) or isinstance(i, tuple):
                attr_type.append('raw_vector')
                continue

            mattr = None
            if isinstance(i, str):
                mattr = MAttribute.create_from_attr_name(i)
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
        return attr_type

    def multiply(self, attr1, attr2):
        pass

    def subtract(self, attr1, attr2):
        pass

    def divide(self, attr1, att2):
        pass

    def add(self, attr1, attr2):
        pass

    def distance_to(self):
        pass

    def as_condition(self):
        pass


class MNodeGraph(object):
    pass


class MFormula(object):
    """
    x.rx+y.rz+z.tx
    x.ty
    """

    def __init__(self):
        self.nodes = []

    def __getitem__(self, idx) -> 'MNode':
        return self.nodes[idx]

    def __iter__(self) -> Iterator['MNode']:
        return iter(self.nodes)

    def register(self):
        pass

    def execute(self):
        pass

    def get_node_from_type(self):
        pass

    def get_node_from_name(self):
        pass

    def insert(self, idx, in_attr, out_attr):
        pass


class MGraphCommand(object):

    def __init__(self):
        pass


class TokenType(object):
    Float = 'Float'
    Integer = 'Integer'
    Attribute = 'Attribute'

    Plus = 'Plus'
    Minus = 'Minus'
    Multiply = 'Multiply'
    Divide = 'Divide'

    LParent = 'LParent'
    RParent = 'RParent'

    Connect = 'Connect'

    IfElse = 'IfElse'

    Sine = 'Sine'
    Cosine = 'Cosine'


class Token(object):

    def __init__(self, token_type, token):
        if not token_type in TokenType.__dict__.keys():
            raise RuntimeError(f'Not supported token type:{token_type}')
        self.token_type = token_type
        self.token = token

    def __str__(self):
        return str(self.token)

    def __repr__(self):
        return f'Token(type:{self.token_type},value:{self.token})'


class Lexer(object):

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char: str = self.text[self.pos] if self.text else None

    def next(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def get_integer(self):
        integer_token = ''
        while self.current_char.isdigit():
            integer_token += self.current_char
            self.next()
        return integer_token

    def get_float(self):
        float_token = ''
        while self.current_char.isdigit() or self.current_char == '.':
            float_token += self.current_char
            self.next()
        return float_token

    def get_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.next()
                continue

            if self.current_char == '(':
                tokens.append(Token(TokenType.LParent, '('))
                self.next()
                continue
            elif self.current_char == ')':
                tokens.append(Token(TokenType.RParent, ')'))
                self.next()
                continue
            elif self.current_char == '+':
                tokens.append(Token(TokenType.Plus, '+'))
            elif self.current_char == '-':
                tokens.append(Token(TokenType.Minus, '-'))
            elif self.current_char == '*':
                tokens.append(Token(TokenType.Multiply, '*'))
            elif self.current_char == '/':
                tokens.append(Token(TokenType.Divide, '/'))

            elif self.current_char == '>>':
                tokens.append(Token(TokenType.Divide, '/'))

            else:
                pass


class NodeOutPorts(object):
    # todo:用于描述节点输出端多个或单个属性的类,将是每个MNode的基础属性，支持getitem操作
    pass


class NodeInPorts(object):
    # todo:用于描述节点输入端多个或单个属性的类,将是每个MNode的基础属性，支持getitem操作
    pass


from XBase.MMathNode import addDoubleLinear


class Operator(object):

    def __init__(self):
        self.current_node = None
        self.branch = []

    def point_to(self, other):
        return self

    def add(self, alias, in1, in2):
        add_node = addDoubleLinear.create(f'{alias}_{addDoubleLinear.ALIAS}')
        add_node.quick_connect(in1, in2)
        self.current_node = add_node
        self.branch.append([in1, in2, add_node])
        return self

    def forward(self, other):
        pass

    def backward(self, step: int):
        raise self

    def select_port(self, attr_name):
        return self


op = Operator()
op.add('LF_Arm_01', 'a.tx', 'b.ty').select_port('a.tx')
