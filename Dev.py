from importlib import reload
import os.path
import sys
import maya.cmds as mc
import maya.api.OpenMaya as om

from XBase.MTransform import MJointChain
from maya.app.renderSetup.model.typeIDs import override

path = os.path.dirname(__file__)
if not path in sys.path:
    sys.path.append(path)
import XBase.MTransform as mt
import XBase.MMathNode as mm
import XBase.MConstant as mco

import XUI.XMainWindow


def dev_reset_scene():
    mc.file(newFile=True, force=True)
    mc.viewSet(front=True)


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
    data = {'name':{
        'pos_array':[1,2,3,4]
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


def dev_save_data():
    from XBase import MGeometry
    # file_path = os.path.join(MGeometry.CurveData.DATA_DIR,'nurbsCircleShape1.json')
    # data = MGeometry.CurveData.load_from_file(file_path)
    # print(data)
    MGeometry.CurveData.save_node_data('nurbsCircleShape1',override=True)

def dev_geo():
    from XBase import MGeometry
    data = MGeometry.CurveData.load_from_file(r'F:\Code\Python\ProjectX\res\GeoData\NurbsCurve\nurbsCircleShape1.json')
    curve = MGeometry.MCurve.create(name='test', curve_data=data)
    curve.curve_data.calculate_up_axis()


if __name__ == '__main__':
    dev_print()
