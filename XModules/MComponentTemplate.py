import os.path

import maya.cmds as mc
from XBase.MConstant import PROJECT_BASE_DIR
from XBase.MTransform import MJoint
from XTools.XFileTool import JsonFile

TempLateDataDir = os.path.join(PROJECT_BASE_DIR, 'res', 'TemplateData')


class IKComponentData(object):

    def __init__(self, data):
        self.joints_data = data

    @classmethod
    def load_from_scene(cls):
        sel = mc.ls(selection=True)
        if not sel:
            raise RuntimeError('Please select at least one joint for data collection')
        data = [MJoint(i).joint_data for i in sel]
        return cls(data)

    @classmethod
    def load_from_file(cls, file):
        pass

    def save_data(self, file_name, override=True):
        # todo 需要一个脚手架GUI,用于测试模板数据的导入导出，编辑
        file_path = os.path.join(TempLateDataDir, f'{file_name}.json')
        file_io = JsonFile.create(file_path, override=override)
        file_io.dump(self.joints_data)


class IKComponentTemplate(object):

    def __init__(self, data: IKComponentData):
        self.template_data = data

    @classmethod
    def create(cls, data):
        pass
