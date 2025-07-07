import pdb

import maya.cmds as mc
from .MConstant import Sign, AttrType
from .MBaseFunctions import get_list_types


class VitualNode(object):
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
                 'rotateQuaternionY', 'rotateQuaternionZ', 'rotateQuaternionW', 'rotationInterpolation', 'renderType',
                 'renderVolume', 'visibleFraction', 'hardwareFogMultiplier', 'motionBlur', 'visibleInReflections',
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
                 'freeze', 'motionVectorColorSet', 'vertexColorSource', 'mikktspaceTangentGen', 'header',
                 'local', 'lineWidth', 'worldSpace', 'worldNormal', 'form', 'degree', 'spans', 'editPoints', 'cached',
                 'inPlace', 'dispCV', 'dispEP', 'dispHull', 'dispCurveEndPoints', 'dispGeometry', 'tweakSize',
                 'minMaxValue', 'minValue', 'maxValue', 'divisionsU', 'divisionsV', 'curvePrecision',
                 'curvePrecisionShaded', 'simplifyMode', 'simplifyU', 'simplifyV', 'smoothEdge', 'smoothEdgeRatio',
                 'useChordHeight', 'objSpaceChordHeight', 'useChordHeightRatio', 'edgeSwap', 'selCVDisp', 'dispOrigin',
                 'numberU', 'modeU', 'numberV', 'modeV', 'chordHeight', 'chordHeightRatio', 'formU', 'formV',
                 'trimFace', 'patchUVIds', 'tweakSizeU', 'tweakSizeV', 'minMaxRangeU', 'minValueU', 'maxValueU',
                 'minMaxRangeV', 'minValueV', 'maxValueV', 'degreeUV', 'degreeU', 'degreeV', 'spansUV', 'spansU',
                 'spansV', 'displayRenderTessellation', 'renderTriangleCount', 'fixTextureWarp', 'gridDivisionPerSpanU',
                 'gridDivisionPerSpanV', 'explicitTessellationAttributes', 'uDivisionsFactor', 'vDivisionsFactor',
                 'curvatureTolerance', 'basicTessellationType', 'dispSF', 'normalsDisplayScale', 'input',
                 'weightFunction', 'outputGeometry', 'originalGeometry', 'envelopeWeightsList', 'blockGPU', 'envelope',
                 'function', 'fchild1', 'fchild2', 'fchild3', 'map64BitIndices', 'skinningMethod', 'blendWeights',
                 'weightList', 'perInfluenceWeights', 'bindPreMatrix', 'geomMatrix', 'dropoffRate', 'dropoff',
                 'smoothness', 'lockWeights', 'maintainMaxInfluences', 'maxInfluences', 'relativeSpaceMode',
                 'relativeSpaceMatrix', 'bindMethod', 'driverPoints', 'basePoints', 'baseDirty', 'paintWeights',
                 'paintTrans', 'paintArrDirty', 'useComponents', 'nurbsSamples', 'useComponentsMatrix',
                 'normalizeWeights', 'weightDistribution', 'deformUserNormals', 'wtDrty', 'bindPose', 'bindVolume',
                 'heatmapFalloff', 'influenceColor', 'geomBind', 'dqsSupportNonRigid', 'dqsScale', 'dqsScaleX',
                 'dqsScaleY', 'dqsScaleZ', 'cacheSetup', 'topologyCheck', 'icon', 'inputTarget', 'origin', 'baseOrigin',
                 'baseOriginX', 'baseOriginY', 'baseOriginZ', 'targetOrigin', 'targetOriginX', 'targetOriginY',
                 'targetOriginZ', 'parallelBlender', 'useTargetCompWeights', 'supportNegativeWeights', 'offsetDeformer',
                 'offsetX', 'offsetY', 'offsetZ', 'localVertexFrame', 'midLayerId', 'midLayerParent', 'nextNode',
                 'parentDirectory', 'nextTarget', 'targetVisibility', 'targetParentVisibility', 'targetDirectory',
                 'deformationOrder', 'inbetweenInfoGroup', 'symmetryEdge', 'operation', 'input1', 'input1X', 'input1Y',
                 'input1Z', 'input2', 'input2X', 'input2Y', 'input2Z', 'output', 'outputX', 'outputY', 'outputZ',
                 'firstTerm', 'secondTerm', 'colorIfTrue', 'colorIfTrueR', 'colorIfTrueG', 'colorIfTrueB',
                 'colorIfFalse', 'colorIfFalseR', 'colorIfFalseG', 'colorIfFalseB', 'outColor', 'outColorR',
                 'outColorG', 'outColorB', 'jointOrientType', 'jointType', 'jointTypeX', 'jointTypeY', 'jointTypeZ',
                 'dofMask', 'jointOrient', 'jointOrientX', 'jointOrientY', 'jointOrientZ', 'segmentScaleCompensate',
                 'inverseScale', 'inverseScaleX', 'inverseScaleY', 'inverseScaleZ', 'stiffness', 'stiffnessX',
                 'stiffnessY', 'stiffnessZ', 'preferredAngle', 'preferredAngleX', 'preferredAngleY', 'preferredAngleZ',
                 'minRotateDampRange', 'minRotateDampRangeX', 'minRotateDampRangeY', 'minRotateDampRangeZ',
                 'minRotateDampStrength', 'minRotateDampStrengthX', 'minRotateDampStrengthY', 'minRotateDampStrengthZ',
                 'maxRotateDampRange', 'maxRotateDampRangeX', 'maxRotateDampRangeY', 'maxRotateDampRangeZ',
                 'maxRotateDampStrength', 'maxRotateDampStrengthX', 'maxRotateDampStrengthY', 'maxRotateDampStrengthZ',
                 'bindRotation', 'bindRotationX', 'bindRotationY', 'bindRotationZ', 'bindJointOrient',
                 'bindJointOrientX', 'bindJointOrientY', 'bindJointOrientZ', 'bindRotateAxis', 'bindRotateAxisX',
                 'bindRotateAxisY', 'bindRotateAxisZ', 'bindScale', 'bindScaleX', 'bindScaleY', 'bindScaleZ',
                 'bindInverseScale', 'bindInverseScaleX', 'bindInverseScaleY', 'bindInverseScaleZ',
                 'bindSegmentScaleCompensate', 'isIKDirtyFlag', 'inIKSolveFlag', 'drawStyle', 'drawLabel', 'side',
                 'type', 'otherType', 'ikRotate', 'ikRotateX', 'ikRotateY', 'ikRotateZ', 'fkRotate', 'fkRotateX',
                 'fkRotateY', 'fkRotateZ', 'radius', 'hikNodeID', 'hikFkJoint', 'underWorldObject', 'localPosition',
                 'localPositionX', 'localPositionY', 'localPositionZ', 'worldPosition', 'localScale', 'localScaleX',
                 'localScaleY', 'localScaleZ', 'matrixIn', 'matrixSum', 'inputMatrix', 'inputRotateOrder',
                 'outputTranslate', 'outputTranslateX', 'outputTranslateY', 'outputTranslateZ', 'outputRotate',
                 'outputRotateX', 'outputRotateY', 'outputRotateZ', 'outputScale', 'outputScaleX', 'outputScaleY',
                 'outputScaleZ', 'outputShear', 'outputShearX', 'outputShearY', 'outputShearZ', 'outputQuat',
                 'outputQuatX', 'outputQuatY', 'outputQuatZ', 'outputQuatW']


