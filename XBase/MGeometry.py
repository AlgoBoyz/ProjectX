import logging
import os
from typing import Union

import maya.cmds as mc
import maya.api.OpenMaya as om

from XBase.MNodes import MNode
from XBase.MTransform import MTransform
from XBase.MShape import MNurbsCurveShape, MNurbsSurfaceShape, MMeshShape
from XBase.MData import MCurveData, MWeightData
from XData.MNurbsCurveData import CurveDataCollection
from XTools.XFileTool import JsonFile
from XBase.MBaseFunctions import get_child


class MMesh(object):
    _CREATE_STR = 'polyPlane'

    def __init__(self, transform, shape):
        self.transform = MTransform(transform)
        if 'Shape' not in shape:
            raise RuntimeError(f'Failed to initiate MMesh({transform, shape})\n'
                               f'Something may go wrong with shape name:{shape}')
        self.shape = MMeshShape(shape)

    @classmethod
    def create(cls, name=None, **kwargs):
        if not name:
            name = cls._CREATE_STR
        # 根据_CREATE_STR检索cmds库中的创建函数并运行
        target_func = getattr(mc, cls._CREATE_STR)

        node = target_func(name=name, **kwargs)[0]
        shape = get_child(node)
        return cls(node, shape)


class MNurbsCurve(object):

    def __init__(self, transform: MTransform, shape: Union[MNurbsCurveShape, list[MNurbsCurveShape], None]):
        self.transform = transform
        self.shape = shape

    @classmethod
    def init_from_transform(cls, transform: Union[MTransform, str]):
        if isinstance(transform, MTransform):
            transform = transform.name
        shape = mc.listRelatives(transform, children=True, allDescendents=True) or None
        if shape is None:
            raise RuntimeError(f'Failed to initialize MNurbsCurve: {transform}')
        if len(shape) == 1:
            shape = MNurbsCurveShape(shape[0])
        else:
            shape = [MNurbsCurveShape(i) for i in shape]
        return cls(transform, shape)

    # @classmethod
    # def create_by_prototype(cls, name, prototype):
    #     if prototype == '':
    #         return cls(MTransform.create(name), None)
    #     file_path = os.path.join(MCurveData.DATA_DIR, f'{prototype}.json')
    #     data_io = JsonFile(file_path)
    #     data = data_io.load()
    #
    #     pos_array = [i[:3] for i in data['pos_array']]
    #     knots = data['knots']
    #     degree = data['degree']
    #
    #     curve = mc.curve(name=name, p=pos_array, knot=knots, degree=degree)
    #     curve_mt = MTransform(curve)
    #     curve_shape = curve_mt.child
    #     m_curve_shape = MNurbsCurveShape(curve_shape.name)
    #     return cls(curve_mt, m_curve_shape)

    # @classmethod
    # def create_by_points(cls, name, points, degree=3):
    #     curve = mc.curve(name=name, p=points, degree=degree)
    #     mc.rename(mc.listRelatives(curve, children=True)[0], f'{name}Shape')
    #     curve_mt = MTransform(curve)
    #     curve_shape = curve_mt.child
    #     m_curve_shape = MNurbsCurveShape(curve_shape.name)
    #     return cls(curve_mt, m_curve_shape)

    # def replace_shape_by_prototype(self, prototype):
    #     mc.delete(self.shape.shape_name)
    #     new_curve = self.create_by_prototype(f'{self.transform.name}_tmp_curve', prototype)
    #     new_curve.transform.match(self.transform)
    #     mc.parent(new_curve.shape.shape_name, self.transform.name, shape=True, addObject=True)
    #     self.shape = new_curve.shape
    #     mc.rename(self.shape.shape_name, f'{self.transform.name}Shape')
    #     mc.delete(new_curve.transform.name)

    # @classmethod
    # def create_on(cls, other: MTransform, name='', prototype='', suffix=None):
    #     if not name:
    #         name = f'{other.name}_Ctrl'
    #     instance = cls.create_by_prototype(name, prototype)
    #     instance.transform.match(other)
    #     other.set_parent(instance.transform)
    #     if suffix:
    #         for i in suffix:
    #             grp_name = f'{name}_{i}'
    #             instance.transform.insert_parent(grp_name)
    #     return instance

    @classmethod
    def rebuild_from_data(cls, name, data_collection: CurveDataCollection):
        transform = MTransform.create(name)
        for data in data_collection:
            tmp_curve = mc.curve(p=data.pos_array,
                                 degree=data.degree,
                                 knot=data.knots,
                                 periodic=data.periodic)
            mc.parent(get_child(tmp_curve), transform.name, addObject=True, shape=True)
            mc.delete(tmp_curve)
        instance = cls.init_from_transform(transform)
        return instance

    @classmethod
    def rebuild_from_disk(cls, name, file_name, work_dir=''):
        data = CurveDataCollection.from_disk(file_name, work_dir)
        instance = cls.rebuild_from_data(name, data)
        return instance


class MNurbsSurface(object):

    def __init__(self, transform, shape):
        self.transform: MTransform = transform
        self.shape: MNurbsSurfaceShape = shape

    @classmethod
    def create(cls, name):
        pass

    def create_joint_on(self, joint_name, uv, aim_axis, up_axis):
        from XBase.MTransform import MJoint
        jnt = MJoint.create(joint_name)

        pos = self.shape.surface_fn.getPointAtParam(uv[0], uv[1], om.MSpace.kWorld)
        normal = self.shape.surface_fn.normal(uv[0], uv[1], om.MSpace.kWorld)
        tangent = self.shape.surface_fn.tangents(uv[0], uv[1], om.MSpace.kWorld)[0]

        jnt.match_pos([pos[0], pos[1], pos[2]])
        jnt.reorient(aim_axis=aim_axis, aim_vec=list(tangent),
                     up_axis=up_axis, up_vec=list(normal))
        return jnt

    def create_follicle_on(self, fol_name, uv):
        fol_shape = mc.createNode(f'follicle')
        fol_transform = mc.listRelatives(fol_shape, parent=True)[0]
        fol_transform = mc.rename(fol_transform, fol_name)
        fol_shape = f'{fol_transform}Shape'
        self.shape.local.mount(f'{fol_shape}.inputSurface')
        self.shape.worldMatrix.mount(f'{fol_shape}.inputWorldMatrix')

        mc.connectAttr(f'{fol_shape}.outTranslate', f'{fol_transform}.translate')
        mc.connectAttr(f'{fol_shape}.outRotate', f'{fol_transform}.rotate')

        mc.setAttr(f'{fol_shape}.parameterU', uv[0])
        mc.setAttr(f'{fol_shape}.parameterV', uv[1])
        return fol_transform
