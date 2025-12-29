from __future__ import annotations
from contextlib import contextmanager
import math

import maya.cmds as mc
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma


@contextmanager
def undo_stack():
    mc.undoInfo(openChunk=True)
    print('Open undo chunk')
    yield
    mc.undoInfo(closeChunk=True)
    print('Close undo chunk')


@contextmanager
def switch_space_root(space_root):
    from XBase.MConstant import GlobalConfig
    GlobalConfig.set_root(space_root)
    print(f'Space root switched to {space_root}')
    yield
    GlobalConfig.reset_root()
    print(f'Space root reset')


def check_exist(node_name):
    if not mc.objExists(node_name):
        raise RuntimeError(f'{node_name} do not exist')


def check_type(node_name, obj_type):
    in_type = mc.objectType(node_name)
    if not in_type == obj_type:
        print(in_type == obj_type)
        raise RuntimeError(f'{node_name}({in_type}) is not {obj_type}')


def get_list_types(lst: list):
    if not lst:
        raise RuntimeError(f'List:{lst} is empty!')
    list_types = []
    for i in lst:
        obj_type = type(i)
        if obj_type not in list_types:
            list_types.append(obj_type)

    return list_types[0] if len(list_types) == 1 else list_types


def check_list_exist(lst):
    exist = True
    for i in lst:
        if not mc.objExists(str(i)):
            exist = False
            break
    return exist


def get_child(node):
    children = mc.listRelatives(node, children=True, allDescendents=True)
    if len(children) != 1:
        raise RuntimeError(f'{node} has more than one child or has not child,use get_children instead!')
    return children[0]


def get_children(node):
    children = mc.listRelatives(node, children=True, allDescendents=True)
    return children


def clamp_list(lst, accuracy=0.0001):
    lst_type = get_list_types(lst)
    if not lst_type not in [float, int]:
        raise RuntimeError(f'Not support list type:{lst_type},{lst}')
    new_lst = []
    for i in lst:
        new_lst.append(round(i))
    return new_lst


def revert_axis(axis):
    return [-1 * i for i in axis]


def disconnect_constraint(constraint_node):
    connected_attr = mc.listConnections(constraint_node, plugs=True)
    print(connected_attr)
    if not connected_attr:
        return
    for attr in connected_attr:
        try:
            mc.disconnectAttr(attr)
        except:
            pass


def get_joint_pos_array(joints):
    pass


def get_third_axis(axis1, axis2):
    from XBase.MConstant import Axis
    all_axis = [Axis.X, Axis.Y, Axis.Z]
    all_axis.remove(axis1)
    all_axis.remove(axis2)
    return all_axis[0]


def MVector2MatFormat(vec):
    lst = list(vec)
    lst.append(0)
    return lst


def List2MVector(lst):
    from maya.api.OpenMaya import MVector
    return MVector(lst[0], lst[1], lst[2])


def cross_product(v1, v2):
    print(v1, v2)
    x = v1[1] * v2[2] - v1[2] * v2[1]
    y = v1[2] * v2[0] - v1[0] * v2[2]
    z = v1[0] * v2[1] - v1[1] * v2[0]
    return [round(i, 5) for i in [x, y, z]]


def dot_product(v1, v2):
    return round(sum(a * b for a, b in zip(v1, v2)), 5)


def normalize_vector(vector):
    norm = math.sqrt(sum(x ** 2 for x in vector))

    return [round(i, 5) for i in [x / norm for x in vector]]


def linear_space(start, end, num):
    if num < 2:
        raise RuntimeError(f'Number can not less than 2')
    portion = (end - start) / num
    lst = []
    current_num = start
    while True:
        lst.append(current_num)
        current_num += portion
        if current_num >= end:
            lst.append(end)
            break
    return lst


def increase_save():
    file = mc.file(absoluteName=True)
    print(file)


def transfer_influences():
    sel = mc.ls(selection=True)
    if not sel:
        raise RuntimeError(f'Select source mesh and target mesh to transfer influences')
    source_mesh = sel[0]
    target_meshes = sel[1:]
    infs_source = get_mesh_infs(source_mesh)
    for target in target_meshes:
        target_skin_cluster = get_skin_cluster(target)
        target_infs = get_mesh_infs(target)
        for inf in infs_source:
            if inf in target_infs:
                continue
            mc.skinCluster(target_skin_cluster, addInfluence=inf, weight=0.0, lockWeights=True, e=True)
            print(f'Adding influence:{inf} to {target_skin_cluster}')


