import logging
from typing import Union

import maya.cmds as mc

from XBase import MTransform as mt
from XBase.MConstant import AttrType, GlobalConfig, ConditionOperation, ParentType


class Component(object):

    def __init__(self, *args, **kwargs):
        pass

    def build(self):
        pass


class IKComponentConfig(object):

    def __init__(self):
        self.solver = 'ikRPsolver'  # ikRPsolver,ikSCsolver,ikSplineSolver
        self.pv_multiplier = 2
        self.pre_build_func = None
        self.post_build_func = None
        self.enable_stretch = True
        self.enable_lock = True


class IKComponent(object):
    CHAINT_TYPE = mt.MTripleJointChain

    def __init__(self, alias, joint_chain: Union['mt.MTripleJointChain', list[str]], config=IKComponentConfig()):
        self.alias = alias
        self.config = config
        if isinstance(joint_chain, mt.MTripleJointChain):
            self.joint_chain = joint_chain
        elif isinstance(joint_chain, list) and len(joint_chain) == 3:
            self.joint_chain = mt.MTripleJointChain(joint_chain)
        else:
            raise RuntimeError(f'Failed to initialize IKComponent')

        self._to_clean = []
        self.ctrl_value_node = None
        self.ik_handle_loc = None
        self.fst_jnt_loc = None

    def pre_build(self):
        if self.config.pre_build_func:
            self.config.pre_build_func()
        self.cache_grp = mt.MTransform.create(f'{self.alias}_Cache_Grp')
        GlobalConfig.set_root(self.cache_grp.name)
        self.ctrl_value_node = mt.MTransform.create(f'{self.alias}_CtrlValue_Proxy_Grp')
        self.ctrl_value_node.lock_attrs('t', 'r', 's', hide=True)
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
        if self.config.enable_lock:
            self._create_ik_lock()
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
            mc.poleVectorConstraint(self.pole_vec_loc, self.ik_handle)

    def _create_pole_vector(self):
        self.pole_vec_loc = mt.MLocator.create(f'{self.alias}_PV_Loc')
        pv_pos = self.joint_chain.get_pole_vec_pos(self.config.pv_multiplier)
        self.pole_vec_loc.match_pos(pv_pos)

    def _create_ik_stretch(self):
        stretch_alias = f'{self.alias}_Stretch'

        if self.ik_handle_loc is None:
            self.ik_handle_loc = self.ik_handle.create_loc(parent_type=ParentType.point_constraint)
        if self.fst_jnt_loc is None:
            self.fst_jnt_loc = self.joint_chain[0].create_loc(parent_type=ParentType.point_constraint)

        # graph connections
        # todo:为了加快项目开发，临时使用手动创建节点的形式，等自动连接节点的项目完成后重构
        from XBase.MConstant import Sign
        from XBase.MMathNode import distanceBetween, multDoubleLinear, condition, blendColors
        mult_factor = 1 if self.joint_chain[1].translateX.value > 0 else -1
        logging.info(f'Multiply factor:{mult_factor};{self.joint_chain[1]}.tx = {self.joint_chain[1].translateX.value}')
        dist_node = distanceBetween.create(f'{stretch_alias}_{distanceBetween.ALIAS}')
        dist_node.quick_connect(self.ik_handle_loc.shape.worldPosition, self.fst_jnt_loc.shape.worldPosition)

        mult_node = multDoubleLinear.create(f'{stretch_alias}_{multDoubleLinear.ALIAS}')
        dist_node.distance.mount(mult_node.input1)
        mult_node.input2.mount(mult_factor * 0.5)
        self.stretch_cond_node = condition.create(f'{stretch_alias}_{condition.ALIAS}')

        self.stretch_cond_node.firstTerm.mount(dist_node.distance, inverse=True)
        self.stretch_cond_node.operation.mount(ConditionOperation.GreaterThan)
        self.stretch_cond_node.secondTerm.mount(self.joint_chain[1].tx.value + self.joint_chain[2].tx.value)
        self.stretch_cond_node.colorIfTrueR.mount(mult_node.output, inverse=True)
        self.stretch_cond_node.colorIfTrueG.mount(mult_node.output, inverse=True)
        self.stretch_cond_node.colorIfFalseR.mount(self.joint_chain[1].tx.value)
        self.stretch_cond_node.colorIfFalseG.mount(self.joint_chain[2].tx.value)

        self.stretch_bldclr_node = blendColors.create(f'{stretch_alias}_{blendColors.ALIAS}')
        self.ctrl_value_node.stretch.mount(self.stretch_bldclr_node.blender)

        self.stretch_cond_node.outColorR.mount(self.stretch_bldclr_node.color1R)
        self.stretch_cond_node.outColorG.mount(self.stretch_bldclr_node.color1G)

        self.stretch_bldclr_node.color2R.mount(self.joint_chain[1].tx.value)
        self.stretch_bldclr_node.color2G.mount(self.joint_chain[2].tx.value)

        self.stretch_bldclr_node.outputR.mount(self.joint_chain[1].translateX)
        self.stretch_bldclr_node.outputG.mount(self.joint_chain[2].translateX)

    def _create_ik_lock(self):
        ik_lock_alias = f'{self.alias}_IkLock'

        if self.ik_handle_loc is None:
            self.ik_handle_loc = self.ik_handle.create_loc(parent_type=ParentType.point_constraint)

        if self.fst_jnt_loc is None:
            self.fst_jnt_loc = self.joint_chain[0].create_loc(parent_type=ParentType.point_constraint)
        # graph connections
        # todo:为了加快项目开发，临时使用手动创建节点的形式，等自动连接节点的项目完成后重构
        from XBase.MConstant import Sign
        from XBase.MMathNode import distanceBetween, blendColors
        distance_ap_node = distanceBetween.create(f'{ik_lock_alias}_{distanceBetween.ALIAS}')
        distance_pc_node = distanceBetween.create(f'{ik_lock_alias}_{distanceBetween.ALIAS}')

        distance_ap_node.quick_connect(self.fst_jnt_loc.shape.worldPosition, self.pole_vec_loc.shape.worldPosition)
        distance_pc_node.quick_connect(self.pole_vec_loc.shape.worldPosition, self.ik_handle_loc.shape.worldPosition)

        self.ik_lock_bldclr_node = blendColors.create(f'{ik_lock_alias}_{blendColors.ALIAS}')
        self.ik_lock_bldclr_node.blender.mount(self.ctrl_value_node.lock, inverse=True)
        self.ik_lock_bldclr_node.color1R.mount(distance_ap_node.distance, inverse=True)
        self.ik_lock_bldclr_node.color1G.mount(distance_pc_node.distance, inverse=True)
        color2R = self.joint_chain[1].translateX.value
        color2G = self.joint_chain[2].translateX.value
        if self.config.enable_stretch:
            color2R = self.stretch_bldclr_node.outputR
            color2G = self.stretch_bldclr_node.outputG

        self.ik_lock_bldclr_node.color2R.mount(color2R, inverse=True)
        self.ik_lock_bldclr_node.color2G.mount(color2G, inverse=True)

        self.ik_lock_bldclr_node.outputR.mount(self.joint_chain[1].translateX)
        self.ik_lock_bldclr_node.outputG.mount(self.joint_chain[2].translateX)

    def clean(self):
        for element in self._to_clean:
            pass

    def post_build(self):
        GlobalConfig.reset_root()
        if self.config.post_build_func:
            self.config.post_build_func()


