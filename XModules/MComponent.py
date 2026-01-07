import logging
from random import uniform
from typing import Union, Optional

import maya.cmds as mc
import maya.api.OpenMayaAnim as oma
import maya.api.OpenMaya as om

from XBase import MTransform as mt
from XBase.MBaseFunctions import linear_space, switch_space_root, OMUtils
from XBase.MConstant import AttrType, GlobalConfig, ConditionOperation, ParentType, ControllerPrototype, Axis, \
    WorldUpType
from XBase.MGeometry import MNurbsCurve, MNurbsSurface
from XBase.MNodes import MNode
from XBase.MShape import MNurbsSurfaceShape


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

        self.ik_handle_ctrl_prototype = 'Cube'
        self.pole_vec_ctrl_prototype = 'Cube'


class IKComponent(object):
    CHAINT_TYPE = mt.MTripleJointChain

    def __init__(self, alias, joint_chain: Union['mt.MTripleJointChain', list[str]], config=IKComponentConfig()):
        self.alias = alias
        self.config = config
        if isinstance(joint_chain, mt.MTripleJointChain):
            self.joint_chain = joint_chain
        elif isinstance(joint_chain, list) and len(joint_chain) == 3:
            self.joint_chain = mt.MTripleJointChain(joint_chain)
        elif isinstance(joint_chain, mt.MJointChain) and joint_chain.len == 3:
            self.joint_chain = mt.MTripleJointChain(joint_chain.node_names)
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
        self._create_controller()
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
        self.ik_handle.match(self.joint_chain[-1])
        self.ik_handle_grp = self.ik_handle.insert_parent(f'{self.ik_handle.name}_Grp')
        self.ik_handle_grp.match(self.joint_chain[2])
        self.ik_handle.set_parent(self.ik_handle_grp)
        self.ik_effector = mt.MTransform(ik_effector)
        if self.pole_vec_loc:
            mc.poleVectorConstraint(self.pole_vec_loc, self.ik_handle)

    def _create_pole_vector(self):
        self.pole_vec_loc = mt.MLocator.create(f'{self.alias}_PV_Loc')
        pv_pos = self.joint_chain.get_pole_vec_pos(self.config.pv_multiplier)
        self.pole_vec_loc.match_pos(pv_pos)

    def _create_controller(self):
        self.ik_ctrl = MNurbsCurve.create_on(self.ik_handle.parent,
                                             name=f'{self.alias}_IkHandle_Ctrl',
                                             prototype=self.config.ik_handle_ctrl_prototype,
                                             suffix=['Grp', 'Offset'])
        # self.ik_ctrl.transform.add_attr(attr_name='stretch',
        #                                 proxy=f'{self.ctrl_value_node}.stretch')
        # self.ik_ctrl.transform.add_attr(attr_name='lock',
        #                                 proxy=f'{self.ctrl_value_node}.lock')
        self.pv_ctrl = MNurbsCurve.create_on(self.pole_vec_loc,
                                             name=f'{self.alias}_PV_Ctrl',
                                             prototype=self.config.ik_handle_ctrl_prototype,
                                             suffix=['Grp', 'Offset'])

    def _create_ik_stretch(self):
        stretch_alias = f'{self.alias}_Stretch'

        if self.ik_handle_loc is None:
            self.ik_handle_loc = self.ik_handle.create_loc(parent_type=ParentType.point_constraint)
        if self.fst_jnt_loc is None:
            self.fst_jnt_loc = self.joint_chain[0].create_loc(parent_type=ParentType.point_constraint)

        # graph connections
        # todo:为了加快项目开发，临时使用手动创建节点的形式，等自动连接节点的项目完成后重构
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
            ctrl = MNurbsCurve.create_by_prototype(ctrl_name, 'Circle')
            ctrl_mt = ctrl.transform
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


class IKFKComponentConfig(object):
    def __init__(self):
        self.pre_build_func = None
        self.post_build_func = None
        self.ik_config = IKComponentConfig()
        self.fk_config = FKComponentConfig()


