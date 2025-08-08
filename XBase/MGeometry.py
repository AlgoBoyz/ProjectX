import logging
import os
from typing import Union

import maya.cmds as mc
import maya.api.OpenMaya as om

from XBase.MTransform import MTransform
from XBase.MShape import MNurbsCurveShape
from XBase.MData import MCurveData, MWeightData
from XTools.XFileTool import JsonFile


# from .MTransform import MTransform





class MMesh(object):
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



class MSurface(object):
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

class MNurbsCurve(object):
    
    def __init__(self,transform:MTransform,shape:Union[MNurbsCurveShape,None]):
        self.transform = transform
        self.shape = shape
    
    @classmethod
    def create_by_prototype(cls,name,prototype):
        if prototype == '':
            return cls(MTransform.create(name),None)
        file_path = os.path.join(MCurveData.DATA_DIR,f'{prototype}.json')
        data_io = JsonFile(file_path)
        data = data_io.load()

        pos_array = [i[:3] for i in data['pos_array']]
        knots = data['knots']
        degree = data['degree']

        curve = mc.curve(name=name,p=pos_array,knot=knots,degree=degree)
        curve_mt = MTransform(curve)
        curve_shape = curve_mt.child
        m_curve_shape = MNurbsCurveShape(curve_shape.name)
        return cls(curve_mt,m_curve_shape)

    @classmethod
    def create_by_points(cls,name,points,degree = 3):
        curve = mc.curve(name=name,p=points,degree=degree)
        curve_mt = MTransform(curve)
        curve_shape = curve_mt.child
        m_curve_shape = MNurbsCurveShape(curve_shape.name)
        return cls(curve_mt,m_curve_shape)

    def replace_shape_by_prototype(self,prototype):
        pass

    @classmethod
    def create_on(cls,other:MTransform,name='',prototype='',suffix=None):
        if not name:
            name = f'{other.name}_Ctrl'
        instance = cls.create_by_prototype(name,prototype)
        instance.transform.match(other)
        other.set_parent(instance.transform)
        if suffix:
            for i in suffix:
                grp_name = f'{name}_{i}'
                instance.transform.insert_parent(grp_name)
        return instance
