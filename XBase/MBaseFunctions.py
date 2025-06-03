import maya.cmds as mc


def get_list_types(lst: list):
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


class StrUtils(object):

    def __init__(self, srting):
        self.srting = srting


lst1 = ['s', 'sss', 'sas']
lst2 = [1, 2, 3, 45, 6, 's']
lst3 = [1, 2, 3, 4, 6]
