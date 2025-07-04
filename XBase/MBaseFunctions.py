import maya.cmds as mc


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


def calculate_plane_normal(vec1, vec2):
    from maya.api.OpenMaya import MVector
    vec1 = MVector(vec1)
    vec2 = MVector(vec2)
    normal = (vec1 ^ vec2).normal()

    return normal


class StrUtils(object):

    def __init__(self, string: str):
        self.string = string

    def make_nice_string(self):
        splited = self.string.split('_')
        chars = [char.capitalize() for char in splited]
        new_string = ' '.join(chars)
        return new_string


if __name__ == '__main__':
    pass