class MNode(VitualNode):
    _CREATE_STR = 'MNodeBase'

    def __init__(self, name):
        if name is None:
            raise RuntimeError(f'Can not initialize from None')
        if isinstance(name, self.__class__):
            print(f'Initializing from {self.__class__}')
            self.name = name.name
        else:
            self.name = name
        self.__check_exist()

    def __repr__(self):
        return f'{self.__class__.__name__} object in name of :{self.name}'

    def __getattr__(self, item):
        return MAttribute(self.name, item)

    def __str__(self):
        return self.name

    def __check_exist(self):
        if '.' in self.name:
            raise RuntimeError(f'Wrong format of node name:{self.name}')
        exist = mc.objExists(self.name)
        if not self.name:
            raise RuntimeError(f'Node name can not be empty!')
        if not exist:
            raise RuntimeError(f'Node:{self.name} do not exist!')

    @classmethod
    def create(cls, name=None, **kwargs):
        if not name:
            name = cls._CREATE_STR
        node = mc.createNode(cls._CREATE_STR, name=name)
        under = kwargs.pop('under', None)
        match = kwargs.pop('match', None)
        pos = kwargs.pop('posisition', kwargs.pop('pos', None))
        if kwargs:
            raise ValueError(f'Parameter:{kwargs} is not supported!')
        if under:
            if isinstance(under, str):
                mc.parent(node, under)
            elif isinstance(under, cls):
                mc.parent(node, under.name)
        if match:
            pass
        if pos:
            mc.xform(node, worldSpace=True, translation=pos)
        return cls(node)

    @property
    def connected_attrs(self, **kwargs):
        connected = mc.listConnections(self.name, **kwargs)
        if connected:
            return connected
        else:
            return None

    @property
    def node_type(self):
        return mc.objectType(self.name)

    @property
    def history(self):
        return mc.listHistory(self.name)

    @property
    def dp_node(self):
        import maya.api.OpenMaya as om
        sel_list: om.MSelectionList = om.MGlobal.getSelectionListByName(self.name)
        dp_node: om.MObject = sel_list.getDependNode(0)
        return dp_node

    @property
    def dag_path(self):
        import maya.api.OpenMaya as om
        sel_list: om.MSelectionList = om.MGlobal.getSelectionListByName(self.name)
        dag_path: om.MDagPath = sel_list.getDagPath(0)
        return dag_path

    def add_attr(self, attr_name: str, **kwargs):
        mc.addAttr(self.name, longName=attr_name, **kwargs)
        return MAttribute(self.name, attr_name)

    def add_to_set(self, set_name):
        pass

    def rename(self, new_name):
        mc.rename(self.name, new_name)

    def attr(self, item):

        return MAttribute(self.name, item)


