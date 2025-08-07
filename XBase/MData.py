import os
from idlelib.outwin import file_line_pats

import maya.cmds as mc
import maya.api.OpenMaya as om

import maya.api.OpenMayaAnim as oman
from maya.api.OpenMayaAnim import MFnSkinCluster
from maya.app.renderSetup.model.typeIDs import override

from XBase.MConstant import PROJECT_BASE_DIR, Axis
from XBase.MBaseFunctions import check_type,check_exist,OMUtils
from XTools.XFileTool import JsonFile


class MCurveData(object):
    DATA_DIR = os.path.join(PROJECT_BASE_DIR, 'res', 'GeoData', 'NurbsCurve')

    def __init__(self, data:dict):
        self.data = data
        self.name = ''
        self.pos_array = []
        self.pos_vec_array = []
        self.knots = []
        self.periodic = True
        self.degree = -1
        self.normal_vec = Axis.X

        self.attrs = ['name', 'pos_array', 'knots', 'periodic', 'degree']
        self.update_data(data)
    def __repr__(self):
        repr_str = 'Curve data:\n'
        for key, val in self.data.items():
            repr_str += f'    {key}:{val}\n'
        return repr_str

    def update_data(self,data=None):
        data = data if not data is None else self.data
        for attr in self.attrs:
            try:
                value = data.get(attr)
                setattr(self,attr,value)
            except Exception as e:
                print(e)

    @classmethod
    def load_from_node(cls,node_name,prototype_name=''):
        check_exist(node_name)
        check_type(node_name,'nurbsCurve')
        data = {}
        curve_fn = om.MFnNurbsCurve(OMUtils.get_dependency_node(node_name))
        data['name'] = prototype_name
        data['pos_array'] = curve_fn.cvPositions()
        data['knots'] = curve_fn.knots()
        data['periodic'] = curve_fn.kPeriodic
        return cls(data)
    @classmethod
    def load_from_file(cls,file_name):
        file_path = os.path.join(cls.DATA_DIR,file_name+'.json')
        file_io = JsonFile(file_path)
        data = file_io.load()
        return cls(data)
    @property
    def serialized_data(self):
        data = self.data
        data['pos_array'] = [tuple(i) for i in self.data['pos_array']]
        data['knots'] = [int(i) for i in self.data['knots']]
        return data

    def save(self,file_name):
        file_path = os.path.join(self.DATA_DIR,file_name+'.json')
        file_io = JsonFile.create(file_path,override=True)
        file_io.dump(self.serialized_data)

class MeshData(object):

    def __init__(self):
        pass


class MWeightData(object):
    DATA_DIR = os.path.join(PROJECT_BASE_DIR, 'res', 'GeoData', 'Weight')

    def __init__(self, data):
        self.joint_array = data[0]
        self.weight_array = data[1]
        self.weight_mapper = data[2]
        self.node_attrs_values = data[3]


class MBlendShapeData(object):

    def __init__(self):
        pass

MCurveData({'name':'test'})