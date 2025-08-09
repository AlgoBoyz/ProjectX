import logging
import os
from typing import Union

import maya.cmds as mc
import maya.api.OpenMaya as om

from XBase.MTransform import MTransform
from XBase.MShape import MNurbsCurveShape, MNurbsSurfaceShape
from XBase.MData import MCurveData, MWeightData
from XTools.XFileTool import JsonFile


# from .MTransform import MTransform





class MMesh(object):
    _CREATE_STR = 'polyPlane'

    def __init__(self, shape_node):
        super().__init__(shape_node)

    @classmethod
    def create(cls, name=None, **kwargs):
        if not name:
            name = cls._CREATE_STR
        node = mc.polyPlane(name=name)[1]
        return cls(node)

    def export_weight(self):
        pass

    @property
    def vert_num(self):
        return om.MFnMesh(self.dp_node).numVertices

class MNurbsCurve(object):
    
    def __init__(self,transform:MTransform,shape:Union[MNurbsCurveShape,None]):
        self.transform = transform
        self.shape = shape
    
    @classmethod
    def create_by_prototype(cls,name,prototype):
        if prototype == '':
            return cls(MTransform.create(name),None)
        file_path = os.path.join(MCurveData.DATA_DIR,f'{prototype}.json')
        data_io = JsonFile(file_path)
        data = data_io.load()

        pos_array = [i[:3] for i in data['pos_array']]
        knots = data['knots']
        degree = data['degree']

        curve = mc.curve(name=name,p=pos_array,knot=knots,degree=degree)
        curve_mt = MTransform(curve)
        curve_shape = curve_mt.child
        m_curve_shape = MNurbsCurveShape(curve_shape.name)
        return cls(curve_mt,m_curve_shape)

    @classmethod
    def create_by_points(cls,name,points,degree = 3):
        curve = mc.curve(name=name,p=points,degree=degree)
        curve_mt = MTransform(curve)
        curve_shape = curve_mt.child
        m_curve_shape = MNurbsCurveShape(curve_shape.name)
        return cls(curve_mt,m_curve_shape)

    def replace_shape_by_prototype(self,prototype):
        pass

    @classmethod
    def create_on(cls,other:MTransform,name='',prototype='',suffix=None):
        if not name:
            name = f'{other.name}_Ctrl'
        instance = cls.create_by_prototype(name,prototype)
        instance.transform.match(other)
        other.set_parent(instance.transform)
        if suffix:
            for i in suffix:
                grp_name = f'{name}_{i}'
                instance.transform.insert_parent(grp_name)
        return instance

class MNurbsSurface(object):

    def __init__(self, transform,shape):
        self.transform:MTransform = transform
        self.shape:MNurbsSurfaceShape = shape

    @classmethod
    def create(cls,name):
        pass

    def create_joint_on(self,joint_name,uv,aim_axis,up_axis):
        from XBase.MTransform import MJoint
        jnt = MJoint.create(joint_name)

        pos = self.shape.surface_fn.getPointAtParam(uv[0],uv[1],om.MSpace.kWorld)
        normal = self.shape.surface_fn.normal(uv[0],uv[1],om.MSpace.kWorld)
        tangent = self.shape.surface_fn.tangents(uv[0],uv[1],om.MSpace.kWorld)[0]

        jnt.match_pos([pos[0],pos[1],pos[2]])
        jnt.reorient(aim_axis=aim_axis,aim_vec=list(tangent),
                     up_axis=up_axis,up_vec=list(normal))
        return jnt