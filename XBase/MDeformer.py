import maya.cmds

import MNodes


class MSkinCluster(object):
    __slots__ = ['message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState', 'binMembership', 'input',
                 'weightFunction', 'outputGeometry', 'originalGeometry', 'envelopeWeightsList', 'blockGPU', 'envelope',
                 'function', 'fchild1', 'fchild2', 'fchild3', 'map64BitIndices', 'skinningMethod', 'blendWeights',
                 'weightList', 'perInfluenceWeights', 'bindPreMatrix', 'geomMatrix', 'matrix', 'dropoffRate', 'dropoff',
                 'smoothness', 'lockWeights', 'maintainMaxInfluences', 'maxInfluences', 'relativeSpaceMode',
                 'relativeSpaceMatrix', 'bindMethod', 'driverPoints', 'basePoints', 'baseDirty', 'paintWeights',
                 'paintTrans', 'paintArrDirty', 'useComponents', 'nurbsSamples', 'useComponentsMatrix',
                 'normalizeWeights', 'weightDistribution', 'deformUserNormals', 'wtDrty', 'bindPose', 'bindVolume',
                 'heatmapFalloff', 'influenceColor', 'geomBind', 'dqsSupportNonRigid', 'dqsScale', 'dqsScaleX',
                 'dqsScaleY', 'dqsScaleZ', 'cacheSetup']

    def __init__(self):
        pass

    def save_weight(self):
        pass

    def load_weight(self, weight_file):
        pass


class MBlendshape(object):
    __slots__ = ['message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState', 'binMembership', 'input',
                 'weightFunction', 'outputGeometry', 'originalGeometry', 'envelopeWeightsList', 'blockGPU', 'envelope',
                 'function', 'fchild1', 'fchild2', 'fchild3', 'map64BitIndices', 'topologyCheck', 'weight', 'icon',
                 'inputTarget', 'origin', 'baseOrigin', 'baseOriginX', 'baseOriginY', 'baseOriginZ', 'targetOrigin',
                 'targetOriginX', 'targetOriginY', 'targetOriginZ', 'parallelBlender', 'useTargetCompWeights',
                 'supportNegativeWeights', 'paintWeights', 'offsetDeformer', 'offsetX', 'offsetY', 'offsetZ',
                 'localVertexFrame', 'midLayerId', 'midLayerParent', 'nextNode', 'parentDirectory', 'nextTarget',
                 'targetVisibility', 'targetParentVisibility', 'targetDirectory', 'deformationOrder',
                 'inbetweenInfoGroup', 'symmetryEdge']

    def __init__(self):
        pass
