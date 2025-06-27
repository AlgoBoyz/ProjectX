import maya.cmds as mc


def get_list_types(lst: list):
    if not lst:
        raise RuntimeError(f'List:{lst} is empty!')
    list_types = []
    for i in lst:
        obj_type = type(i)
        if obj_type not in list_types:
            list_types.append(obj_type)

    return list_types


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


def clamp_list(lst,accuracy=0.0001):
    lst_type = get_list_types(lst)
    if not lst_type not in [float,int]:
        raise RuntimeError(f'Not support list type:{lst_type},{lst}')
    new_lst = []
    for i in lst:
        new_lst.append(i) if abs(i) > accuracy else new_lst.append(0)
    return new_lst

class StrUtils(object):

    def __init__(self, string: str):
        self.string = string

    def make_nice_string(self):
        splited = self.string.split('_')
        chars = [char.capitalize() for char in splited]
        new_string = ' '.join(chars)
        return new_string

