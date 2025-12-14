import maya.cmds as mc

import XBase.MTransform as mt
import XBase.MGeometry as mg

from XBase.MBaseFunctions import switch_space_root


class IndicatorPlane(object):
    BACK_GROUND_COLOR = [0.15, 0.6, 1]
    INDICATOR_COLOR = [1, 0, 0]

    def __init__(self, alias):
        self.alias = alias
        self.plane_name = f'{self.alias}_Indicator_Plane'

    def build(self):
        self.plane = mg.MMesh.create(self.plane_name, sx=1, sy=1)
        mc.select(f'{self.plane.shape}.e[3]')
        mc.polySubdivideEdge()
        mc.polyConnectComponents(f'{self.plane.shape}.vtx[0]', f'{self.plane.shape}.vtx[4]')
        mc.polyConnectComponents(f'{self.plane.shape}.vtx[1]', f'{self.plane.shape}.vtx[4]')
        self.create_shader()

    def create_shader(self):
        background_shader_name = 'SurfBG_Shader'
        indicator_shader_name = 'SurfID_Shader'

        if not mc.objExists(background_shader_name):
            background_shader = mc.shadingNode('surfaceShader',
                                               name=background_shader_name,
                                               asShader=True)
            mc.setAttr(f'{background_shader}.outColor', *self.BACK_GROUND_COLOR, type='double3')
            mc.setAttr(f'{background_shader}.outTransparency', 0.5, 0.5, 0.5, type='double3')
            bg_shader_grp = mc.sets(name='BackGroundSG',
                                    renderable=True,
                                    noSurfaceShader=True,
                                    empty=True,
                                    )
            mc.connectAttr(f'{background_shader}.outColor', f'{bg_shader_grp}.surfaceShader', force=True)
            mc.sets(['LF_Arm_01_Indicator_Plane.f[2]', 'LF_Arm_01_Indicator_Plane.f[0]'],
                    edit=True,
                    forceElement=bg_shader_grp)
        if not mc.objExists(indicator_shader_name):
            indicator_shader = mc.shadingNode('surfaceShader',
                                              name=background_shader_name,
                                              asShader=True)
            mc.setAttr(f'{indicator_shader}.outColor', *self.INDICATOR_COLOR, type='double3')
            mc.setAttr(f'{indicator_shader}.outTransparency', 0.5, 0.5, 0.5, type='double3')
            indicator_shader_grp = mc.sets(name='BackGroundSG',
                                           renderable=True,
                                           noSurfaceShader=True,
                                           empty=True,
                                           )
            mc.connectAttr(f'{indicator_shader}.outColor', f'{indicator_shader_grp}.surfaceShader', force=True)
            mc.sets(['LF_Arm_01_Indicator_Plane.f[1]'],
                    edit=True,
                    forceElement=indicator_shader_grp)


class MBlueprintArm(object):
    SPECULAR_JOINT_NAMES = ['Specular', 'SpecularTip']
    ARM_JOINT_NAMES = ['Shoulder', 'Elbow', 'Wrist']

    def __init__(self, alias):
        self.alias = alias
        self.joint_chains = []
        self.normal_plane = None

    def create_initial_skeleton(self):
        self.cache_grp = mt.MTransform.create(f'{self.alias}_cache_grp')
        with switch_space_root(self.cache_grp):
            specular_names = [f'{self.alias}_{i}_Jnt' for i in self.SPECULAR_JOINT_NAMES]
            self._specular_joint_chain = mt.MJointChain.create(specular_names)
            self.joint_chains.append(self._specular_joint_chain)
            arm_names = [f'{self.alias}_{i}_Jnt' for i in self.ARM_JOINT_NAMES]
            self._arm_joint_chain = mt.MTripleJointChain.create(arm_names)
            self.joint_chains.append(self._arm_joint_chain)

            self._arm_joint_chain[0].set_parent(self._specular_joint_chain[-1])

            # initialize position
            self._specular_joint_chain[1].tx.mount(2)
            self._arm_joint_chain[1].tx.mount(4)
            self._arm_joint_chain[2].tx.mount(4)

            # rearrange hierarchy
            self._specular_joint_chain[0].set_parent(self.cache_grp)

    def read_skeleton_from_scene(self):
        for chain in self.joint_chains:
            for jnt in chain:
                print(jnt.name)

    def mirror(self):
        pass
