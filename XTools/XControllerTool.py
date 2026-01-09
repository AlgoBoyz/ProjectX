from typing import Union, TypedDict

import maya.cmds as mc

from XBase.MTransform import MTransform
from XBase.MGeometry import MNurbsCurve
from XBase.MShape import MNurbsCurveShape
from XBase.MData import NurbsCurveDataDepot
from XBase.MBaseFunctions import get_child

class ControllerShapeData(TypedDict):
    is_compound: bool
    shape_data:dict

class MNurbsCurveController(object):
    class Prototype(object):
        Cube = 'cube'
        Circle = 'Circle'
        RootCircle = 'root_circle'
        SpineCircle = 'spine_circle'
        Cross = 'cross'
        Narrow = 'narrow'

    def __init__(self, transform: MTransform, shape: Union[MNurbsCurveShape, list[MNurbsCurveShape]]):
        self.transform = transform
        self.shape = shape

    @classmethod
    def create(cls, name, prototype_name):
        data = NurbsCurveDataDepot().get_geo_data_from_disk(prototype_name)
        pos_array = [i[:3] for i in data['pos_array']]
        knots = data['knots']
        degree = data['degree']

        curve = mc.curve(name=name, p=pos_array, knot=knots, degree=degree)
        instance = cls(MTransform(curve), MNurbsCurveShape(get_child(curve)))
        return instance
