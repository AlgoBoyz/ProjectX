import os

from XBase import MTransform as mt
from XTools.XFileTool import JsonFile
from XBase.MConstant import PROJECT_BASE_DIR


class MController(object):

    def __init__(self, name):
        self.name = name

    @classmethod
    def create(cls, name, prototype_name):
        ctrl_shape_data_dir = os.path.join(PROJECT_BASE_DIR, 'res', 'ControllerShapeData', prototype_name, '.json')
        shape_data = JsonFile(ctrl_shape_data_dir).load()
