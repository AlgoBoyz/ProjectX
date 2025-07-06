from importlib import reload
import os.path
import sys

from maya.OpenMaya import MVector
from mypyc.primitives.misc_ops import type_op

from maya.cmds import polyPlane

import maya.cmds as mc
import maya.api.OpenMaya as om

import XUI.XMainWindow

import datetime

print(datetime.datetime.today())


def standalone():
    import maya.standalone
    maya.standalone.initialize()


def dev_reset_scene():
    mc.file(newFile=True, force=True)
    # mc.viewSet(front=True)


def dev_reload():
    to_reload = []
    for key, value in sys.modules.items():
        if 'ProjectX' in str(value):
            to_reload.append(value)

    for m in to_reload:
        try:
            reload(m)
            print(f'{m} reloaded!')
        except ModuleNotFoundError:
            print(f'Failed to reload module:{m},module not found')


def reload_stdout():
    import sys
    import maya.app.startup.basic

    # Run the user's userSetup.py if it exists
    maya.app.startup.basic.executeUserSetup()

    import maya.app.baseUI
    import maya.utils

    # Replace sys.stdin with a GUI version that will request input from the user
    sys.stdin = maya.app.baseUI.StandardInput()

    # Replace sys.stdout and sys.stderr with versions that can output to Maya's
    # GUI
    sys.stdout = maya.utils.Output()
    sys.stderr = maya.utils.Output(error=1)


def dev():
    from XBase import MTransform as mt
    joint_chain = mt.MJointChain.create([f'joint_{i}' for i in range(10)])
    for jnt in joint_chain:
        print(jnt.dp_node)
        print(jnt.dag_path.fullPathName())


def dev_attribute():
    from XBase import MTransform as mt
    jc = mt.MJointChain.create(['jnt1', 'jnt2'])
    jc[0].t.add(jc[1].t, 'test')


def dev_print():
    data = {'name': {
        'pos_array': [1, 2, 3, 4]
    }}
    print(list(data.keys())[0])


def dev_mt():
    from XBase import MTransform as mt
    # mt_node = mt.MTransform.create('test', with_offset=True)
    mt2 = mt.MTransform.create('test2')
    mt2.insert_parent('offset')
    # mt2.set_parent(mt_node)


def dev_math():
    from XBase import MMathNode
    add = MMathNode.addDoubleLinear.create()


def dev_ui():
    from PySide6 import QtWidgets
    for widget in QtWidgets.QApplication.topLevelWidgets():
        if widget.windowTitle() == 'XRig':
            widget.deleteLater()
    main_ui = XUI.XMainWindow.XRigMainWindow()
    main_ui.show()


def dev_component():
    from XModules import MComponent
    from XBase import MTransform as mt
    jc = mt.MJointChain.create(['jnt1', 'jnt2', 'jnt3'])
    cp = MComponent.IKComponent('LF_Arm_01', jc)
    cp.build()


def dev_create_skined_mesh():
    from XBase import MTransform as mt
    plane = mc.polyPlane(subdivisionsX=5, subdivisionsY=5)[0]
    jnts = [mt.MJoint.create(f'test_jnt_{i}').name for i in range(10)]

    mc.skinCluster(*jnts, plane, dropoffRate=4.5)
    return plane, jnts


def dev_save_data():
    standalone()
    mesh, jnts = dev_create_skined_mesh()
    from XBase import MGeometry
    from XBase.MData import MCurveData, MWeightData, MSkinCluster
    weight = MSkinCluster.get_skin_cluster_from_node(mesh).collect_weight_data()
    # file_path = os.path.join(MCurveData.DATA_DIR,'nurbsCircleShape1.json')
    # data = MCurveData.load_from_file(file_path)
    # print(data)


def dev_geo():
    from XBase.MData import MCurveData
    from XBase import MGeometry
    data = MCurveData.load_from_file(r'F:\Code\Python\ProjectX\res\GeoData\NurbsCurve\nurbsCircleShape1.json')
    curve = MGeometry.MCurve.create(name='test', curve_data=data)
    curve.curve_data.calculate_up_axis()


def dev_generate_node_slot():
    from XBase import BuildNodeCache
    BuildNodeCache.dev()


def dev_matrix():
    standalone()
    # dev_reset_scene()
    from XBase.MGeometry import MMesh
    from XBase.MTransform import MLocator
    import XBase.MMathNode as mn
    plane = MMesh.create('test_plane')

    loc1 = MLocator.create('loc1')
    loc2 = MLocator.create('loc2')

    mulMat1 = mn.multMatrix.create('mul1')
    mulMat2 = mn.multMatrix.create('mul2')

    dMat1 = mn.decomposeMatrix.create('dMat1')
    dMat2 = mn.decomposeMatrix.create('dMat2')

    mdl1 = mn.multDoubleLinear.create('mdl1')
    mdl2 = mn.multDoubleLinear.create('mdl2')

    loc1.worldPosition.connect(mulMat1.matrixIn)
    mulMat1.matrixSum.connect(dMat1.inputMatrix)
    dMat1.outputTranslateZ.connect(mdl1.input1)


def dev_create_joints(num, alias='', offset=1, parent=True, attr='tx'):
    jnts = []
    for i in range(num):
        jnt_name = f'{alias}_{i + 1:02d}_Jnt'
        jnt = mc.createNode('joint', name=f'{alias}_{i + 1:02d}_Jnt')
        jnts.append(jnt)
        if parent:
            if i > 0:
                print(jnt, jnts[i - 1])
                mc.parent(jnt, jnts[i - 1])
        if offset and i > 0:
            mc.setAttr(f'{jnt}.{attr}', offset)

    return jnts


