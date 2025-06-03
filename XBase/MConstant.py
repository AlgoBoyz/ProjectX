import enum
from re import split


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
