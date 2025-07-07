from typing import Union, Optional

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
        pass


class IKComponent(MJointBaseComponent):

    def __init__(self, alias, joint_chain: Union['mt.MTripleJointChain', list[str]], config=IKComponentConfig()):
        super().__init__(alias, joint_chain, config)
        self.alias = alias
        if isinstance(joint_chain, mt.MTripleJointChain):
            self.joint_chain = joint_chain
        elif isinstance(joint_chain, list) and len(joint_chain) == 3:
            self.joint_chain = MTripleJointChain(joint_chain)
        self._to_clean = []
        self.clean()

    @classmethod
    def create(cls, template, config):
        return cls(template.joints, template.alias, config)

    def build(self):
        self._create_cache_grp()

    def _create_cache_grp(self):
        root_grp_name = f'{self.alias}_component_cache'
        self.build_root_grp = mt.MTransform.create(name=root_grp_name)
        # XSpace.set_global_root(root_grp_name)
        jnt = mt.MJoint.create('test')
        tr = mt.MTransform.create('test_t')

    def _create_ik(self):
        self.ik_handle, self.ik_effector = mc.ikHandle(startJoint=self.joint_chain[0].name,
                                                       endEffector=self.joint_chain[-1].name)


    def clean(self):
        print(self._to_clean)
        mt.MTransform.set_root_space('')

    def post_build(self, func):
        func()


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
