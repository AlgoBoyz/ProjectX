import maya.cmds as mc

from XBase.MAttribute import MAttribute


class VirtualNode(object):
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


class MNode(VirtualNode):
    _CREATE_STR = 'MNodeBase'

    def __init__(self, name):
        if name is None or name == '':
            raise RuntimeError(f'Can not initialize from None or empty string:{name}')
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
        if mc.nodeType(node) == 'unknown':
            raise RuntimeError(f'Failed to create node:{name},type:{cls._CREATE_STR}')

        return cls(node)

    @property
    def connected_attrs(self, **kwargs):
        connected = mc.listConnections(self.name, **kwargs)
        if connected:
            return connected
        else:
            return None

    @property
    def all_attrs(self):
        attrs = mc.attributeInfo(allAttributes=True, type=self._CREATE_STR)
        print(attrs)
        return attrs

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

    def rename(self, new_name, parent_instance=None):
        old_name = self.name
        mc.rename(self.name, new_name)
        self.name = new_name
        if parent_instance:
            name_idx = parent_instance.node_names.index(old_name)
            parent_instance.node_names[name_idx] = new_name
            parent_instance.nodes[name_idx] = parent_instance.MEMBER_TYPE(new_name)

    def attr(self, item):

        return MAttribute(self.name, item)


# todo:未来应新增一个MShaderNode.py文件，把这个类放进去
class MSurfaceShaderNode(MNode):
    _CREATE_STR = 'surfaceShader'
    DEFAULT_COLOR = [1, 1, 1]
    DEFAULT_TRANSPARENCY = [1, 1, 1]

    def __init__(self, name):
        super().__init__(name)

    @classmethod
    def create(cls, name=None, **kwargs):
        color = kwargs.pop('color', cls.DEFAULT_COLOR)
        transparency = kwargs.pop('transparency', cls.DEFAULT_TRANSPARENCY)
        shading_grp = kwargs.pop('shading_grp', 'initialShadingGroup')
        if kwargs:
            raise RuntimeError(f'Not supported kwarg:{kwargs}')
        if name is None:
            name = 'surfaceShader'
        node = mc.createNode(cls._CREATE_STR, name=name)
        mc.setAttr(f'{node}.outColor', *color, type='double3')
        mc.setAttr(f'{node}.outTransparency', *transparency, type='double3')
        if shading_grp != 'initialShadingGroup':
            try:
                shading_grp = mc.sets(name=shading_grp,
                                      renderable=True,
                                      noSurfaceShader=True,
                                      empty=True)
            except Exception as e:
                raise RuntimeError(f'Failed to create set:{shading_grp}\n{e}')

        mc.connectAttr(f'{node}.outColor', f'{shading_grp}.surfaceShader')
        return cls(node)

    @property
    def shading_grp(self):
        return mc.listConnections(f'{self.name}.outColor', source=True, destination=True)[0] or 'initialShadingGroup'

    def apply_to(self, objs):
        # obj.f[0] or obj
        mc.sets(objs, edit=True, forceElement=self.shading_grp)