class MAttribute(object):
    VALUE_ACCURACY = 5  # 数值精确到小数点后几位

    def __init__(self, node, attr_name):
        self.node = node
        self.attr_name = attr_name
        self.full_name = f'{self.node}.{self.attr_name}'
        self.__check_exist()
        self.attr_type = mc.getAttr(self.full_name, type=True)

    def __repr__(self):
        return f'MAttribue: {self.full_name}'

    def __str__(self):
        return self.full_name

    def __getitem__(self, item):
        if not self.attr_type in ['matrix']:
            raise RuntimeError(f'{AttrType} do not support index operation')
        try:
            res = mc.getAttr(f'{self.full_name}[{item}]')
            print(res)
        except:
            pass

    def __check_exist(self):
        exist = mc.objExists(self.full_name)
        if not exist:
            raise AttributeError(f'Attribute:({mc.objectType(self.node)}){self.full_name} do not exist!')

    @staticmethod
    def validate_attr(attr: str):
        # todo ：重写以支持复合属性
        if '.' not in attr:
            raise AttributeError(f'Wrong format of attribute:{attr}')
        if not mc.objExists(attr):
            raise AttributeError(f'Attibute:{attr} do not exist')
        splited = attr.split('.')
        if not splited or len(splited) != 2:
            raise AttributeError(f'Wrong format of attribute:{attr}')
        return splited

    @classmethod
    def create_by_name(cls, full_name: str):
        # todo ：重写以支持复合属性
        splited = cls.validate_attr(full_name)
        return cls(splited[0], splited[1])

    @property
    def value(self):
        v = mc.getAttr(self.full_name)
        if isinstance(v, tuple) or isinstance(v, list):
            lst_type = get_list_types(v)
            if lst_type == float:
                res = [round(i, self.VALUE_ACCURACY) for i in v]
                return res[0] if len(res) == 1 else res
            elif lst_type == list or lst_type == tuple and len(v) == 1:
                res = [round(i, self.VALUE_ACCURACY) for i in v[0]]
                return res
            else:
                return v
        else:
            return round(v, self.VALUE_ACCURACY) if isinstance(v, float) else v

    @property
    def sign(self):
        if not self.attr_type in ['float', 'double', 'int']:
            return None
        if self.value > 0:
            return Sign.Positive
        elif self.value == 0:
            return Sign.Zero
        elif self.value < 0:
            return Sign.Negative
        else:
            return None

    def connect(self, other, force=False, compund=False) -> 'MNode':
        other_node = ''
        if isinstance(other, str):
            if compund:
                node = other.split('.')[0]
                attr = other.split('.', 1)[1]
            else:
                node, attr = self.validate_attr(other)
            other_node = node
            mc.connectAttr(self.full_name, other, force=force)
            print(f'{self.full_name}>>{other}')
        elif isinstance(other, MAttribute):
            mc.connectAttr(self.full_name, other.full_name, force=force)
            other_node = other.node
            print(f'{self.full_name}>>{other.full_name}')
        elif isinstance(other, list):
            other_type = get_list_types(other)
            if not other_type != str and other_type != MAttribute:
                raise AttributeError(f'Wrong format of list of attibutes:{other}')
            for attr in other:
                self.connect(attr, force=force)
        else:
            raise RuntimeError(f'Not supported attibute to connect')
        return MNode(other_node)

    def disconnect(self):
        pass

    def set(self, value):
        if isinstance(value, list):
            print(self.full_name, value, len(value))
        if isinstance(value, int) and self.attr_type in ['double', 'float', 'doubleLinear', 'doubleAngle']:
            print(f'Assigning an int({value}) to a float or double ,convert the value to {float(value)}')
            value = float(value)
        if isinstance(value, MAttribute):
            value = value.value
        if self.attr_type in ['float3', 'double3', 'float2']:
            mc.setAttr(self.full_name, *value)
        elif self.attr_type in ['matrix']:
            mc.setAttr(self.full_name, value, type=self.attr_type)
        else:
            mc.setAttr(self.full_name, value)

    def get(self, raw=True):
        if raw:
            return mc.getAttr(self.full_name)
        else:
            return self.value

    def add(self, other, alias):
        from XBase.MMathNode import addDoubleLinear, colorMath
        if isinstance(other, str) and mc.objExists(other):
            node_name = other.split('.', 1)[0]
            attr_name = other.split('.', 1)[1]
            other = MAttribute(node_name, attr_name)
        if self.attr_type in AttrType.ValueType:
            add_node = addDoubleLinear.create(f'{alias}_adl')
            self.connect(add_node.input1)
            other.connect(add_node.input2)

        elif self.attr_type in AttrType.CompundType:
            add_node = colorMath.create(f'{alias}_clrm')
            add_node.operation.set(0)
            self.connect(add_node.colorA)
            other.connect(add_node.colorB)
        else:
            raise RuntimeError(f'Operation add do not support attibute type of :{self.attr_type}')
        return add_node

    def substract(self, other, alias):
        from XBase.MMathNode import floatMath, colorMath
        if isinstance(other, str) and mc.objExists(other):
            node_name = other.split('.', 1)[0]
            attr_name = other.split('.', 1)[1]
            other = MAttribute(node_name, attr_name)
        if self.attr_type in AttrType.ValueType:
            sub_node = floatMath.create(f'{alias}_flm')
            sub_node.operation.set(1)
            self.connect(sub_node.floatA)
            other.connect(sub_node.floatB)

        elif self.attr_type in AttrType.CompundType:
            sub_node = colorMath.create(f'{alias}_clrm')
            sub_node.operation.set(1)
            self.connect(sub_node.colorA)
            other.connect(sub_node.colorB)
        else:
            raise RuntimeError(f'Operation substract do not support attibute type of :{self.attr_type}')
        return sub_node

    def multiply(self, other, alias):
        from XBase.MMathNode import floatMath, colorMath
        if isinstance(other, str) and mc.objExists(other):
            node_name = other.split('.', 1)[0]
            attr_name = other.split('.', 1)[1]
            other = MAttribute(node_name, attr_name)
        # case 1: scalar * scalar
        # case 2: scalar * vector
        # case 3: scalar * matrix
        if self.attr_type in AttrType.ValueType:
            if other.attr_type in ['float3', 'double3']:
                mult_node = colorMath.create(f'{alias}_clrm')
                self.connect(mult_node.colorAR)
                self.connect(mult_node.colorAG)
                self.connect(mult_node.colorAB)
                other.connect(mult_node.colorB)
            elif other.attr_type == 'matrix':
                raise NotImplemented
            elif other.attr_type in AttrType.ValueType:
                mult_node = floatMath.create(f'{alias}_flm')
                mult_node.operation.set(2)
                self.connect(mult_node.floatA)
                other.connect(mult_node.floatB)

        # case 4: vector * matrix
        elif self.attr_type in ['float3', 'double3']:
            pass
