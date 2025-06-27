from typing import Iterator, Union

import maya.api.OpenMaya as om
import maya.cmds as mc

from . import MBaseFunctions as mb
from . import MNodes
from .MConstant import XSpace

class MTransform(MNodes.MNode):
    __slots__ = ['message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState', 'hyperLayout', 'isCollapsed',
                 'blackBox', 'borderConnections', 'publishedNodeInfo', 'templateName', 'templatePath', 'viewName',
                 'iconName', 'viewMode', 'templateVersion', 'uiTreatment', 'customTreatment', 'creator', 'creationDate',
                 'containerType', 'boundingBox', 'boundingBoxMin', 'boundingBoxMinX', 'boundingBoxMinY',
                 'boundingBoxMinZ', 'boundingBoxMax', 'boundingBoxMaxX', 'boundingBoxMaxY', 'boundingBoxMaxZ',
                 'boundingBoxSize', 'boundingBoxSizeX', 'boundingBoxSizeY', 'boundingBoxSizeZ', 'center',
                 'boundingBoxCenterX', 'boundingBoxCenterY', 'boundingBoxCenterZ', 'matrix', 'inverseMatrix',
                 'worldMatrix', 'worldInverseMatrix', 'parentMatrix', 'parentInverseMatrix', 'visibility',
                 'intermediateObject', 'template', 'instObjGroups', 'objectColorRGB', 'objectColorR', 'objectColorG',
                 'objectColorB', 'wireColorRGB', 'wireColorR', 'wireColorG', 'wireColorB', 'useObjectColor',
                 'objectColor', 'drawOverride', 'overrideDisplayType', 'overrideLevelOfDetail', 'overrideShading',
                 'overrideTexturing', 'overridePlayback', 'overrideEnabled', 'overrideVisibility', 'hideOnPlayback',
                 'overrideRGBColors', 'overrideColor', 'overrideColorRGB', 'overrideColorR', 'overrideColorG',
                 'overrideColorB', 'overrideColorA', 'lodVisibility', 'selectionChildHighlighting', 'renderInfo',
                 'identification', 'layerRenderable', 'layerOverrideColor', 'renderLayerInfo', 'ghosting',
                 'ghostingMode', 'ghostCustomSteps', 'ghostPreFrames', 'ghostPostFrames', 'ghostsStep', 'ghostFrames',
                 'ghostOpacityRange', 'ghostFarOpacity', 'ghostNearOpacity', 'ghostColorPre', 'ghostColorPreR',
                 'ghostColorPreG', 'ghostColorPreB', 'ghostColorPost', 'ghostColorPostR', 'ghostColorPostG',
                 'ghostColorPostB', 'ghostDriver', 'ghostUseDriver', 'hiddenInOutliner', 'useOutlinerColor',
                 'outlinerColor', 'outlinerColorR', 'outlinerColorG', 'outlinerColorB', 'translate', 'translateX',
                 'translateY', 'translateZ', 'rotate', 'rotateX', 'rotateY', 'rotateZ', 'rotateOrder', 'scale',
                 'scaleX', 'scaleY', 'scaleZ', 'shear', 'shearXY', 'shearXZ', 'shearYZ', 'rotatePivot', 'rotatePivotX',
                 'rotatePivotY', 'rotatePivotZ', 'rotatePivotTranslate', 'rotatePivotTranslateX',
                 'rotatePivotTranslateY', 'rotatePivotTranslateZ', 'scalePivot', 'scalePivotX', 'scalePivotY',
                 'scalePivotZ', 'scalePivotTranslate', 'scalePivotTranslateX', 'scalePivotTranslateY',
                 'scalePivotTranslateZ', 'rotateAxis', 'rotateAxisX', 'rotateAxisY', 'rotateAxisZ',
                 'transMinusRotatePivot', 'transMinusRotatePivotX', 'transMinusRotatePivotY', 'transMinusRotatePivotZ',
                 'minTransLimit', 'minTransXLimit', 'minTransYLimit', 'minTransZLimit', 'maxTransLimit',
                 'maxTransXLimit', 'maxTransYLimit', 'maxTransZLimit', 'minTransLimitEnable', 'minTransXLimitEnable',
                 'minTransYLimitEnable', 'minTransZLimitEnable', 'maxTransLimitEnable', 'maxTransXLimitEnable',
                 'maxTransYLimitEnable', 'maxTransZLimitEnable', 'minRotLimit', 'minRotXLimit', 'minRotYLimit',
                 'minRotZLimit', 'maxRotLimit', 'maxRotXLimit', 'maxRotYLimit', 'maxRotZLimit', 'minRotLimitEnable',
                 'minRotXLimitEnable', 'minRotYLimitEnable', 'minRotZLimitEnable', 'maxRotLimitEnable',
                 'maxRotXLimitEnable', 'maxRotYLimitEnable', 'maxRotZLimitEnable', 'minScaleLimit', 'minScaleXLimit',
                 'minScaleYLimit', 'minScaleZLimit', 'maxScaleLimit', 'maxScaleXLimit', 'maxScaleYLimit',
                 'maxScaleZLimit', 'minScaleLimitEnable', 'minScaleXLimitEnable', 'minScaleYLimitEnable',
                 'minScaleZLimitEnable', 'maxScaleLimitEnable', 'maxScaleXLimitEnable', 'maxScaleYLimitEnable',
                 'maxScaleZLimitEnable', 'offsetParentMatrix', 'dagLocalMatrix', 'dagLocalInverseMatrix', 'geometry',
                 'xformMatrix', 'selectHandle', 'selectHandleX', 'selectHandleY', 'selectHandleZ', 'inheritsTransform',
                 'displayHandle', 'displayScalePivot', 'displayRotatePivot', 'displayLocalAxis', 'dynamics',
                 'showManipDefault', 'specifiedManipLocation', 'rotateQuaternion', 'rotateQuaternionX',
                 'rotateQuaternionY', 'rotateQuaternionZ', 'rotateQuaternionW', 'rotationInterpolation', 'msg', 'cch',
                 'fzn', 'ihi', 'nds', 'hl', 'isc', 'bbx', 'boc', 'pni', 'tna', 'tpt', 'vwn', 'icn', 'vwm', 'tpv', 'uit',
                 'ctrt', 'ctor', 'cdat', 'ctyp', 'bb', 'bbmn', 'bbnx', 'bbny', 'bbnz', 'bbmx', 'bbxx', 'bbxy', 'bbxz',
                 'bbsi', 'bbsx', 'bbsy', 'bbsz', 'c', 'bcx', 'bcy', 'bcz', 'm', 'im', 'wm', 'wim', 'pm', 'pim', 'v',
                 'io', 'tmp', 'iog', 'obcc', 'obcr', 'obcg', 'obcb', 'wfcc', 'wfcr', 'wfcg', 'wfcb', 'uoc', 'oc', 'do',
                 'ovdt', 'ovlod', 'ovs', 'ovt', 'ovp', 'ove', 'ovv', 'hpb', 'ovrgbf', 'ovc', 'ovrgb', 'ovcr', 'ovcg',
                 'ovcb', 'ovca', 'lodv', 'sech', 'ri', 'rlid', 'rndr', 'lovc', 'rlio', 'gh', 'gm', 'gcs', 'gprf',
                 'gpof', 'gstp', 'gf', 'golr', 'gfro', 'gnro', 'gcp', 'grr', 'gpg', 'gpb', 'gac', 'gar', 'gag', 'gab',
                 'gdr', 'gud', 'hio', 'uocol', 'oclr', 'oclrr', 'oclrg', 'oclrb', 't', 'tx', 'ty', 'tz', 'r', 'rx',
                 'ry', 'rz', 'ro', 's', 'sx', 'sy', 'sz', 'sh', 'shxy', 'shxz', 'shyz', 'rp', 'rpx', 'rpy', 'rpz',
                 'rpt', 'rptx', 'rpty', 'rptz', 'sp', 'spx', 'spy', 'spz', 'spt', 'sptx', 'spty', 'sptz', 'ra', 'rax',
                 'ray', 'raz', 'tmrp', 'tmrx', 'tmry', 'tmrz', 'mntl', 'mtxl', 'mtyl', 'mtzl', 'mxtl', 'xtxl', 'xtyl',
                 'xtzl', 'mtle', 'mtxe', 'mtye', 'mtze', 'xtle', 'xtxe', 'xtye', 'xtze', 'mnrl', 'mrxl', 'mryl', 'mrzl',
                 'mxrl', 'xrxl', 'xryl', 'xrzl', 'mrle', 'mrxe', 'mrye', 'mrze', 'xrle', 'xrxe', 'xrye', 'xrze', 'mnsl',
                 'msxl', 'msyl', 'mszl', 'mxsl', 'xsxl', 'xsyl', 'xszl', 'msle', 'msxe', 'msye', 'msze', 'xsle', 'xsxe',
                 'xsye', 'xsze', 'opm', 'dlm', 'dlim', 'g', 'xm', 'hdl', 'hdlx', 'hdly', 'hdlz', 'it', 'dh', 'dsp',
                 'drp', 'dla', 'dyn', 'smd', 'sml', 'rq', 'rqx', 'rqy', 'rqz', 'rqw', 'roi']
    _CREATE_STR = 'transform'
    root_space = XSpace.transform_root

    def __init__(self, name):
        super().__init__(name)
        self.top_group = None

    @classmethod
    def set_root_space(cls, root):
        cls.root_space = root

    @classmethod
    def create(cls, name=None, **kwargs):
        if cls.root_space:
            instance = super().create(name, under=cls.root_space, **kwargs)
        else:
            instance = super().create(name, **kwargs)
        return instance

    @property
    def children(self):
        children = mc.listRelatives(self.name, children=True, allDescendents=True)
        if not children:
            return None
        else:
            return [MTransform(node) for node in children]

    @property
    def child(self):
        if self.children and len(self.children) == 1:
            return self.children[0]
        else:
            raise RuntimeError(
                f'Can not use child attribute while a node has more than one child,please use children instead.')

    @property
    def world_pos(self):
        pos = mc.xform(self.name, worldSpace=True, translation=True, q=True)
        return om.MVector(pos)

    @property
    def local_pos(self):
        pos = mc.xform(self.name, worldSpace=False, translation=True, q=True)
        return om.MVector(pos)

    @property
    def parent(self):
        p = mc.listRelatives(self.name, parent=True)
        if p is None:
            return None
        elif isinstance(p, list) and len(p) == 1:
            return MTransform(p[0])
        else:
            raise RuntimeError(f'Failed to retrive parent of {self.name}\nresult:{p}')

    def set_parent(self, parent):
        if parent is None:
            if self.parent is None:
                return True
            else:
                mc.parent(self.name, world=True)
                return True
        elif mc.objExists(str(parent)):
            mc.parent(self.name, str(parent))
            return True
        else:
            raise RuntimeError(f'Parent object do not exist :{parent}')

    def insert_parent(self, name):
        pass

    def unparent(self):
        pass

    def match(self, other, **kwargs):
        if isinstance(other, str):
            other = MTransform(other)
        mc.matchTransform(self.name, other.name, **kwargs)

    def match_pos(self, pos, world=True):
        if isinstance(pos, om.MVector):
            pos = [i for i in pos]
        mc.xform(self.name, worldSpace=world, translation=pos)

    def match_rotatation(self, rot, world=True):
        mc.xform(self.name, worldSpace=world, rotation=rot, e=True)

    def move_by(self, vec, world=True):
        if isinstance(vec, list) and len(vec) == 3:
            vec = om.MVector(*vec)
        else:
            raise RuntimeError(f'Wrong vector format:{vec}')
        pos_after = self.world_pos + vec if world else self.local_pos + vec
        self.match_pos(pos_after)

    def set_visibility(self, visibility: bool):
        pass

    def get_vector_to(self, other):
        if isinstance(other, str):
            other = MTransform(other)
        vec = om.MVector(other.world_pos) - om.MVector(self.world_pos)
        return vec

    def reorient(self, aim_vec, up_vec, aim_axis, up_axis):
        pass


