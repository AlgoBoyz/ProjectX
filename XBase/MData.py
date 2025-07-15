import os

import maya.cmds as mc
import maya.api.OpenMaya as om

import maya.api.OpenMayaAnim as oman
from maya.api.OpenMayaAnim import MFnSkinCluster

from .MBaseFunctions import clamp_list
from .MNodes import MNode
from .MConstant import PROJECT_BASE_DIR, Axis
from XTools.XFileTool import JsonFile


class MCurveData(object):
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
        for key, val in self.data.items():
            repr_str += f'{key}:{val}\n'
        return repr_str

    @classmethod
    def load_from_file(cls, file_path, shape_index=0):
        file_io = JsonFile(file_path)
        data = file_io.load()
        name = list(data.keys())[shape_index]
        instance = cls(name)
        instance.update_data(data[name])
        return instance

    @classmethod
    def load_from_node(cls, node_name):
        data = cls.collect_curve_data(node_name)[node_name]
        instance = MCurveData(node_name)
        instance.update_data(data)

    @staticmethod
    def collect_curve_data(shape_dag_name):
        curve_fn = om.MFnNurbsCurve(om.MGlobal.getSelectionListByName(shape_dag_name).getDagPath(0))
        pos_array = [clamp_list(tuple(i)[:3]) for i in curve_fn.cvPositions()]
        knots = tuple(curve_fn.knots())
        degree = curve_fn.degree
        periodic = curve_fn.kPeriodic
        data = {shape_dag_name: {
            'pos_array': pos_array,
            'knots': knots,
            'degree': degree,
            'periodic': periodic
        }}
        return data

    @staticmethod
    def save_curve_data(node_name, file_path='', override=True):
        data = MCurveData.collect_curve_data(node_name)
        if not file_path:
            file_path = os.path.join(MCurveData.DATA_DIR, f'{node_name}.json')
        file_io = JsonFile.create(file_path, override=override)
        file_io.dump(data)

    def apply_data(self, data: dict):
        pass

    @staticmethod
    def deserialize_data(data: dict):
        data['pos_array'] = [om.MVector(i) for i in data['pos_array']]
        data['knots'] = om.MDoubleArray(data['knots'])
        return data

    @staticmethod
    def serialize_data(data):
        data['pos_array'] = [tuple(i)[:3] for i in data['pos_array']]
        data['knots'] = tuple(data['knots'])
        return data

    def update_data(self, data):
        self.data = self.serialize_data(data)

        exclude = ['name', 'normal_vec']
        for item in self.attrs:
            if item in exclude:
                continue
            setattr(self, item, self.data[item])

    def check_validate(self):
        if self.pos_array is None or self.periodic is None or self.knots is None or self.degree == -1:
            raise ValueError(f'Invalid curve data,\n'
                             f'pos_array:{self.pos_array}\n'
                             f'periodic:{self.periodic}\n'
                             f'knots:{self.knots}\n'
                             f'degree:{self.degree}')


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
