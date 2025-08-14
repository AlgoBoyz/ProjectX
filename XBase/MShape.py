import os.path
from typing import Union

import maya.cmds as mc
import maya.api.OpenMaya as om
from setuptools.command.rotate import rotate

from XBase.MBaseFunctions import OMUtils,undo_stack
from XBase.MData import MCurveData
from XBase.MNodes import MNode, MAttribute
from XBase.MConstant import Axis


class VirtualShape(object):

    __slots__ = ['hyperLayout', 'isCollapsed', 'blackBox', 'borderConnections', 'isHierarchicalConnection', 'publishedNodeInfo', 'publishedNode', 'isHierarchicalNode', 'publishedNodeType', 'rmbCommand', 'templateName', 'templatePath', 'viewName', 'iconName', 'viewMode', 'templateVersion', 'uiTreatment', 'customTreatment', 'creator', 'creationDate', 'containerType', 'boundingBox', 'boundingBoxMin', 'boundingBoxMinX', 'boundingBoxMinY', 'boundingBoxMinZ', 'boundingBoxMax', 'boundingBoxMaxX', 'boundingBoxMaxY', 'boundingBoxMaxZ', 'boundingBoxSize', 'boundingBoxSizeX', 'boundingBoxSizeY', 'boundingBoxSizeZ', 'center', 'boundingBoxCenterX', 'boundingBoxCenterY', 'boundingBoxCenterZ', 'matrix', 'inverseMatrix', 'worldMatrix', 'worldInverseMatrix', 'parentMatrix', 'parentInverseMatrix', 'visibility', 'intermediateObject', 'template', 'instObjGroups', 'objectGroups', 'objectGrpCompList', 'objectGroupId', 'objectGrpColor', 'objectColorRGB', 'objectColorR', 'objectColorG', 'objectColorB', 'wireColorRGB', 'wireColorR', 'wireColorG', 'wireColorB', 'useObjectColor', 'objectColor', 'drawOverride', 'overrideDisplayType', 'overrideLevelOfDetail', 'overrideShading', 'overrideTexturing', 'overridePlayback', 'overrideEnabled', 'overrideVisibility', 'hideOnPlayback', 'overrideRGBColors', 'overrideColor', 'overrideColorRGB', 'overrideColorR', 'overrideColorG', 'overrideColorB', 'overrideColorA', 'lodVisibility', 'selectionChildHighlighting', 'renderInfo', 'identification', 'layerRenderable', 'layerOverrideColor', 'renderLayerInfo', 'renderLayerId', 'renderLayerRenderable', 'renderLayerColor', 'ghosting', 'ghostingMode', 'ghostCustomSteps', 'ghostPreFrames', 'ghostPostFrames', 'ghostsStep', 'ghostFrames', 'ghostOpacityRange', 'ghostFarOpacity', 'ghostNearOpacity', 'ghostColorPre', 'ghostColorPreR', 'ghostColorPreG', 'ghostColorPreB', 'ghostColorPost', 'ghostColorPostR', 'ghostColorPostG', 'ghostColorPostB', 'ghostDriver', 'ghostUseDriver', 'renderType', 'renderVolume', 'visibleFraction', 'hardwareFogMultiplier', 'motionBlur', 'visibleInReflections', 'visibleInRefractions', 'castsShadows', 'receiveShadows', 'asBackground', 'maxVisibilitySamplesOverride', 'maxVisibilitySamples', 'geometryAntialiasingOverride', 'antialiasingLevel', 'shadingSamplesOverride', 'shadingSamples', 'maxShadingSamples', 'volumeSamplesOverride', 'volumeSamples', 'depthJitter', 'ignoreSelfShadowing', 'primaryVisibility', 'referenceObject', 'compInstObjGroups', 'compObjectGroups', 'compObjectGrpCompList', 'compObjectGroupId', 'componentTags', 'componentTagName', 'componentTagContents', 'instMaterialAssign', 'pickTexture', 'tweak', 'relativeTweak', 'controlPoints', 'xValue', 'yValue', 'zValue', 'weights', 'tweakLocation', 'blindDataNodes', 'uvPivot', 'uvPivotX', 'uvPivotY', 'uvSet', 'uvSetName', 'uvSetPoints', 'uvSetPointsU', 'uvSetPointsV', 'uvSetTweakLocation', 'currentUVSet', 'displayImmediate', 'displayColors', 'displayColorChannel', 'currentColorSet', 'colorSet', 'colorName', 'clamped', 'representation', 'colorSetPoints', 'colorSetPointsR', 'colorSetPointsG', 'colorSetPointsB', 'colorSetPointsA', 'header', 'create', 'local', 'lineWidth', 'worldSpace', 'worldNormal', 'worldNormalX', 'worldNormalY', 'worldNormalZ', 'form', 'degree', 'spans', 'editPoints', 'xValueEp', 'yValueEp', 'zValueEp', 'cached', 'inPlace', 'dispCV', 'dispEP', 'dispHull', 'dispCurveEndPoints', 'dispGeometry', 'tweakSize', 'minMaxValue', 'alwaysDrawOnTop', 'minValue', 'maxValue', 'hiddenInOutliner', 'useOutlinerColor', 'outlinerColor', 'outlinerColorR', 'outlinerColorG', 'outlinerColorB', 'underWorldObject', 'localPosition', 'localPositionX', 'localPositionY', 'localPositionZ', 'worldPosition', 'worldPositionX', 'worldPositionY', 'worldPositionZ', 'localScale', 'localScaleX', 'localScaleY', 'localScaleZ', 'ignoreHwShader', 'doubleSided', 'opposite', 'holdOut', 'smoothShading', 'boundingBoxScale', 'boundingBoxScaleX', 'boundingBoxScaleY', 'boundingBoxScaleZ', 'featureDisplacement', 'initialSampleRate', 'extraSampleRate', 'textureThreshold', 'normalThreshold', 'displayHWEnvironment', 'collisionOffsetVelocityIncrement', 'collisionOffsetVelocityIncrement_Position', 'collisionOffsetVelocityIncrement_FloatValue', 'collisionOffsetVelocityIncrement_Interp', 'collisionDepthVelocityIncrement', 'collisionDepthVelocityIncrement_Position', 'collisionDepthVelocityIncrement_FloatValue', 'collisionDepthVelocityIncrement_Interp', 'collisionOffsetVelocityMultiplier', 'collisionOffsetVelocityMultiplier_Position', 'collisionOffsetVelocityMultiplier_FloatValue', 'collisionOffsetVelocityMultiplier_Interp', 'collisionDepthVelocityMultiplier', 'collisionDepthVelocityMultiplier_Position', 'collisionDepthVelocityMultiplier_FloatValue', 'collisionDepthVelocityMultiplier_Interp', 'divisionsU', 'divisionsV', 'curvePrecision', 'curvePrecisionShaded', 'simplifyMode', 'simplifyU', 'simplifyV', 'smoothEdge', 'smoothEdgeRatio', 'useChordHeight', 'objSpaceChordHeight', 'useChordHeightRatio', 'edgeSwap', 'useMinScreen', 'selCVDisp', 'dispOrigin', 'numberU', 'modeU', 'numberV', 'modeV', 'chordHeight', 'chordHeightRatio', 'minScreen', 'formU', 'formV', 'trimFace', 'patchUVIds', 'tweakSizeU', 'tweakSizeV', 'minMaxRangeU', 'minMaxRangeV', 'degreeUV', 'spansUV', 'displayRenderTessellation', 'renderTriangleCount', 'fixTextureWarp', 'gridDivisionPerSpanU', 'gridDivisionPerSpanV', 'explicitTessellationAttributes', 'uDivisionsFactor', 'vDivisionsFactor', 'curvatureTolerance', 'basicTessellationType', 'dispSF', 'normalsDisplayScale', 'minValueU', 'maxValueU', 'minValueV', 'maxValueV', 'degreeU', 'degreeV', 'spansU', 'spansV']