class MLocator(MTransform):
    _CREATE_STR = 'locator'
    root_space = XSpace.locator_root

    def __init__(self, name):
        super().__init__(name)


class MJoint(MTransform):
    _CREATE_STR = 'joint'
    root_space = XSpace.joint_root
    __slots__ = ['message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState', 'hyperLayout', 'isCollapsed',
                 'blackBox', 'borderConnections', 'publishedNodeInfo', 'templateName', 'templatePath', 'viewName',
                 'iconName', 'viewMode', 'templateVersion', 'uiTreatment', 'customTreatment', 'creator', 'creationDate',
                 'containerType', 'boundingBox', 'boundingBoxMin', 'boundingBoxMinX', 'boundingBoxMinY',
                 'boundingBoxMinZ', 'boundingBoxMax', 'boundingBoxMaxX', 'boundingBoxMaxY', 'boundingBoxMaxZ',
                 'boundingBoxSize', 'boundingBoxSizeX', 'boundingBoxSizeY', 'boundingBoxSizeZ', 'center',
                 'boundingBoxCenterX', 'boundingBoxCenterY', 'boundingBoxCenterZ', 'matrix', 'inverseMatrix',
                 'worldMatrix', 'worldInverseMatrix', 'parentMatrix', 'parentInverseMatrix', 'visibility',
                 'intermediateObject', 'template', 'instObjGroups', 'objectColorRGB', 'objectColorR', 'objectColorG',
                 'objectColorB', 'wireColorRGB', 'wireColorR', 'wireColorG', 'wireColorB', 'useObjectColor',
                 'objectColor', 'drawOverride', 'overrideDisplayType', 'overrideLevelOfDetail', 'overrideShading',
                 'overrideTexturing', 'overridePlayback', 'overrideEnabled', 'overrideVisibility', 'hideOnPlayback',
                 'overrideRGBColors', 'overrideColor', 'overrideColorRGB', 'overrideColorR', 'overrideColorG',
                 'overrideColorB', 'overrideColorA', 'lodVisibility', 'selectionChildHighlighting', 'renderInfo',
                 'identification', 'layerRenderable', 'layerOverrideColor', 'renderLayerInfo', 'ghosting',
                 'ghostingMode', 'ghostCustomSteps', 'ghostPreFrames', 'ghostPostFrames', 'ghostsStep', 'ghostFrames',
                 'ghostOpacityRange', 'ghostFarOpacity', 'ghostNearOpacity', 'ghostColorPre', 'ghostColorPreR',
                 'ghostColorPreG', 'ghostColorPreB', 'ghostColorPost', 'ghostColorPostR', 'ghostColorPostG',
                 'ghostColorPostB', 'ghostDriver', 'ghostUseDriver', 'hiddenInOutliner', 'useOutlinerColor',
                 'outlinerColor', 'outlinerColorR', 'outlinerColorG', 'outlinerColorB', 'translate', 'translateX',
                 'translateY', 'translateZ', 'rotate', 'rotateX', 'rotateY', 'rotateZ', 'rotateOrder', 'scale',
                 'scaleX', 'scaleY', 'scaleZ', 'shear', 'shearXY', 'shearXZ', 'shearYZ', 'rotatePivot', 'rotatePivotX',
                 'rotatePivotY', 'rotatePivotZ', 'rotatePivotTranslate', 'rotatePivotTranslateX',
                 'rotatePivotTranslateY', 'rotatePivotTranslateZ', 'scalePivot', 'scalePivotX', 'scalePivotY',
                 'scalePivotZ', 'scalePivotTranslate', 'scalePivotTranslateX', 'scalePivotTranslateY',
                 'scalePivotTranslateZ', 'rotateAxis', 'rotateAxisX', 'rotateAxisY', 'rotateAxisZ',
                 'transMinusRotatePivot', 'transMinusRotatePivotX', 'transMinusRotatePivotY', 'transMinusRotatePivotZ',
                 'minTransLimit', 'minTransXLimit', 'minTransYLimit', 'minTransZLimit', 'maxTransLimit',
                 'maxTransXLimit', 'maxTransYLimit', 'maxTransZLimit', 'minTransLimitEnable', 'minTransXLimitEnable',
                 'minTransYLimitEnable', 'minTransZLimitEnable', 'maxTransLimitEnable', 'maxTransXLimitEnable',
                 'maxTransYLimitEnable', 'maxTransZLimitEnable', 'minRotLimit', 'minRotXLimit', 'minRotYLimit',
                 'minRotZLimit', 'maxRotLimit', 'maxRotXLimit', 'maxRotYLimit', 'maxRotZLimit', 'minRotLimitEnable',
                 'minRotXLimitEnable', 'minRotYLimitEnable', 'minRotZLimitEnable', 'maxRotLimitEnable',
                 'maxRotXLimitEnable', 'maxRotYLimitEnable', 'maxRotZLimitEnable', 'minScaleLimit', 'minScaleXLimit',
                 'minScaleYLimit', 'minScaleZLimit', 'maxScaleLimit', 'maxScaleXLimit', 'maxScaleYLimit',
                 'maxScaleZLimit', 'minScaleLimitEnable', 'minScaleXLimitEnable', 'minScaleYLimitEnable',
                 'minScaleZLimitEnable', 'maxScaleLimitEnable', 'maxScaleXLimitEnable', 'maxScaleYLimitEnable',
                 'maxScaleZLimitEnable', 'offsetParentMatrix', 'dagLocalMatrix', 'dagLocalInverseMatrix', 'geometry',
                 'xformMatrix', 'selectHandle', 'selectHandleX', 'selectHandleY', 'selectHandleZ', 'inheritsTransform',
                 'displayHandle', 'displayScalePivot', 'displayRotatePivot', 'displayLocalAxis', 'dynamics',
                 'showManipDefault', 'specifiedManipLocation', 'rotateQuaternion', 'rotateQuaternionX',
                 'rotateQuaternionY', 'rotateQuaternionZ', 'rotateQuaternionW', 'rotationInterpolation', 'jointTypeX',
                 'jointTypeY', 'jointTypeZ', 'jointOrient', 'jointOrientX', 'jointOrientY', 'jointOrientZ',
                 'segmentScaleCompensate', 'inverseScale', 'inverseScaleX', 'inverseScaleY', 'inverseScaleZ',
                 'stiffness', 'stiffnessX', 'stiffnessY', 'stiffnessZ', 'preferredAngle', 'preferredAngleX',
                 'preferredAngleY', 'preferredAngleZ', 'minRotateDampRange', 'minRotateDampRangeX',
                 'minRotateDampRangeY', 'minRotateDampRangeZ', 'minRotateDampStrength', 'minRotateDampStrengthX',
                 'minRotateDampStrengthY', 'minRotateDampStrengthZ', 'maxRotateDampRange', 'maxRotateDampRangeX',
                 'maxRotateDampRangeY', 'maxRotateDampRangeZ', 'maxRotateDampStrength', 'maxRotateDampStrengthX',
                 'maxRotateDampStrengthY', 'maxRotateDampStrengthZ', 'bindPose', 'drawStyle', 'drawLabel', 'radius',
                 'hikNodeID', 'hikFkJoint', 'msg', 'cch', 'fzn', 'ihi', 'nds', 'hl', 'isc', 'bbx', 'boc', 'pni', 'tna',
                 'tpt', 'vwn', 'icn', 'vwm', 'tpv', 'uit', 'ctrt', 'ctor', 'cdat', 'ctyp', 'bb', 'bbmn', 'bbnx', 'bbny',
                 'bbnz', 'bbmx', 'bbxx', 'bbxy', 'bbxz', 'bbsi', 'bbsx', 'bbsy', 'bbsz', 'c', 'bcx', 'bcy', 'bcz', 'm',
                 'im', 'wm', 'wim', 'pm', 'pim', 'v', 'io', 'tmp', 'iog', 'obcc', 'obcr', 'obcg', 'obcb', 'wfcc',
                 'wfcr', 'wfcg', 'wfcb', 'uoc', 'oc', 'do', 'ovdt', 'ovlod', 'ovs', 'ovt', 'ovp', 'ove', 'ovv', 'hpb',
                 'ovrgbf', 'ovc', 'ovrgb', 'ovcr', 'ovcg', 'ovcb', 'ovca', 'lodv', 'sech', 'ri', 'rlid', 'rndr', 'lovc',
                 'rlio', 'gh', 'gm', 'gcs', 'gprf', 'gpof', 'gstp', 'gf', 'golr', 'gfro', 'gnro', 'gcp', 'grr', 'gpg',
                 'gpb', 'gac', 'gar', 'gag', 'gab', 'gdr', 'gud', 'hio', 'uocol', 'oclr', 'oclrr', 'oclrg', 'oclrb',
                 't', 'tx', 'ty', 'tz', 'r', 'rx', 'ry', 'rz', 'ro', 's', 'sx', 'sy', 'sz', 'sh', 'shxy', 'shxz',
                 'shyz', 'rp', 'rpx', 'rpy', 'rpz', 'rpt', 'rptx', 'rpty', 'rptz', 'sp', 'spx', 'spy', 'spz', 'spt',
                 'sptx', 'spty', 'sptz', 'ra', 'rax', 'ray', 'raz', 'tmrp', 'tmrx', 'tmry', 'tmrz', 'mntl', 'mtxl',
                 'mtyl', 'mtzl', 'mxtl', 'xtxl', 'xtyl', 'xtzl', 'mtle', 'mtxe', 'mtye', 'mtze', 'xtle', 'xtxe', 'xtye',
                 'xtze', 'mnrl', 'mrxl', 'mryl', 'mrzl', 'mxrl', 'xrxl', 'xryl', 'xrzl', 'mrle', 'mrxe', 'mrye', 'mrze',
                 'xrle', 'xrxe', 'xrye', 'xrze', 'mnsl', 'msxl', 'msyl', 'mszl', 'mxsl', 'xsxl', 'xsyl', 'xszl', 'msle',
                 'msxe', 'msye', 'msze', 'xsle', 'xsxe', 'xsye', 'xsze', 'opm', 'dlm', 'dlim', 'g', 'xm', 'hdl', 'hdlx',
                 'hdly', 'hdlz', 'it', 'dh', 'dsp', 'drp', 'dla', 'dyn', 'smd', 'sml', 'rq', 'rqx', 'rqy', 'rqz', 'rqw',
                 'roi', 'jtx', 'jty', 'jtz', 'jo', 'jox', 'joy', 'joz', 'ssc', 'is', 'isx', 'isy', 'isz', 'st', 'stx',
                 'sty', 'stz', 'pa', 'pax', 'pay', 'paz', 'ndr', 'ndx', 'ndy', 'ndz', 'nst', 'nstx', 'nsty', 'nstz',
                 'xdr', 'xdx', 'xdy', 'xdz', 'xst', 'xstx', 'xsty', 'xstz', 'bps', 'ds', 'dl', 'radi', 'hni', 'hfk']

    @classmethod
    def create(cls, name=None, **kwargs):
        instance = super().create(name, **kwargs)
        return instance


