import maya.cmds as mc
from XBase.MTransform import MTransform
from XBase.MDeformer import MSkinCluster


class WeightDataCollector(object):

    def __init__(self):
        self.shape_skin = []
        self.get_all_skined_mesh()
        print(self.shape_skin)

    def get_all_skined_mesh(self):
        meshes = mc.ls(type='mesh')
        for mesh in meshes:
            sc = [i for i in mc.listHistory(mesh) if mc.objectType(i) == 'skinCluster']
            if not sc:
                continue
            self.shape_skin.append([mesh, sc[0]])
        return self.shape_skin

    def rename_all_sc(self):
        for shape, sc in self.shape_skin:
            new_name = f'{shape}_SC'
            mc.rename(sc, new_name)
            print(f'Rename {sc} >> {new_name}')

    @staticmethod
    def gather_weight_data():
        pass
