import os

import maya.cmds as mc
import maya.api.OpenMaya as om

from XBase.MBaseFunctions import check_exist, OMUtils, get_children
from XBase.MConstant import PROJECT_BASE_DIR
from XTools.XFileTool import JsonFile


class CurveDataCollection(object):
    def __init__(self, data: list):
        self.data_collection = data
        self._validate()

    def _validate(self):
        for data in self.data_collection:
            if not isinstance(data, CurveShapeData):
                raise TypeError("Data must be CurveShapeData")

    def __repr__(self):
        repr_str = ''
        for data in self.data_collection:
            repr_str += f'\n{data}\n'
        return repr_str

    def __getitem__(self, idx) -> 'CurveShapeData':
        if not isinstance(idx, int):
            raise TypeError("Key must be an integer")
        if idx < 0 or idx >= len(self.data_collection):
            raise IndexError("Index out of range")

        return self.data_collection[idx]

    def save_to_disk(self, file_name: str, work_dir: str = '') -> None:
        manager = NurbsCurveShapeDataManger(work_dir) if work_dir else NurbsCurveShapeDataManger()
        manager.save_to_disk(file_name, self)

    @classmethod
    def from_disk(cls, file_name: str, work_dir: str = '') -> 'CurveDataCollection':
        manager = NurbsCurveShapeDataManger(work_dir) if work_dir else NurbsCurveShapeDataManger()
        collection = manager.load_from_disk(file_name)
        return collection

    @classmethod
    def from_maya(cls, node_name):
        return NurbsCurveShapeDataManger.get_from_maya(node_name)


class CurveShapeData(object):

    def __init__(self, data: dict):
        self.data = data
        self._validate()

    def _validate(self):
        required_keys = ['pos_array', 'knots', 'degree', 'periodic']
        for key in required_keys:
            if key not in self.data.keys():
                raise KeyError(f"Required key {key} is missing")

    def __repr__(self):
        repr_str = ''
        for key, val in self.data.items():
            repr_str += f'\n{key}: {val}\n'
        return repr_str

    @property
    def pos_array(self) -> list:
        return self.data['pos_array']

    @property
    def knots(self) -> list:
        return self.data['knots']

    @property
    def degree(self) -> int:
        return self.data['degree']

    @property
    def periodic(self) -> bool:
        return self.data['periodic']


class NurbsCurveShapeDataManger(object):
    DEFAULT_WORK_PATH = os.path.join(PROJECT_BASE_DIR, 'res', 'GeoData', 'NurbsCurve')

    def __init__(self, work_dir=None):
        if work_dir and not os.path.exists(work_dir):
            raise FileNotFoundError(f"Work dir {work_dir} does not exist")

        self.work_dir = work_dir or self.DEFAULT_WORK_PATH

    @classmethod
    def get_curve_shape_data(cls, node_name: str) -> 'CurveShapeData':
        data_dict = cls.get_raw_from_maya(node_name)
        instance = CurveShapeData(data_dict)
        return instance

    @classmethod
    def get_from_maya(cls, node_name: str) -> 'CurveDataCollection':
        if not mc.objectType(node_name) == 'transform':
            raise TypeError("Node name must be 'transform'")

        children = get_children(node_name)
        data = []
        if children is None:
            raise RuntimeError(f"{node_name} has no shapes")
        for child in children:
            child_data = cls.get_curve_shape_data(child)
            data.append(child_data)
        data_instance = CurveDataCollection(data)
        return data_instance

    @staticmethod
    def get_raw_from_maya(node_name) -> dict:
        check_exist(node_name)
        curve_fn = OMUtils.get_nurbsCurve_fn_from(node_name)
        pos_array = [list(i)[:-1] for i in curve_fn.cvPositions(om.MSpace.kObject)]
        knot = [i for i in curve_fn.knots()]
        degree = curve_fn.degree
        periodic = curve_fn.kPeriodic

        data = {'pos_array': pos_array,
                'knots': knot,
                'degree': degree,
                'periodic': periodic}

        return data

    def load_from_disk(self, file_name: str) -> 'CurveDataCollection':
        file_path = os.path.join(self.work_dir, file_name + '.json')
        if not os.path.exists(file_path):
            raise IOError(f"File {file_name} does not exist")

        data = JsonFile(file_path).load()
        data_lst = [CurveShapeData(i) for i in data]
        return CurveDataCollection(data_lst)

    def save_to_disk(self, file_name: str, data: CurveDataCollection):
        if not isinstance(data, CurveDataCollection):
            raise TypeError("Data must be CurveDataCollection")
        file_path = os.path.join(self.work_dir, file_name + '.json')
        file = JsonFile.create(file_path, override=True)
        file.dump([i.data for i in data])
