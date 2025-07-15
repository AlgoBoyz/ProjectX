import logging
import os.path
from typing import Optional

from maya.cmds import polyPlane

import maya.cmds as mc
import maya.api.OpenMaya as om
from .MNodes import MNode
from .MConstant import PROJECT_BASE_DIR, Axis
from .MBaseFunctions import get_child, clamp_list
from .MTransform import MTransform
from .MData import MCurveData, MWeightData
from XTools.XFileTool import JsonFile


# from .MTransform import MTransform


class MShape(MNode):
    def __init__(self, shape_node):
        super().__init__(shape_node)

    @property
    def transform_node(self):
        parent = mc.listRelatives(self.name, parent=True)
        return MTransform(parent)


class MMesh(MShape):
    _CREATE_STR = 'polyPlane'

    def __init__(self, shape_node):
        super().__init__(shape_node)

    @classmethod
    def create(cls, name=None, **kwargs):
        if not name:
            name = cls._CREATE_STR
        node = mc.polyPlane(name=name)[1]
        return cls(node)

    def export_weight(self):
        pass

    @property
    def vert_num(self):
        return om.MFnMesh(self.dp_node).numVertices


class MCurve(MShape):
    __slots__ = ['message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState', 'binMembership',
                 'hyperLayout', 'isCollapsed', 'blackBox', 'borderConnections', 'isHierarchicalConnection',
                 'publishedNodeInfo', 'rmbCommand', 'templateName', 'templatePath', 'viewName', 'iconName', 'viewMode',
                 'templateVersion', 'uiTreatment', 'customTreatment', 'creator', 'creationDate', 'containerType',
                 'boundingBox', 'boundingBoxMin', 'boundingBoxMinX', 'boundingBoxMinY', 'boundingBoxMinZ',
                 'boundingBoxMax', 'boundingBoxMaxX', 'boundingBoxMaxY', 'boundingBoxMaxZ', 'boundingBoxSize',
                 'boundingBoxSizeX', 'boundingBoxSizeY', 'boundingBoxSizeZ', 'center', 'boundingBoxCenterX',
                 'boundingBoxCenterY', 'boundingBoxCenterZ', 'matrix', 'inverseMatrix', 'worldMatrix',
                 'worldInverseMatrix', 'parentMatrix', 'parentInverseMatrix', 'visibility', 'intermediateObject',
                 'template', 'instObjGroups', 'objectColorRGB', 'objectColorR', 'objectColorG', 'objectColorB',
                 'wireColorRGB', 'wireColorR', 'wireColorG', 'wireColorB', 'useObjectColor', 'objectColor',
                 'drawOverride', 'overrideDisplayType', 'overrideLevelOfDetail', 'overrideShading', 'overrideTexturing',
                 'overridePlayback', 'overrideEnabled', 'overrideVisibility', 'hideOnPlayback', 'overrideRGBColors',
                 'overrideColor', 'overrideColorRGB', 'overrideColorR', 'overrideColorG', 'overrideColorB',
                 'overrideColorA', 'lodVisibility', 'selectionChildHighlighting', 'renderInfo', 'identification',
                 'layerRenderable', 'layerOverrideColor', 'renderLayerInfo', 'ghosting', 'ghostingMode',
                 'ghostCustomSteps', 'ghostPreFrames', 'ghostPostFrames', 'ghostsStep', 'ghostFrames',
                 'ghostOpacityRange', 'ghostFarOpacity', 'ghostNearOpacity', 'ghostColorPre', 'ghostColorPreR',
                 'ghostColorPreG', 'ghostColorPreB', 'ghostColorPost', 'ghostColorPostR', 'ghostColorPostG',
                 'ghostColorPostB', 'ghostDriver', 'ghostUseDriver', 'hiddenInOutliner', 'useOutlinerColor',
                 'outlinerColor', 'outlinerColorR', 'outlinerColorG', 'outlinerColorB', 'renderType', 'renderVolume',
                 'visibleFraction', 'hardwareFogMultiplier', 'motionBlur', 'visibleInReflections',
                 'visibleInRefractions', 'castsShadows', 'receiveShadows', 'asBackground',
                 'maxVisibilitySamplesOverride', 'maxVisibilitySamples', 'geometryAntialiasingOverride',
                 'antialiasingLevel', 'shadingSamplesOverride', 'shadingSamples', 'maxShadingSamples',
                 'volumeSamplesOverride', 'volumeSamples', 'depthJitter', 'ignoreSelfShadowing', 'primaryVisibility',
                 'referenceObject', 'compInstObjGroups', 'componentTags', 'instMaterialAssign', 'pickTexture', 'tweak',
                 'relativeTweak', 'controlPoints', 'weights', 'tweakLocation', 'blindDataNodes', 'uvPivot', 'uvPivotX',
                 'uvPivotY', 'uvSet', 'currentUVSet', 'displayImmediate', 'displayColors', 'displayColorChannel',
                 'currentColorSet', 'colorSet', 'header', 'local', 'lineWidth', 'worldSpace', 'worldNormal',
                 'form', 'degree', 'spans', 'editPoints', 'cached', 'inPlace', 'dispCV', 'dispEP', 'dispHull',
                 'dispCurveEndPoints', 'dispGeometry', 'tweakSize', 'minMaxValue', 'minValue', 'maxValue',
                 'alwaysDrawOnTop']
    _CREATE_STR = 'nurbsCurve'

    def __init__(self, shape_node):
        super().__init__(shape_node)
        self._check_curve()
        self.curve_data = MCurveData.load_from_node(shape_node)

    def _check_curve(self):
        node_type = mc.nodeType(self.name)
        if node_type != self._CREATE_STR:
            raise RuntimeError(f'{self.name} is not a nurbscurve!')
        if not mc.objExists(f'{self.name}.cv[*]'):
            raise RuntimeError(f'{self.name} may has not points,please check it again.')

    @property
    def curve_fn(self):
        fn = om.MFnNurbsCurve(self.dag_path.fullPathName())
        return fn

    @property
    def points(self):
        pos = mc.xform(f'{self.name}.cv[*]', q=True, worldSpace=True, translation=True)
        if len(pos) == 0:
            raise RuntimeError(f'{self.name} has not points!')
        pos_array = [pos[i:i + 3] for i in range(0, len(pos), 3)]
        return pos_array

    @classmethod
    def create(cls, name=None, curve_data=None, space='', **kwargs):
        pos_array = [tuple(i) for i in curve_data.pos_array]
        curve = mc.curve(p=pos_array,
                         periodic=curve_data.periodic,
                         knot=curve_data.knots,
                         degree=curve_data.degree,
                         name=name)
        instance = cls(get_child(curve))
        return instance

    def set_color(self, color):
        pass

    def set_scale(self, scale_factor):
        pass

    def set_rotate(self, axis, degree):
        pass