class IKFKComponent(object):

    def __init__(self, alias, joint_chain: mt.MJointChain, config=IKFKComponentConfig()):
        self.alias = alias
        self.main_joint_chain = joint_chain
        self.config = config

    def build(self):
        self.pre_build()
        self._create_ik_fk_joints()
        self._create_blend()
        self._create_component()
        self._create_proxy_attr()

    def pre_build(self):
        if self.config.pre_build_func:
            self.config.pre_build_func()
        self.cache_grp = mt.MTransform.create(f'{self.alias}_Cache_Grp')
        GlobalConfig.set_root(self.cache_grp.name)
        self.ctrl_value_node = mt.MTransform.create(f'{self.alias}_CtrlValue_Proxy_Grp')
        self.ctrl_value_node.lock_attrs('t', 'r', 's', hide=True)
        self.ctrl_value_node.add_attr(attr_name='IKFKSwitch', at='float', minValue=0, maxValue=1, keyable=True)

    def _create_ik_fk_joints(self):
        chains = []
        for suffix in ['IK', 'FK']:
            new_chain = mt.MJointChain(mc.duplicate(self.main_joint_chain[0], renameChildren=True))
            chains.append(new_chain)
            new_names = []
            for i, jnt in enumerate(new_chain):
                new_name = f'{self.alias}_{suffix}_{i + 1:02d}_Jnt'
                jnt.rename(new_name, parent_instance=new_chain)
                new_names.append(new_name)
                jnt.match(self.main_joint_chain[i])
                if i == 0:
                    jnt.set_visibility(False)
                    jnt.insert_parent(f'{self.alias}_{suffix}_Jnts_Grp')
        self.ik_joint_chain = chains[0]
        self.fk_joint_chain = chains[1]

    def _create_blend(self):
        from XBase.MMathNode import blendColors
        for i, jnt in enumerate(self.main_joint_chain):
            for attr in ['t', 'r', 's']:
                blend_node = blendColors.create(f'{jnt.name}_{attr}_{blendColors.ALIAS}')
                self.fk_joint_chain[i].attr(f'{attr}').mount(blend_node.color1)
                self.ik_joint_chain[i].attr(f'{attr}').mount(blend_node.color2)
                blend_node.blender.mount(self.ctrl_value_node.IKFKSwitch, inverse=True)
                blend_node.output.mount(jnt.attr(attr))

    def _create_component(self):
        self.ik_component = IKComponent(f'{self.alias}_IK', self.ik_joint_chain.node_names, self.config.ik_config)
        self.ik_component.build()
        self.fk_component = FKComponent(f'{self.alias}_FK', self.fk_joint_chain, self.config.fk_config)
        self.fk_component.build()

    def _create_proxy_attr(self):
        self.ik_component.ik_ctrl.transform.add_attr(attr_name='IKFKSwitch',
                                                     keyable=True,
                                                     proxy=f'{self.ctrl_value_node.IKFKSwitch.full_name}')
        self.ik_component.ik_ctrl.transform.add_attr(attr_name='stretch',
                                                     keyable=True,
                                                     proxy=f'{self.ik_component.ctrl_value_node.stretch.full_name}')
        self.ik_component.ik_ctrl.transform.add_attr(attr_name='lock',
                                                     keyable=True,
                                                     proxy=f'{self.ik_component.ctrl_value_node.lock.full_name}')
        self.ik_component.ik_ctrl.transform.visibility.lock(hide=True)


class SplineIKComponentConfig(object):

    def __init__(self):
        self.pre_build_func = None
        self.create_curve = True


class SplineIKComponent(object):
    def __init__(self, alias, joint_chain: mt.MJointChain, config=SplineIKComponentConfig()):
        self.alias = alias
        self.joint_chain = joint_chain
        self.config = config

    def pre_build(self):
        if self.config.pre_build_func:
            self.config.pre_build_func()
        self.cache_grp = mt.MTransform.create(f'{self.alias}_Cache_Grp')
        GlobalConfig.set_root(self.cache_grp.name)
        self.ctrl_value_node = mt.MTransform.create(f'{self.alias}_CtrlValue_Proxy_Grp')
        self.ctrl_value_node.lock_attrs('t', 'r', 's', hide=True)

    def build(self):
        self.pre_build()
        self._create_spline_ik()

    def _create_spline_ik(self):

        if self.config.create_curve:
            ik_handle, ik_effector, ik_curve = mc.ikHandle(startJoint=self.joint_chain[0].name,
                                                           endEffector=self.joint_chain[-1].name,
                                                           solver='ikSplineSolver',
                                                           createCurve=self.config.create_curve)
            self.ik_curve = MNurbsCurve(mt.MTransform(ik_curve), mc.listRelatives(ik_curve, shapes=True)[0])
        else:
            ik_handle, ik_effector = mc.ikHandle(startJoint=self.joint_chain[0].name,
                                                 endEffector=self.joint_chain[-1].name,
                                                 solver='ikSplineSolver'
                                                 )
        self.ik_handle = mt.MTransform(ik_handle)
        self.ik_handle.insert_parent(f'{self.ik_handle.name}_Grp')

    def _create_fk_controllers(self):
        pass

    def _create_ik_controllers(self):
        pass


