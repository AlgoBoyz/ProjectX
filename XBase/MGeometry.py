import logging
import os.path
from typing import Optional

import maya.cmds as mc
import maya.api.OpenMaya as om
from maya.app.renderSetup.model.utils import isExistingType
from .MNodes import MNode
from .MConstant import PROJECT_BASE_DIR, Axis
from .MBaseFunctions import get_child,clamp_list
from XTools.XFileTool import JsonFile
from .MTransform import MTransform


# from .MTransform import MTransform


class MShape(MNode):
    def __init__(self, shape_node):
        super().__init__(shape_node)

    @property
    def transform_node(self):
        parent = mc.listRelatives(self.name, parent=True)
        return MTransform(parent)


class MMesh(MShape):
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
                 'collisionOffsetVelocityMultiplier', 'collisionDepthVelocityMultiplier', 'inMesh', 'outMesh',
                 'outGeometryClean', 'cachedInMesh', 'worldMesh', 'outSmoothMesh', 'cachedSmoothMesh', 'smoothWarn',
                 'smoothLevel', 'smoothDrawType', 'useGlobalSmoothDrawType', 'outSmoothMeshSubdError',
                 'showDisplacements', 'displacementType', 'loadTiledTextures', 'enableOpenCL', 'smoothTessLevel',
                 'smoothOsdColorizePatches', 'useOsdBoundaryMethods', 'osdVertBoundary', 'osdFvarBoundary',
                 'osdFvarPropagateCorners', 'osdSmoothTriangles', 'osdCreaseMethod', 'osdIndependentUVChannels',
                 'continuity', 'smoothUVs', 'keepBorder', 'boundaryRule', 'keepHardEdge', 'propagateEdgeHardness',
                 'keepMapBorders', 'smoothOffset', 'sofx', 'sofy', 'sofz', 'displaySubdComps',
                 'useSmoothPreviewForRender', 'renderSmoothLevel', 'useMaxEdgeLength', 'useMinEdgeLength',
                 'useMaxSubdivisions', 'useMaxUV', 'useMinScreen', 'useNumTriangles', 'numTriangles', 'maxEdgeLength',
                 'minEdgeLength', 'maxSubd', 'maxUv', 'minScreen', 'maxTriangles', 'pnts', 'vrts', 'edge', 'uvpt',
                 'colors', 'normals', 'face', 'faceColorIndices', 'creaseData', 'creaseVertexData', 'pinData',
                 'holeFaceData', 'colorPerVertex', 'vertexColor', 'normalPerVertex', 'vertexNormal', 'displayVertices',
                 'displayBorders', 'displayMapBorders', 'displayEdges', 'displayFacesWithGroupId', 'displayCenter',
                 'displayTriangles', 'displayUVs', 'displayItemNumbers', 'displayNonPlanar', 'backfaceCulling',
                 'vertexBackfaceCulling', 'vertexSize', 'uvSize', 'borderWidth', 'normalSize', 'normalType',
                 'displayNormal', 'displayTangent', 'tangentSpace', 'tangentSmoothingAngle', 'tangentNormalThreshold',
                 'allowTopologyMod', 'materialBlend', 'uvTweakLocation', 'userTrg', 'dispResolution', 'vertexIdMap',
                 'edgeIdMap', 'faceIdMap', 'displaySmoothMesh', 'smoothMeshSelectionMode', 'inForceNodeUVUpdate',
                 'outForceNodeUVUpdate', 'alwaysDrawOnTop', 'reuseTriangles', 'quadSplit', 'vertexNormalMethod',
                 'perInstanceIndex', 'perInstanceTag', 'displayAlphaAsGreyScale', 'displayColorAsGreyScale',
                 'displayRedColorChannel', 'displayGreenColorChannel', 'displayBlueColorChannel',
                 'displayInvisibleFaces', 'useMeshSculptCache', 'computeFromSculptCache', 'useMeshTexSculptCache',
                 'freeze', 'motionVectorColorSet', 'vertexColorSource']

    def __init__(self, shape_node):
        super().__init__(shape_node)


class CurveData(object):
    DATA_DIR = os.path.join(PROJECT_BASE_DIR, 'res', 'GeoData', 'NurbsCurve')

    def __init__(self, name):
        self.name = name
        self.pos_array = None
        self.pos_vec_array = None
        self.knots = None
        self.periodic = None
        self.degree = -1
        self.normal_vec = Axis.X
        self.data = None

        self.attrs = ['name', 'pos_array', 'knots', 'periodic', 'degree', 'normal_vec']

    def __repr__(self):
        repr_str = 'Curve data:\n'
        for key,val in self.data.items():
            repr_str+=f'{key}:{val}\n'
        return repr_str
    @classmethod
    def load_from_file(cls, file_path,shape_index=0):
        file_io = JsonFile(file_path)
        data = file_io.load()
        name = list(data.keys())[shape_index]
        instance = cls(name)
        instance.update_data(data[name])
        return instance

    @classmethod
    def load_from_node(cls, node_name):
        data = cls.collect_curve_data(node_name)[node_name]
        instance = CurveData(node_name)
        instance.update_data(data)

    @staticmethod
    def collect_curve_data(shape_dag_name):
        curve_fn = om.MFnNurbsCurve(om.MGlobal.getSelectionListByName(shape_dag_name).getDagPath(0))
        pos_array = [clamp_list(tuple(i)[:3]) for i in curve_fn.cvPositions()]
        knots = tuple(curve_fn.knots())
        degree = curve_fn.degree
        periodic = curve_fn.kPeriodic
        data = {shape_dag_name:{
            'pos_array':pos_array,
            'knots':knots,
            'degree':degree,
            'periodic':periodic
        }}
        return data

    @staticmethod
    def save_node_data(node_name,file_path = '',override=True):
        data = CurveData.collect_curve_data(node_name)
        if not file_path:
            file_path = os.path.join(CurveData.DATA_DIR,f'{node_name}.json')
        file_io = JsonFile.create(file_path,override=override)
        file_io.dump(data)

    def apply_data(self, data: dict):
        pass

    @staticmethod
    def deserialize_data(data:dict):
        data['pos_array'] = [om.MVector(i) for i in data['pos_array']]
        data['knots'] = om.MDoubleArray(data['knots'])
        return data

    @staticmethod
    def serialize_data(data):
        data['pos_array'] =  [tuple(i)[:3] for i in data['pos_array']]
        data['knots'] = tuple(data['knots'])
        return data

    def update_data(self,data):
        self.data = self.serialize_data(data)

        exclude = ['name','normal_vec']
        for item in self.attrs:
            if item in exclude:
                continue
            setattr(self,item,self.data[item])
    def check_validate(self):
        if self.pos_array is None or self.periodic is None or self.knots is None or self.degree == -1:
            raise ValueError(f'Invalid curve data,\n'
                             f'pos_array:{self.pos_array}\n'
                             f'periodic:{self.periodic}\n'
                             f'knots:{self.knots}\n'
                             f'degree:{self.degree}')


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
        self.curve_data = CurveData.load_from_node(shape_node)

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