class MShapeNode(VirtualShape):

    def __init__(self, shape_name):
        self.shape_name = shape_name

    def __getattr__(self, item):
        return MAttribute(self.shape_name, item)

    def get_shape_data(self):
        raise NotImplemented
class MLocatorShape(MShapeNode):

    def __init__(self, shape_name):
        super().__init__(shape_name)



class MNurbsCurveShape(MShapeNode):

    def __init__(self, shape_name):
        MShapeNode.__init__(self,shape_name)
        self._check_curve()

    def get_shape_data(self):
        data = MCurveData.load_from_node(self.shape_name)
        return data

    def _check_curve(self):
        node_type = mc.nodeType(self.shape_name)
        if node_type != 'nurbsCurve':
            raise RuntimeError(f'{self.shape_name} is not a nurbsCurve!')
        if not mc.objExists(f'{self.shape_name}.cv[*]'):
            raise RuntimeError(f'{self.shape_name} may has not points,please check it again.')

    @property
    def points(self):
        pos = mc.xform(f'{self.name}.cv[*]', q=True, worldSpace=True, translation=True)
        if len(pos) == 0:
            raise RuntimeError(f'{self.name} has not points!')
        pos_array = [pos[i:i + 3] for i in range(0, len(pos), 3)]
        return pos_array
    @property
    def shape_fn(self):
        return om.MFnNurbsCurve(OMUtils.get_dependency_node(self.shape_name))
    def set_color(self, color):
        self.overrideEnabled.set(1)
        self.overrideRGBColors.set(1)
        self.overrideColorRGB.set(color)

    def set_scale(self, scale_factor:Union[list,int]):
        if isinstance(scale_factor,int):
            scale_factor = [scale_factor,scale_factor,scale_factor]
        with undo_stack():
            for vert_idx in range(self.shape_fn.numCVs):
                vert_coord = mc.xform(f'{self.shape_name}.cv[{vert_idx}]',q=True,translation=True,objectSpace=True)
                coord = [i*j for i,j in zip(vert_coord,scale_factor)]
                mc.xform(f'{self.shape_name}.cv[{vert_idx}]',translation=coord,objectSpace=True)
    def set_rotate(self, axis, degree):
        rotation = [degree,0,0]
        if axis == Axis.X:
            rotation = [degree,0,0]
        elif axis == Axis.Y:
            rotation = [0,degree,0]
        elif axis == Axis.Z:
            rotation = [0,0,degree]

        with undo_stack():
            for vert_idx in range(self.shape_fn.numCVs):
                vert_coord = mc.xform(f'{self.shape_name}.cv[{vert_idx}]',q=True,translation=True,objectSpace=True)
                mc.xform(f'{self.shape_name}.cv[{vert_idx}]',rotation=rotation,objectSpace=True)

class MNurbsSurfaceShape(MShapeNode):

    def __init__(self, shape_name):
        MShapeNode.__init__(self,shape_name)
    @property
    def surface_fn(self):
        return om.MFnNurbsSurface(OMUtils.get_dag_path(self.shape_name))