class CurveBaseTwistComponentConfig(object):

    def __init__(self):
        self.pre_build_func = None

        self.enable_stretch = True
        self.enable_squash = True


class CurveBaseTwistComponent(object):

    def __init__(self, alias: str, joint_chain, config=CurveBaseTwistComponentConfig()):
        self.alias = alias
        self.joint_chain = mt.MJointChain(joint_chain)
        self.spline: Optional[MNurbsCurve, None] = None
        self.config = config

    @classmethod
    def init_from_spline(cls, alias: str,
                         spline: str,
                         count: int,
                         uniformed: bool,
                         config=CurveBaseTwistComponentConfig()):
        jc = mt.MJointChain.create_from_spline(alias, spline, count, uniformed=uniformed)
        instance = cls(alias, jc, config)
        instance.spline = MNurbsCurve(mt.MTransform(spline), None)
        return instance

    def pre_build(self):
        if self.config.pre_build_func:
            self.config.pre_build_func()
        self.cache_grp = mt.MTransform.create(f'{self.alias}_Cache_Grp')
        self.ctrl_value_node = mt.MTransform.create(f'{self.alias}_CtrlValue_Proxy_Grp',
                                                    under=self.cache_grp.name,
                                                    match=self.joint_chain[0].name)
        self.ctrl_value_node.lock_attrs('t', 'r', 's', hide=True)

    def build(self):
        self.pre_build()
        with switch_space_root(self.cache_grp.name):
            if self.spline:
                self.ik_handle = mc.ikHandle(startJoint=self.joint_chain[0].name,
                                             endEffector=self.joint_chain[-1].name,
                                             solver='ikSplineSolver',
                                             createCurve=False,
                                             curve=self.spline.transform.name,
                                             name=f'{self.alias}_IKHandle'
                                             )[0]
            else:
                res = mc.ikHandle(startJoint=self.joint_chain[0].name,
                                  endEffector=self.joint_chain[-1].name,
                                  solver='ikSplineSolver',
                                  name=f'{self.alias}_IKHandle'
                                  )

                self.ik_handle = mt.MTransform(res[0])
                spline = mc.rename(res[-1], f'{self.alias}_Spline')
                self.spline = MNurbsCurve(mt.MTransform(spline), None)
            self._create_twist()
            if self.config.enable_stretch:
                self._create_stretch()
            if self.config.enable_squash:
                self._create_squash()
            self._setup_curve_weight()
            self._rearrange_hierarchy()

    def _create_twist(self):
        self.start_ctrl_jnt = mt.MJoint.create(name=f'{self.alias}_Start_Jnt',
                                               match=self.joint_chain[0])
        self.end_ctrl_jnt = mt.MJoint.create(name=f'{self.alias}_End_Jnt',
                                             match=self.joint_chain[-1])

        mc.skinCluster(self.spline.transform.name,
                       [self.end_ctrl_jnt,
                        self.start_ctrl_jnt],
                       toSelectedBones=True)
        mc.setAttr(f'{self.ik_handle}.dTwistControlEnable', True)
        mc.setAttr(f'{self.ik_handle}.dWorldUpType', 4)
        self.start_ctrl_jnt.worldMatrix.mount(f'{self.ik_handle}.dWorldUpMatrix')
        self.end_ctrl_jnt.worldMatrix.mount(f'{self.ik_handle}.dWorldUpMatrixEnd')

    def _create_stretch(self):
        from XBase.MMathNode import curveInfo, multiplyDivide
        stretch_alias = f'{self.alias}_Stretch'
        self.cvf_node = curveInfo.create(f'{stretch_alias}_{curveInfo.ALIAS}')
        self.cvf_node.set_curve(self.spline.shape.name)
        self.curve_stretch_rate_mldv_node = multiplyDivide.create(f'{stretch_alias}_{multiplyDivide.ALIAS}',
                                                                  operation=multiplyDivide.DIVIDE)
        self.curve_stretch_rate_mldv_node.input1X.mount(self.cvf_node.arcLength, inverse=True)
        self.curve_stretch_rate_mldv_node.input2X.mount(self.cvf_node.arcLength.value)

        for jnt in self.joint_chain:
            self.curve_stretch_rate_mldv_node.outputX.mount(jnt.translateX)

    def _create_squash(self):
        from XBase.MMathNode import curveInfo, multDoubleLinear, multiplyDivide, remapValue, addDoubleLinear
        squash_alias = f'{self.alias}_Squash'
        if not self.config.enable_stretch:
            self.cvf_node = curveInfo.create(f'{squash_alias}_{curveInfo.ALIAS}')
            self.squash_mldv_node = multiplyDivide.create(f'{squash_alias}_{multiplyDivide.ALIAS}',
                                                          operation=multiplyDivide.DIVIDE)
            self.curve_stretch_rate_mldv_node.input1X.mount(self.cvf_node.arcLength)
            self.curve_stretch_rate_mldv_node.input2X.mount(self.cvf_node.arcLength.value)

        squash_factor_mldv_node = multiplyDivide.create(f'{squash_alias}_{multiplyDivide.ALIAS}',
                                                        operation=multiplyDivide.DIVIDE)
        squash_factor_mldv_node.input1X.mount(1)
        squash_factor_mldv_node.input2X.mount(self.curve_stretch_rate_mldv_node.outputX, inverse=True)

        is_even = True if self.joint_chain.len % 2 == 0 else False
        factors = []
        mid = int(self.joint_chain.len / 2 if is_even else (self.joint_chain.len + 1) / 2)
        factors.extend(linear_space(0, 1, mid))
        factors.extend(linear_space(1, 0, mid))
        if not is_even:
            factors.pop(mid)

        self.cache_grp.add_attr(attr_name='scaleFactor',
                                at='float',
                                dv=1,
                                minValue=1
                                )

        for i, jnt in enumerate(self.joint_chain):
            factor_mdl = multDoubleLinear.create(f'{squash_alias}_{i + 1:02d}_{multDoubleLinear.ALIAS}')
            factor_mdl.input1.mount(factors[i])
            factor_mdl.input2.mount(squash_factor_mldv_node.outputX, inverse=True)

            factor_adl = addDoubleLinear.create(name=f'{squash_alias}_{i + 1:02d}_{addDoubleLinear.ALIAS}')
            factor_adl.input1.mount(factor_mdl.output, inverse=True)
            factor_adl.input2.mount(self.cache_grp.scaleFactor,inverse=True)

            factor_adl.output.mount(jnt.scaleY)
            factor_adl.output.mount(jnt.scaleZ)

    def _setup_curve_weight(self):
        curve_component = OMUtils.get_nurbsCurve_component(self.spline.shape.name)
        head_jnt_weight = linear_space(0, 1, OMUtils.get_nurbsCurve_fn_from(self.spline.shape.name).numCVs)
        weight_array = []
        for i in head_jnt_weight:
            weight_array.append(i)
            weight_array.append(1 - i)
        weight_array = om.MDoubleArray(weight_array)
        sc_fn = OMUtils.get_geo_sc_fn(self.spline.transform.name)
        sc_fn.setWeights(self.spline.shape.dag_path,
                         curve_component,
                         om.MIntArray([0, 1]),
                         weight_array)

    def _rearrange_hierarchy(self):
        if self.joint_chain[0].parent is None:
            self.joint_chain[0].set_parent(GlobalConfig.transform_root)
        if self.spline.transform.parent is None:
            self.spline.transform.set_parent(GlobalConfig.transform_root)
        mc.parent(self.ik_handle, GlobalConfig.transform_root)