def dev_reoient():
    # dev_reset_scene()
    from XBase.MConstant import Axis
    from XBase.MTransform import MJointChain
    jnts = MJointChain(mc.ls(selection=True))
    jnts.reorient_to_plane_normal(Axis.Y.name, Axis.X.name)


def dev_template():
    # dev_reset_scene()
    standalone()
    names = ['Shoulder', 'Elbow', 'Wrist']
    # jnts = dev_create_joints(num=3, alias='Test', offset=10, parent=True, attr='tx')
    # for i, jnt in enumerate(jnts):
    #     mc.rename(jnt, names[i])
    from XModules.MComponentTemplate import IKComponentData
    data = IKComponentData.load_from_scene()
    data.save_data('test_joints')


def dev_build_node_slot():
    # standalone()
    from XBase import BuildNodeCache
    attrs = BuildNodeCache.build_math_node_cache()
    print(attrs)

def dev_skirt():
    from XBase import MTransform as mt
    from XBase.MMathNode import colorMath, dotProduct, setRange, remapValue
    from XBase.MConstant import Axis
    import math
    dev_reset_scene()

    test_scene_path = r'F:\作品集\Rig\Skirt\skirt_test_scene.mb'
    mc.file(test_scene_path, i=True)
    leg_jc = mt.MJointChain.create(['Leg_01_Jnt', 'Leg_02_Jnt'])
    leg_jc[1].ty.set(1.6)
    skirt_mesh = 'skirt_meshShape'
    origin_loc = mt.MTransform.create('origin_loc')
    origin_loc_tip = mt.MTransform.create('origin_loc_tip')
    mc.pointConstraint(leg_jc[1].name, origin_loc_tip.name)

    leg_vec_node = colorMath.create(name='leg_vec')
    leg_vec_node.operation.set(1)
    origin_loc_tip.translate.connect(leg_vec_node.colorB)
    origin_loc.translate.connect(leg_vec_node.colorA)

    raw_data_node = mt.MTransform.create('raw')
    remap_data_node = mt.MTransform.create('remap')
    leg_jc[0].add_attr(attr_name='param1', at='float', k=True)

    for idx in range(20):
        attr_name = f'Jnt_{idx}_dot'
        raw_data_node.add_attr(attr_name=attr_name, at='float', k=True)
        vtx = f'{skirt_mesh}.vtx[{idx}]'
        vtx_up = f'{skirt_mesh}.vtx[{idx + 20}]'

        jc = mt.MJointSet.create([f'Jnt_{vtx}', f'Jnt_{vtx_up}'])
        jc[0].translate.set(mc.xform(vtx, worldSpace=True, translation=True, q=True))
        jc[1].translate.set(mc.xform(vtx_up, worldSpace=True, translation=True, q=True))
        jc[1].set_parent(jc[0])

        # set orientation
        aim_vector = list((jc[0].world_pos - leg_jc[0].world_pos).normal())
        jc[0].reorient(aim_axis=Axis.X.name, aim_vec=aim_vector,
                       up_axis=Axis.Y.name, up_vec=[0.0, 1.0, 0.0])

        target_loc = mt.MTransform.create(f'target_loc_{vtx_up}')
        target_loc.translate.set(mc.xform(jc[1].name, worldSpace=True, translation=True, q=True))
        target_vec = colorMath.create(name=f'{target_loc.name}_vec')
        target_vec.operation.set(1)

        origin_loc.translate.connect(target_vec.colorB)
        target_loc.translate.connect(target_vec.colorA)

        dot = dotProduct.create(f'dot_{vtx_up}')

        leg_vec_node.outColor.connect(dot.input2)
        target_vec.outColor.connect(dot.input1)

        dot.output.connect(raw_data_node.attr(attr_name))

        remap = remapValue.create(f'remap_{attr_name}')
        raw_data_node.attr(attr_name).connect(remap.inputValue)
        remap.inputMin.set(-3.052)
        remap.inputMax.set(-2.668)

        remap.outputMin.set(0)
        remap.outputMax.set(1)

        remap_attr_name = f'Jnt_{idx}_remap'
        remap_data_node.add_attr(attr_name=remap_attr_name, at='float', k=True)

        remap.outValue.connect(f'{remap_data_node}.{remap_attr_name}')

        # getattr(sRange, remap_attr_name).connect()
        jc[0].freeze()

        rot_remap = remapValue.create(f'Jnt_{idx}_rot_remap')
        remap_data_node.attr(remap_attr_name).connect(rot_remap.inputValue)
        rot_remap.inputMin.set(0)
        rot_remap.inputMax.set(1)

        rot_remap.outputMin.set(-40)
        rot_remap.outputMax.set(0)

        rot_remap.outValue.connect(jc[0].rz)

        # mc.connectAttr(f'{leg_jc[0].name}.param1', f'{rot_remap.name}.value[0].value_Position')
        leg_jc[0].attr('param1').connect(f'{rot_remap.name}.value[0].value_Position', compund=True)


if __name__ == '__main__':
    # help(om.MVector)
    standalone()
    # dev_reload()
    dev_build_node_slot()
    # dev_reload()