class MTransformList(object):
    MEMBER_TYPE = MTransform

    def __init__(self, mt_names):
        self.node_names = mt_names
        self.nodes = []
        self.positions = []
        self._init_node_list()
        self.length = len(self.node_names)

    def __getitem__(self, idx) -> MTransform:
        return self.nodes[idx]

    def __iter__(self) -> Iterator[MTransform]:
        return iter(self.nodes)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.length}):{self.node_names}'

    def _init_node_list(self):
        lst_types = mb.get_list_types(self.node_names)
        if len(lst_types) > 1:
            raise ValueError(f'Input joint list:{self.nodes} has more than one type:{lst_types}')
        if lst_types[0] == str:
            self.nodes = [self.MEMBER_TYPE(name) for name in self.node_names]
        elif lst_types[0] == self.MEMBER_TYPE:
            self.nodes = self.node_names
            self.node_names = [jnt.name for jnt in self.node_names]

    @classmethod
    def create(cls, names: list):
        exist = mb.check_list_exist(names)
        nodes_created = []
        if not exist:
            for name in names:
                node = cls.MEMBER_TYPE.create(name=name)
                nodes_created.append(node)
            return cls(nodes_created)
        else:
            return cls(names)

    def unparent_all(self, tmp_group=None):

        for node in self.nodes:
            node.set_parent(tmp_group)

    def parent_all(self, reverse=False):
        self.unparent_all()
        to_reparent = self.nodes
        if reverse:
            to_reparent = self.nodes[::-1]
        for i, node in enumerate(to_reparent):
            if i < 1:
                continue
            node.set_parent(to_reparent[i - 1])