def get_mesh_infs(mesh):
    skin_cluster = [i for i in mc.listHistory(mesh) if mc.objectType(i) == 'skinCluster'][0] or None
    if skin_cluster is None:
        raise RuntimeError(f'Source mesh:{mesh} has not skin cluster node')
    infs = [i for i in mc.listHistory(skin_cluster) if mc.objectType(i) == 'joint']
    if not infs:
        raise RuntimeError(f'Skin cluster :{skin_cluster} has not infs')
    return infs


def get_skin_cluster(mesh):
    return [i for i in mc.listHistory(mesh) if mc.objectType(i) == 'skinCluster'][0] or None


def compress_list(lst, limit=2):
    compressed_lst = []
    zero_counter = 0
    for i, num in enumerate(lst):
        if num == 0:
            zero_counter += 1
        else:
            if zero_counter != 0:
                if zero_counter < limit:
                    for _ in range(zero_counter):
                        compressed_lst.append(0.0)
                else:
                    compressed_lst.append([zero_counter])
            compressed_lst.append(num)
            zero_counter = 0
        if i == len(lst) - 1 and zero_counter > 0:
            compressed_lst.append([zero_counter])
    return compressed_lst


def decompress_lst(lst):
    decompressed_lst = []
    for comp in lst:
        if isinstance(comp, list):
            for i in range(comp[0]):
                decompressed_lst.append(0.0)
        else:
            decompressed_lst.append(comp)
    return decompressed_lst


class StrUtils(object):

    def __init__(self, string: str):
        self.string = string

    def make_nice_string(self):
        splited = self.string.split('_')
        chars = [char.capitalize() for char in splited]
        new_string = ' '.join(chars)
        return new_string


def arg_match_attr(arg, attr_name):
    from XBase.MConstant import AttrType
    attr_type = mc.getAttr(attr_name, type=True)
    if attr_type in AttrType.ValueType:
        if not isinstance(arg, int) or isinstance(arg, float):
            return False
        else:
            return True
    elif attr_type in AttrType.CompoundType:
        if isinstance(arg, list) or isinstance(arg, tuple):
            if len(arg) == 3:
                return True
            else:
                return False
        elif isinstance(arg, int) or isinstance(arg, float):
            return True
        else:
            return False
    else:
        return False


def timer():
    import time
    start_time = time.time()


class OMUtils(object):

    @staticmethod
    def get_dependency_node(node_name):
        sel_list: om.MSelectionList = om.MGlobal.getSelectionListByName(node_name)
        dp = sel_list.getDependNode(0)
        return dp

    @staticmethod
    def get_dag_path(node_name):
        sel_list: om.MSelectionList = om.MGlobal.getSelectionListByName(node_name)
        dag = sel_list.getDagPath(0)
        return dag

    @staticmethod
    def get_mesh_component(mesh, idx=None):
        mesh_fn = om.MFnMesh(OMUtils.get_dependency_node(mesh))
        single_comp = om.MFnSingleIndexedComponent()
        mo = single_comp.create(om.MFn.kMeshVertComponent)
        if idx is None:
            single_comp.addElements([i for i in range(mesh_fn.numVertices)])
        elif isinstance(idx, list) or isinstance(idx, tuple):
            single_comp.addElements(idx)
        elif isinstance(idx, int):
            single_comp.addElement(idx)
        else:
            raise RuntimeError(f'Wrong index :{idx}')

        return mo

    @staticmethod
    def get_nurbs_component(nurbs_name, cv=None):
        comp_fn = om.MFnDoubleIndexedComponent()
        comp = comp_fn.create(om.MFn.kSurfaceCVComponent)
        nurbs_fn = om.MFnNurbsSurface(OMUtils.get_dependency_node(nurbs_name))
        if cv is None:
            cv = [[i, j] for i in range(nurbs_fn.numCVsInU) for j in range(nurbs_fn.numCVsInV)]
        comp_fn.addElements(cv)
        return comp


if __name__ == '__main__':
    res = linear_space(0, 1, 5)
    print(res)