class SurfaceBaseTwistComponentConfig(object):

    def __init__(self):
        self.pre_build_func = None

        self.enable_wave = True
        self.enable_fk = False
        self.ik_ctrl_count = 5

        self.is_upper = True


class SurfaceBaseTwistComponent(object):

    def __init__(self, alias, joint_chain, config=SurfaceBaseTwistComponentConfig()):
        self.alias = alias
        self.joint_chain = joint_chain
        self.config = config

    def pre_build(self):
        if self.config.pre_build_func:
            self.config.pre_build_func()
        self.cache_grp = mt.MTransform.create(f'{self.alias}_Cache_Grp')

    def build(self):
        self.pre_build()
        with switch_space_root(self.cache_grp.name):
            self.ctrl_value_node = mt.MTransform.create(f'{self.alias}_CtrlValue_Proxy_Grp')
            self.ctrl_value_node.lock_attrs('t', 'r', 's', hide=True)
            self._create_surface()
            self._create_twist_joints()
            self._create_control_joint()
            self._setup_surface_weight()
            self._rearrange_hierarchy()

    def _create_surface(self):
        surface_transform, make_surface = mc.nurbsPlane(name=f'{self.alias}_Surface', axis=(0, 1, 0))
        surface_shape = mc.listRelatives(surface_transform, shapes=True)[0]
        self.surface = MNurbsSurface(mt.MTransform(surface_transform), MNurbsSurfaceShape(surface_shape))
        self.surface.transform.match(self.joint_chain[0])
        self.surface_maker = MNode(make_surface)
        self.surface_maker.pivotX.set(0.5 * self.joint_chain[1].tx.value)
        self.surface_maker.width.set(self.joint_chain[1].tx)
        self.surface_maker.lengthRatio.set(0.1)

        # mc.delete(surface_shape,constructionHistory=True)

    def _create_twist_joints(self):
        u_array = linear_space(0, 1, self.config.ik_ctrl_count - 1)
        jnts = []
        self.follicles = []
        for i, u in enumerate(u_array):
            jnt = self.surface.create_joint_on(f'{self.alias}_{i + 1:02d}_Jnt',
                                               [u, 0.5],
                                               aim_axis=Axis.X.name,
                                               up_axis=Axis.Y.name)
            jnts.append(jnt)
            fol = self.surface.create_follicle_on(f'{self.alias}_{i + 1:02d}_Fol',
                                                  [u, 0.5])
            self.follicles.append(fol)
            jnt.insert_parent(f'{jnt.name}_Grp')
            jnt.parent.set_parent(fol)

        self.twist_joints = mt.MJointSet(jnts)

    def _create_control_joint(self):
        if self.config.is_upper:
            self.upper_ik_jc = mt.MJointChain.create([f'{self.alias}_IK_Jnt', f'{self.alias}_IKTip_Jnt', ])
            self.upper_ik_jc[0].match(self.joint_chain[0])
            self.upper_ik_jc[-1].match(self.joint_chain[-1])
            handle = mc.ikHandle(solver='ikSCsolver',
                                 startJoint=self.upper_ik_jc[0].name,
                                 endEffector=self.upper_ik_jc[1].name,
                                 name=f'{self.alias}_IkHandle')[0]
            self.upper_ik_Handle = mt.MTransform(handle)

            mc.pointConstraint(self.joint_chain[-1],
                               self.upper_ik_Handle.name)

        self.twist_tip_jnt = mt.MJoint.create(f'{self.alias}_TipTwist_Jnt',
                                              match=self.joint_chain[-1])

        mc.aimConstraint(self.joint_chain[0],
                         self.twist_tip_jnt.name,
                         aimVector=[-1, 0, 0],
                         upVector=[0, 1, 0],
                         worldUpType='objectrotation',
                         worldUpObject=self.joint_chain[-1],
                         worldUpVector=[0, 1, 0])

        mc.pointConstraint(self.joint_chain[-1],
                           self.twist_tip_jnt.name)
        if self.config.is_upper:
            mc.skinCluster(self.surface.transform.name,
                           [self.twist_tip_jnt.name, self.upper_ik_jc[0].name],
                           toSelectedBones=True)
        else:
            mc.skinCluster(self.surface.transform.name,
                           [self.twist_tip_jnt.name, self.joint_chain[0].name],
                           toSelectedBones=True)
        self._setup_surface_weight()

    def _setup_surface_weight(self):
        weight = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0,
                  0.333, 0.667, 0.333, 0.667, 0.333, 0.667, 0.333, 0.667,
                  0.667, 0.333, 0.667, 0.333, 0.667, 0.333, 0.667, 0.333,
                  1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0]
        cv = OMUtils.get_nurbsSurface_component(self.surface.shape.name)
        skin_fn = oma.MFnSkinCluster(OMUtils.get_dependency_node(self.surface.shape.skin_cluster))

        skin_fn.setWeights(self.surface.shape.dag_path,
                           cv,
                           om.MIntArray([0, 1]),
                           om.MDoubleArray(weight))

    def _rearrange_hierarchy(self):
        self.surface.transform.set_parent(self.cache_grp.name)
        for fol in self.follicles:
            mc.parent(fol, self.cache_grp.name)
        if self.config.is_upper:
            self.upper_ik_Handle.set_parent(self.cache_grp.name)
