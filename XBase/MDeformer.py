from maya.cmds import weightsColor

from maya.api.OpenMayaAnim import MFnSkinCluster

import maya.cmds as mc
import maya.api.OpenMaya as om
from XBase.MNodes import MNode
from XBase.MGeometry import MMesh
from XBase.MData import MWeightData
from XBase.MBaseFunctions import compress_list,decompress_lst,OMUtils
class MSkinCluster(MNode):
    _CREATE_STR = 'skinCluster'

    def __init__(self, shape_name, skin_name):
        super().__init__(skin_name)
        self.skin_fn = MFnSkinCluster(self.dp_node)
        self.skin_cluster_node_data = {}
        self.shape_name = shape_name
        print(self.shape_name)
        self.shape_mn = MMesh(self.shape_name)
        # to collect: name,node_attrs,skin influences,skin weight,deformer weight

    @classmethod
    def create(cls, name=None, **kwargs):
        shape = kwargs.pop('shape', None)
        if shape is None:
            raise RuntimeError(f'Must be created with a shape node')
        skin_cluster = mc.skinCluster()
        return MSkinCluster(skin_cluster)

    @classmethod
    def rebuild_from_data(cls, data):
        pass

    @property
    def influences(self):
        infs = [i for i in mc.listHistory(self.name) if mc.objectType(i) == 'joint']
        return infs

    @property
    def influences_dag(self):
        infs = [om.MGlobal.getSelectionListByName(i).getDagPath(0) for i in self.influences]
        return infs

    @property
    def influence_logical_indices(self):
        indices = [self.skin_fn.indexForInfluenceObject(i) for i in self.influences_dag]
        return indices

    def get_weight_array(self, pnt_indices=None, inf_indices=None):
        shape_dag = self.shape_mn.dag_path
        component_fn = om.MFnSingleIndexedComponent()
        component = component_fn.create(om.MFn.kMeshVertComponent)
        if pnt_indices is None:
            component_fn.addElements([i for i in range(self.shape_mn.vert_num)])
        elif isinstance(pnt_indices, int):
            component_fn.addElement(pnt_indices)
        elif isinstance(pnt_indices, list) or isinstance(pnt_indices, tuple):
            component_fn.addElements(pnt_indices)

        if inf_indices is None:
            inf_indices = om.MIntArray([i for i in range(len(self.influences))])
        elif isinstance(inf_indices, list) or isinstance(inf_indices, tuple):
            inf_indices = om.MIntArray(inf_indices)
        elif isinstance(inf_indices, int):
            inf_indices = inf_indices
        else:
            raise RuntimeError(f'Wrong influence input')

        weight = self.skin_fn.getWeights(shape_dag,component,inf_indices)
        return weight

    def set_weight(self,weight_array,inf_array):

        component = OMUtils.get_mesh_component(self.shape_mn.name)
        if isinstance(weight_array,list):
            weight_array=om.MDoubleArray(weight_array)
        if isinstance(inf_array,list):
            inf_array = om.MIntArray(inf_array)
        self.skin_fn.setWeights(self.shape_mn.dag_path,component,inf_array,weight_array)
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