class MJointSet(MTransformList):
    MEMBER_TYPE = MJoint

    def __init__(self, joints: list):
        super().__init__(joints)

    def __getitem__(self, idx) -> Union[MJoint, 'MJointSet']:
        if isinstance(idx, slice):
            return MJointSet(self.nodes[idx])
        else:
            return MJoint(self.nodes[idx])

    def __iter__(self) -> Iterator[MJoint]:
        return iter(self.nodes)


class MJointChain(MJointSet):

    def __init__(self, joints: list):
        super().__init__(joints)

    def __getitem__(self, idx) -> Union[MJoint, 'MJointChain']:
        if isinstance(idx, slice):
            return MJointChain(self.nodes[idx])
        else:
            return MJoint(self.nodes[idx])

    @classmethod
    def create(cls, joints: list[str]):
        instance = super().create(joints)
        instance.parent_all()
        return cls(instance.node_names)

    def update_chain(self):
        self.unparent_all()
        self.parent_all()

    def convert_to_curve(self):
        pass

    def duplicate(self):
        pass

    def reorient(self):
        pass

    def reverse_chain(self):
        self.unparent_all()
        self.parent_all(reverse=True)


class MTripleJointChain(MJointChain):

    def __init__(self, joints):
        super().__init__(joints)

    def __getitem__(self, idx) -> Union[MJoint, 'MTripleJointChain']:
        if isinstance(idx, slice):
            return MTripleJointChain(self.nodes[idx])
        else:
            return MJoint(self.nodes[idx])

    @property
    def vec_ab(self):
        pass

    @property
    def vec_ac(self):
        pass

    @property
    def vec_bc(self):
        pass

    @property
    def pole_vec_pos(self):
        pass

    @property
    def normal(self):
        pass

    @property
    def length(self):
        pass


class MQuadJointChain(MJointChain):

    def __init__(self, joints):
        super().__init__(joints)

    def __getitem__(self, idx) -> Union[MJoint, 'MQuadJointChain']:
        if isinstance(idx, slice):
            return MQuadJointChain(self.nodes[idx])
        else:
            return MJoint(self.nodes[idx])