class FKComponentConfig(object):
    def __init__(self):
        self.pre_build_func = None
        self.post_build_func = None
        self.enable_last = True
        self.parent_type = ParentType.parent_constraint
        self.ctrl_parent_suffix = ['Grp', 'Offset']


class FKComponent(object):
    CHAINT_TYPE = mt.MJointChain

    def __init__(self, alias, joint_chain, config=FKComponentConfig()):
        self.alias = alias
        self.joint_chain = joint_chain
        self.config = config
        self.fk_ctrls = []

    def build(self):
        self.pre_build()
        self._create_fk_ctrls()
        self._create_parent()
        self.post_build()

    def pre_build(self):
        if self.config.pre_build_func:
            self.config.pre_build_func()
        self.cache_grp = mt.MTransform.create(f'{self.alias}_Cache_Grp')
        GlobalConfig.set_root(self.cache_grp.name)
        self.ctrl_value_node = mt.MTransform.create(f'{self.alias}_CtrlValue_Proxy_Grp')
        self.ctrl_value_node.lock_attrs('t', 'r', 's', hide=True)

    def _create_fk_ctrls(self):
        for i, jnt in enumerate(self.joint_chain.nodes):
            ctrl_name = f'{jnt.name}_Ctrl'
            print(ctrl_name)
            ctrl = self.create_fk_ctrl(ctrl_name)
            ctrl_mt = mt.MTransform(ctrl)
            ctrl_mt.match(jnt)
            self.fk_ctrls.append(ctrl_mt)
            if i > 0:
                ctrl_mt.set_parent(self.fk_ctrls[i - 1])
            if self.config.ctrl_parent_suffix:
                for suffix in self.config.ctrl_parent_suffix:
                    ctrl_mt.insert_parent(f'{ctrl_mt.name}_{suffix}')

    def _create_parent(self):
        for i, ctrl_mt in enumerate(self.fk_ctrls):
            if self.config.parent_type == ParentType.hierarchy:
                self.joint_chain[i].set_parent(ctrl_mt)
            elif self.config.parent_type == ParentType.parent_constraint:
                mc.parentConstraint(ctrl_mt.name, self.joint_chain[i].name)

    def post_build(self):
        if self.config.post_build_func:
            self.config.post_build_func()

    @staticmethod
    def create_fk_ctrl(name):
        ctrl = mc.circle(name=name)[0]
        return ctrl


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


class BlendComponent(object):

    def __init__(self, alias, joint_chain):
        super().__init__()


class SplineIKComponent(Component):
    pass


class IKFKComponent(Component):
    pass