class MSurface(MShape):
    __slots__ = ['message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState', 'binMembership',
                 'hyperLayout', 'isCollapsed', 'blackBox', 'borderConnections', 'isHierarchicalConnection',
                 'publishedNodeInfo', 'rmbCommand', 'templateName', 'templatePath', 'viewName', 'iconName', 'viewMode',
                 'templateVersion', 'uiTreatment', 'customTreatment', 'creator', 'creationDate', 'containerType',
                 'boundingBox', 'boundingBoxMin', 'boundingBoxMinX', 'boundingBoxMinY', 'boundingBoxMinZ',
                 'boundingBoxMax', 'boundingBoxMaxX', 'boundingBoxMaxY', 'boundingBoxMaxZ', 'boundingBoxSize',
                 'boundingBoxSizeX', 'boundingBoxSizeY', 'boundingBoxSizeZ', 'center', 'boundingBoxCenterX',
                 'boundingBoxCenterY', 'boundingBoxCenterZ', 'matrix', 'inverseMatrix', 'worldMatrix',
                 'worldInverseMatrix', 'parentMatrix', 'parentInverseMatrix', 'visibility', 'intermediateObject',
                 'template', 'instObjGroups', 'objectColorRGB', 'objectColorR', 'objectColorG', 'objectColorB',
                 'wireColorRGB', 'wireColorR', 'wireColorG', 'wireColorB', 'useObjectColor', 'objectColor',
                 'drawOverride', 'overrideDisplayType', 'overrideLevelOfDetail', 'overrideShading', 'overrideTexturing',
                 'overridePlayback', 'overrideEnabled', 'overrideVisibility', 'hideOnPlayback', 'overrideRGBColors',
                 'overrideColor', 'overrideColorRGB', 'overrideColorR', 'overrideColorG', 'overrideColorB',
                 'overrideColorA', 'lodVisibility', 'selectionChildHighlighting', 'renderInfo', 'identification',
                 'layerRenderable', 'layerOverrideColor', 'renderLayerInfo', 'ghosting', 'ghostingMode',
                 'ghostCustomSteps', 'ghostPreFrames', 'ghostPostFrames', 'ghostsStep', 'ghostFrames',
                 'ghostOpacityRange', 'ghostFarOpacity', 'ghostNearOpacity', 'ghostColorPre', 'ghostColorPreR',
                 'ghostColorPreG', 'ghostColorPreB', 'ghostColorPost', 'ghostColorPostR', 'ghostColorPostG',
                 'ghostColorPostB', 'ghostDriver', 'ghostUseDriver', 'hiddenInOutliner', 'useOutlinerColor',
                 'outlinerColor', 'outlinerColorR', 'outlinerColorG', 'outlinerColorB', 'renderType', 'renderVolume',
                 'visibleFraction', 'hardwareFogMultiplier', 'motionBlur', 'visibleInReflections',
                 'visibleInRefractions', 'castsShadows', 'receiveShadows', 'asBackground',
                 'maxVisibilitySamplesOverride', 'maxVisibilitySamples', 'geometryAntialiasingOverride',
                 'antialiasingLevel', 'shadingSamplesOverride', 'shadingSamples', 'maxShadingSamples',
                 'volumeSamplesOverride', 'volumeSamples', 'depthJitter', 'ignoreSelfShadowing', 'primaryVisibility',
                 'referenceObject', 'compInstObjGroups', 'componentTags', 'instMaterialAssign', 'pickTexture', 'tweak',
                 'relativeTweak', 'controlPoints', 'weights', 'tweakLocation', 'blindDataNodes', 'uvPivot', 'uvPivotX',
                 'uvPivotY', 'uvSet', 'currentUVSet', 'displayImmediate', 'displayColors', 'displayColorChannel',
                 'currentColorSet', 'colorSet', 'ignoreHwShader', 'doubleSided', 'opposite', 'holdOut', 'smoothShading',
                 'boundingBoxScale', 'boundingBoxScaleX', 'boundingBoxScaleY', 'boundingBoxScaleZ',
                 'featureDisplacement', 'initialSampleRate', 'extraSampleRate', 'textureThreshold', 'normalThreshold',
                 'displayHWEnvironment', 'collisionOffsetVelocityIncrement', 'collisionDepthVelocityIncrement',
                 'collisionOffsetVelocityMultiplier', 'collisionDepthVelocityMultiplier', 'header', 'create', 'local',
                 'worldSpace', 'divisionsU', 'divisionsV', 'curvePrecision', 'curvePrecisionShaded', 'simplifyMode',
                 'simplifyU', 'simplifyV', 'smoothEdge', 'smoothEdgeRatio', 'useChordHeight', 'objSpaceChordHeight',
                 'useChordHeightRatio', 'edgeSwap', 'useMinScreen', 'selCVDisp', 'dispCV', 'dispEP', 'dispHull',
                 'dispGeometry', 'dispOrigin', 'numberU', 'modeU', 'numberV', 'modeV', 'chordHeight',
                 'chordHeightRatio', 'minScreen', 'formU', 'formV', 'cached', 'trimFace', 'patchUVIds', 'inPlace',
                 'tweakSizeU', 'tweakSizeV', 'minMaxRangeU', 'minValueU', 'maxValueU', 'minMaxRangeV', 'minValueV',
                 'maxValueV', 'degreeUV', 'degreeU', 'degreeV', 'spansUV', 'spansU', 'spansV',
                 'displayRenderTessellation', 'renderTriangleCount', 'fixTextureWarp', 'gridDivisionPerSpanU',
                 'gridDivisionPerSpanV', 'explicitTessellationAttributes', 'uDivisionsFactor', 'vDivisionsFactor',
                 'curvatureTolerance', 'basicTessellationType', 'dispSF', 'normalsDisplayScale']

    def __init__(self, shape_node):
        super().__init__(shape_node)
