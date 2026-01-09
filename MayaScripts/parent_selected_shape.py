import maya.cmds as mc

selected = mc.ls(selection=True)

mc.parent(selected[0], selected[1], addObject=True, shape=True)
