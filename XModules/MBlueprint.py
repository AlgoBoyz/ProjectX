from ast import literal_eval

import maya.cmds as mc

import XBase.MTransform as mt
import XBase.MGeometry as mg

from XBase.MBaseFunctions import switch_space_root
from XBase.MNodes import MSurfaceShaderNode
from XBase.MBaseFunctions import undo_stack


class IndicatorPlane(mg.MMesh):
    BACK_GROUND_COLOR = [0.15, 0.6, 1]
    INDICATOR_COLOR = [1, 0, 0]

    def __init__(self, transform, shape):
        super().__init__(transform, shape)
        self.locators: list[mt.MLocator] = []
        self.bg_shader = None
        self.vec_shader = None

    @classmethod
    def create(cls, name=None, **kwargs):
        with undo_stack():
            plane = mg.MMesh.create(name, sx=1, sy=1)
            mc.select(f'{plane.shape}.e[3]')
            mc.polySubdivideEdge()
            mc.select(f'{plane.shape}.e[0]')
            mc.polySubdivideEdge()
            instance = cls(plane.transform.name, plane.shape.name)
            mc.polyConnectComponents(f'{instance.shape.name}.vtx[0]', f'{instance.shape.name}.vtx[4]')
            mc.polyConnectComponents(f'{instance.shape.name}.vtx[1]', f'{instance.shape.name}.vtx[4]')
            instance.create_shader()
            return instance

    def create_shader(self):
        self.bg_shader = MSurfaceShaderNode.create(name=f'{self.transform.name}_BGShader',
                                                   color=[0, 0, 1],
                                                   transparency=[0.8, 0.8, 0.8],
                                                   shading_grp=f'{self.transform.name}_ShadingGrp')
        self.bg_shader.apply_to([f'{self.shape.name}.f[{i}]' for i in [0, 2]])
        self.vec_shader = MSurfaceShaderNode.create(name=f'{self.transform.name}_VECShader',
                                                    color=[1, 0, 0],
                                                    transparency=[0.8, 0.8, 0.8],
                                                    shading_grp=f'{self.transform.name}_ShadingGrp')
        self.vec_shader.apply_to([f'{self.shape.name}.f[{i}]' for i in [1]])

    def match_joint_chain(self, joint_chain: mt.MJointChain):
        if len(joint_chain) == 2:
            self.transform.match(joint_chain[0])
        elif len(joint_chain) == 3:
            self.transform.match(joint_chain[1])
        else:
            pass


class MBlueprintArm(object):
    SPECULAR_JOINT_NAMES = ['Specular', 'SpecularTip']
    ARM_JOINT_NAMES = ['Shoulder', 'Elbow', 'Wrist']

    def __init__(self, alias):
        self.alias = alias
        self.joint_chains = []
        self.normal_plane = None

    def create_initial_skeleton(self):
        self.cache_grp = mt.MTransform.create(f'{self.alias}_cache_grp')
        meta_data = {}
        with switch_space_root(self.cache_grp):
            specular_names = [f'{self.alias}_{i}_Jnt' for i in self.SPECULAR_JOINT_NAMES]
            self.specular_joint_chain = mt.MJointChain.create(specular_names)
            self.joint_chains.append(self.specular_joint_chain)
            arm_names = [f'{self.alias}_{i}_Jnt' for i in self.ARM_JOINT_NAMES]
            self.arm_joint_chain = mt.MTripleJointChain.create(arm_names)
            self.joint_chains.append(self.arm_joint_chain)

            self.arm_joint_chain[0].set_parent(self.specular_joint_chain[-1])

            # initialize position
            self.specular_joint_chain[1].tx.mount(2)
            self.arm_joint_chain[1].tx.mount(4)
            self.arm_joint_chain[2].tx.mount(4)

            # rearrange hierarchy
            self.specular_joint_chain[0].set_parent(self.cache_grp)
            # collect meta data
            meta_data['specular_joints'] = specular_names
            meta_data['arm_joints'] = arm_names

        self.cache_grp.add_attr(attr_name='meta_data', dt='string')
        mc.setAttr(f'{self.cache_grp}.meta_data', str(meta_data), type='string')

    @classmethod
    def initial_from_scene(cls, alias):
        instance = cls(alias)
        instance.cache_grp = mt.MTransform(f'{alias}_cache_grp')
        meta_data = literal_eval(mc.getAttr(f'{alias}_cache_grp.meta_data'))
        instance.specular_joints = mt.MJointChain(meta_data['specular_joints'])
        instance.arm_joints = mt.MTripleJointChain(meta_data['arm_joints'])
        instance.joint_chains = [instance.specular_joints, instance.arm_joints]
        return instance

    def mirror(self):
        pass
