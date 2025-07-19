from typing import Union, Optional
from xml.etree.ElementTree import XMLParser

import maya.cmds as mc

from XBase import *
from XBase import MTransform as mt
from XBase.MConstant import AttrType, XSpace
from XBase.MTransform import MTripleJointChain


class Component(object):

    def __init__(self, *args, **kwargs):
        pass

    def build(self):
        pass


class MJointBaseComponent(object):
    CHAINT_TYPE = mt.MJointChain

    def __init__(self, alias, joint_chain, config):
        self.alias = alias
        self.joint_chain = self.CHAINT_TYPE(joint_chain)
        self.config = config

class IKComponentConfig(object):

    def __init__(self):
        self.solver = 'ikRPsolver' #ikRPsolver,ikSCsolver,ikSplineSolver
        self.pv_multiplier = 2
        self.pre_build_func = None
        self.post_build_func = None
        self.enable_stretch = True
        self.enable_lock = True
class IKComponent(MJointBaseComponent):

    def __init__(self, alias, joint_chain: Union['mt.MTripleJointChain', list[str]], config=IKComponentConfig()):
        super().__init__(alias, joint_chain, config)
        self.ctrl_value_node = None
        self.alias = alias
        if isinstance(joint_chain, mt.MTripleJointChain):
            self.joint_chain = joint_chain
        elif isinstance(joint_chain, list) and len(joint_chain) == 3:
            self.joint_chain = MTripleJointChain(joint_chain)
        else:
            raise RuntimeError(f'Failed to initialize IKComponent')
        self._to_clean = []
    def pre_build(self):
        if self.config.pre_build_func:
            self.config.pre_build_func()
        self.cache_grp = mt.MTransform.create(f'{self.alias}_Cache_Grp')
        XSpace.set_root(self.cache_grp.name)
        self.ctrl_value_node = mt.MTransform.create(f'{self.alias}_CtrlValue_Proxy_Grp')
        self.ctrl_value_node.lock_attrs('t','r','s',hide=True)
        if self.config.enable_stretch:
            self.ctrl_value_node.add_attr(attr_name='stretch',
                                          at='float',
                                          minValue=0,
                                          maxValue=1,
                                          keyable=True)
        if self.config.enable_lock:
            self.ctrl_value_node.add_attr(attr_name='lock',
                                          at='float',
                                          minValue=0,
                                          maxValue=1,
                                          keyable=True)

    def build(self):
        self.pre_build()
        self._create_pole_vector()
        self._create_ik()
        if self.config.enable_stretch:
            self._create_ik_stretch()
        self.post_build()
    def _create_ik(self):
        ik_handle, ik_effector = mc.ikHandle(startJoint=self.joint_chain[0].name,
                                                       endEffector=self.joint_chain[2].name,
                                                       solver=self.config.solver)
        self.ik_handle = mt.MTransform(ik_handle)
        self.ik_handle.rename(f'{self.alias}_IkHandle')
        self.ik_handle_grp = self.ik_handle.insert_parent(f'{self.ik_handle.name}_Grp')
        self.ik_handle_grp.match(self.joint_chain[2])
        self.ik_effector = mt.MTransform(ik_effector)
        if self.pole_vec_loc:
            mc.poleVectorConstraint(self.pole_vec_loc,self.ik_handle)

    def _create_pole_vector(self):
        self.pole_vec_loc = mt.MLocator.create(f'{self.alias}_PV_Loc')
        pv_pos = self.joint_chain.get_pole_vec_pos(self.config.pv_multiplier)
        self.pole_vec_loc.match_pos(pv_pos)

    def _create_ik_stretch(self):
        stretch_alias = f'{self.alias}_Stretch'
        self.ik_handle_loc = mt.MLocator.create(f'{self.alias}_IkHandle_Loc',
                                                match_parent=self.ik_handle)
        self.first_joint_loc = mt.MLocator.create(f'{self.joint_chain[0].name}_Loc',
                                                  match_parent = self.joint_chain[0])
        distance_node = self.ik_handle_loc.shape.worldPosition.distance_to(self.first_joint_loc.shape.worldPosition,
                                                                        alias=stretch_alias)
        mult_node=distance_node.distance.multiply(0.5,alias=stretch_alias)[0]

    def _create_ik_lock(self):
        pass
    def clean(self):
        for element in self._to_clean:
            pass
    def post_build(self):
        XSpace.reset_root()
        if self.config.post_build_func:
            self.config.post_build_func()


class FKComponent(MJointBaseComponent):

    def __init__(self, alias, joint_chain, config):
        super().__init__()
        self.alias = alias
        self.joint_chain = joint_chain
        self.config = config


class SplineIKComponentConfig(object):

    def __init__(self):
        self.controller_count = 5
        self.add_pose_morph_tag = True
        self.controller_parent_suffixes = ["Grp", "Driven"]
        self.spline_type = "Cubic"
        self.fit_mode = "Relevant"
        self.create_fk_controller = True
        self.controller_null_shape = None
        self.add_controller_properties = True
        self.create_hierarchy = True
        self.use_spline = ""
        self.attr_type = AttrType.Float3


class BlendComponent(MJointBaseComponent):

    def __init__(self, alias, joint_chain):
        super().__init__()


class SplineIKComponent(Component):
    pass


class IKFKComponent(Component):
    pass
