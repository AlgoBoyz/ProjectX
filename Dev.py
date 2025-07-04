from importlib import reload
import os.path
import sys

from maya.cmds import polyPlane

import maya.cmds as mc
import maya.api.OpenMaya as om

from XBase.MTransform import MJointChain
from XBase.MTransform import MJoint

path = os.path.dirname(__file__)
if not path in sys.path:
    sys.path.append(path)
import XBase.MTransform as mt
import XBase.MMathNode as mm
import XBase.MConstant as mco

import XUI.XMainWindow

import datetime

print(datetime.datetime.today())


def standlone():
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
    joint_chain = mt.MJointChain.create([f'joint_{i}' for i in range(10)])
    for jnt in joint_chain:
        print(jnt.dp_node)
        print(jnt.dag_path.fullPathName())


def dev_attribute():
    node = mt.MJoint.create('joint')
    node.tx.connect(['joint.ty', 'joint.tz'])


def dev_print():
    data = {'name': {
        'pos_array': [1, 2, 3, 4]
    }}
    print(list(data.keys())[0])


def dev_mt():
    # mt_node = mt.MTransform.create('test', with_offset=True)
    mt2 = mt.MTransform.create('test2')
    mt2.insert_parent('offset')
    # mt2.set_parent(mt_node)


def dev_ui():
    from PySide6 import QtWidgets
    for widget in QtWidgets.QApplication.topLevelWidgets():
        if widget.windowTitle() == 'XRig':
            widget.deleteLater()
    main_ui = XUI.XMainWindow.XRigMainWindow()
    main_ui.show()


def dev_component():
    from XModules import MComponent
    jc = MJointChain.create(['jnt1', 'jnt2', 'jnt3'])
    cp = MComponent.IKComponent('LF_Arm_01', jc)
    cp.build()


def dev_create_skined_mesh():
    plane = mc.polyPlane(subdivisionsX=5, subdivisionsY=5)[0]
    jnts = [mt.MJoint.create(f'test_jnt_{i}').name for i in range(10)]

    mc.skinCluster(*jnts, plane, dropoffRate=4.5)
    return plane, jnts


def dev_save_data():
    standlone()
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
    standlone()
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
    from XBase.MTransform import MJointChain
    sel = mc.ls(selection=True)
    jc = MJointChain(sel)
    # standlone()
    # jc = MJointChain.create(['test1', 'test2'])
    # up_obj = mt.MTransform.create('test_transform').name
    from XBase.MConstant import WorldUpType, Axis
    jc.reorient(Axis.X.value, Axis.Y.value, up_obj='LF_Arm_01_PoleVec_loc')


def dev_template():
    # dev_reset_scene()
    # standlone()
    names = ['Shoulder', 'Elbow', 'Wrist']
    # jnts = dev_create_joints(num=3, alias='Test', offset=10, parent=True, attr='tx')
    # for i, jnt in enumerate(jnts):
    #     mc.rename(jnt, names[i])
    from XModules.MComponentTemplate import IKComponentData
    data = IKComponentData.load_from_scene()
    data.save_data('test_joints')


def dev_build_node_slot():
    standlone()
    from XBase import BuildNodeCache
    attrs: list[str] = BuildNodeCache.dev()
    for at in attrs:
        print(f"{at.capitalize()} = '{at}'")


if __name__ == '__main__':
    import maya.api.OpenMayaAnim as oman

    # help(oman)
    dev_template()
