from importlib import reload
import os.path
import sys
import numpy as np
import maya.cmds as mc

path = os.path.dirname(__file__)
if not path in sys.path:
    sys.path.append(path)
import XBase.MTransform as mt
import XBase.MMathNode as mm
import XBase.MConstant as mco


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


def dev():
    joint_chain = mt.MJointChain.create([f'joint_{i}' for i in range(10)])


def dev_attribute():
    node = mt.MJoint.create('joint')
    node.tx.connect(['joint.ty', 'joint.tz'])


def dev_print():
    mt1 = mt.MTransform.create('test')
    mt2 = mt.MTransform(mt1)
    adl = mm.addDoubleLinear.create('adl')
    adl2 = mm.addDoubleLinear(adl)
    print(adl2)


def dev_Component():
    import XModules.MComponent


if __name__ == '__main__':
    dev_print()
