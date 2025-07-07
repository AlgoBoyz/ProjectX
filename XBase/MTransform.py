from typing import Iterator, Union

from maya.OpenMaya import MVector

import maya.api.OpenMaya as om
import maya.cmds as mc

from . import MBaseFunctions as mb
from . import MNodes
from .MConstant import XSpace, WorldUpType, Axis, Matrix


class MTransform(MNodes.MNode):
    _CREATE_STR = 'transform'
    root_space = XSpace.transform_root

    def __init__(self, name):
        super().__init__(name)
        self.top_group = None

    @classmethod
    def set_root_space(cls, root):
        cls.root_space = root

    @classmethod
    def create(cls, name=None, **kwargs) -> 'MTransform':
        if cls.root_space:
            instance = super().create(name, under=cls.root_space, **kwargs)
        else:
            instance = super().create(name, **kwargs)
        return instance

    @property
    def children(self):
        children = mc.listRelatives(self.name, children=True, allDescendents=True)
        if not children:
            return None
        else:
            return [MTransform(node) for node in children]

    @property
    def child(self):
        if self.children and len(self.children) == 1:
            return self.children[0]
        else:
            raise RuntimeError(
                f'Can not use child attribute while a node has more than one child,please use children instead.')

    @property
    def world_pos(self):
        pos = mc.xform(self.name, worldSpace=True, translation=True, q=True)
        return om.MVector(pos)

    @property
    def local_pos(self):
        pos = mc.xform(self.name, worldSpace=False, translation=True, q=True)
        return om.MVector(pos)

    @property
    def parent(self):
        p = mc.listRelatives(self.name, parent=True)
        if p is None:
            return None
        elif isinstance(p, list) and len(p) == 1:
            return MTransform(p[0])
        else:
            raise RuntimeError(f'Failed to retrive parent of {self.name}\nresult:{p}')

    def set_parent(self, parent):
        if parent is None or parent == 'None':
            if self.parent is None:
                return True
            else:
                mc.parent(self.name, world=True)
                return True
        elif mc.objExists(str(parent)):
            mc.parent(self.name, str(parent))
            return True
        else:
            raise RuntimeError(f'Parent object do not exist :{parent}')

    def set_aim_constraint(self, other: str,
                           aim_vec, up_vec,
                           up_type, up_obj):
        constraint_node = None
        if up_type == WorldUpType.Vector.value:
            constraint_node = mc.aimConstraint(other, self.name, aimVector=aim_vec, upVector=up_vec,
                                               worldUpType=up_type,
                                               worldUpVector=up_obj)

        elif up_type == WorldUpType.Object.value:
            constraint_node = mc.aimConstraint(other, self.name, aimVector=aim_vec, upVector=up_vec,
                                               worldUpType=up_type,
                                               worldUpObject=up_obj)
        return constraint_node

    def insert_parent(self, name):
        pass

    def unparent(self):
        pass

    def freeze(self, translate=True, rotate=True, scale=True):
        mc.makeIdentity(self.name, apply=True, translate=translate, rotate=rotate, scale=scale)

    def match(self, other, **kwargs):
        if isinstance(other, str):
            other = MTransform(other)
        mc.matchTransform(self.name, other.name, **kwargs)

    def match_pos(self, pos, world=True):
        if isinstance(pos, om.MVector):
            pos = [i for i in pos]
        mc.xform(self.name, worldSpace=world, translation=pos)

    def match_rotatation(self, rot, world=True):
        mc.xform(self.name, worldSpace=world, rotation=rot, e=True)

    def move_by(self, vec, world=True):
        if isinstance(vec, list) and len(vec) == 3:
            vec = om.MVector(*vec)
        else:
            raise RuntimeError(f'Wrong vector format:{vec}')
        pos_after = self.world_pos + vec if world else self.local_pos + vec
        self.match_pos(pos_after)

    def set_visibility(self, visibility: bool):
        pass

    def get_vector_to(self, other):
        if isinstance(other, str):
            other = MTransform(other)
        vec = om.MVector(other.world_pos) - om.MVector(self.world_pos)
        return vec

    def get_world_matrix(self):
        mat = self.worldMatrix.value
        mat = [mat[i:i + 4] for i in range(0, 16, 4)]
        return mat

    def reorient(self, aim_axis, aim_vec, up_axis, up_vec):
        print(f'Reorienting node:{self.name}')
        axis_index_look_up = {Axis.X.name: 0, Axis.Y.name: 1, Axis.Z.name: 2}

        lst = [i for i in axis_index_look_up.values()]

        mat = self.get_world_matrix()
        aim_index = axis_index_look_up[aim_axis]
        lst.remove(aim_index)
        up_index = axis_index_look_up[up_axis]
        lst.remove(up_index)
        third_index = lst[0]
        third_vec = mb.normalize_vector(mb.cross_product(aim_vec, up_vec))
        aim_vec.append(0.0)
        up_vec.append(0.0)
        third_vec.append(0.0)
        mat[aim_index] = aim_vec[:4]
        mat[up_index] = up_vec[:4]
        mat[third_index] = third_vec[:4]
        # print('aim2', aim_vec)
        # print('up2', up_vec)
        # print('third', third_vec)
        reformat_mat = []
        for lst in mat:
            for i in lst:
                reformat_mat.append(i)
        # print(f'Matrix previous :{reformat_mat}')
        mc.xform(self.name, matrix=reformat_mat)
        # print(f'Matrix after :{self.worldMatrix.value}')


class MLocator(MTransform):
    _CREATE_STR = 'locator'
    root_space = XSpace.locator_root

    def __init__(self, name):
        super().__init__(name)
        self.shape = ''


class MJoint(MTransform):
    _CREATE_STR = 'joint'
    root_space = XSpace.joint_root

    @classmethod
    def create(cls, name=None, **kwargs) -> 'MJoint':
        instance = super().create(name, **kwargs)

        return cls(instance.name)

    @property
    def joint_data(self):
        data = {
            'name': self.name,
            'pos': tuple(self.world_pos)[:3],
            'rot': self.rotate.value,
            'scale': self.scale.value,
            'orient': self.rotateOrder.value,
            'parent': str(self.parent)

        }
        return data

    @classmethod
    def recreate_from_data(cls, data):
        jnt_name = data['name']
        if mc.objExists(jnt_name):
            raise RuntimeError(f'Joint: {jnt_name} already exist!')
        jnt = cls.create(jnt_name)
        jnt.set_parent(data['parent'])
        jnt.rotateOrder.set(data['orient'])
        jnt.translate.set(data['pos'])
        jnt.rotate.set(data['rot'])
        jnt.scale.set(data['scale'])
        return jnt


class MTransformList(object):
    MEMBER_TYPE = MTransform

    def __init__(self, mt_names):
        self.node_names = mt_names
        self.nodes = []
        self.positions = []
        self._init_node_list()
        self.len = len(self.node_names)

    def __getitem__(self, idx) -> MTransform:
        return self.nodes[idx]

    def __iter__(self) -> Iterator[MTransform]:
        return iter(self.nodes)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.len}):{self.node_names}'

    def _init_node_list(self):
        lst_types = mb.get_list_types(self.node_names)
        if isinstance(lst_types, list) and len(lst_types) > 1:
            raise ValueError(f'Input joint list:{self.nodes} has more than one type:{lst_types}')
        if lst_types == str:
            self.nodes = [self.MEMBER_TYPE(name) for name in self.node_names]
        elif lst_types == self.MEMBER_TYPE:
            self.nodes = self.node_names
            self.node_names = [jnt.name for jnt in self.node_names]

    @classmethod
    def create(cls, names: list):
        exist = mb.check_list_exist(names)
        nodes_created = []
        if not exist:
            for name in names:
                node = cls.MEMBER_TYPE.create(name=name)
                nodes_created.append(node)
            return cls(nodes_created)
        else:
            return cls(names)

    def unparent_all(self, tmp_group=None):

        for node in self.nodes:
            node.set_parent(tmp_group)

    def parent_all(self, reverse=False):
        self.unparent_all()
        to_reparent = self.nodes
        if reverse:
            to_reparent = self.nodes[::-1]
        for i, node in enumerate(to_reparent):
            if i < 1:
                continue
            node.set_parent(to_reparent[i - 1])


class MJointSet(MTransformList):
    MEMBER_TYPE = MJoint

    def __init__(self, joints: list):
        super().__init__(joints)

    @classmethod
    def create(cls, joints: list[str]) -> 'MJointSet':
        instance = super().create(joints)
        return cls(instance.node_names)

    def __getitem__(self, idx) -> Union[MJoint, 'MJointSet']:
        if isinstance(idx, slice):
            return MJointSet(self.nodes[idx])
        else:
            return MJoint(self.nodes[idx])

    def __iter__(self) -> Iterator[MJoint]:
        return iter(self.nodes)


class MJointChain(MJointSet):

    def __init__(self, joints: list):
        super().__init__(joints)

    def __getitem__(self, idx) -> Union[MJoint, 'MJointChain']:
        if isinstance(idx, slice):
            return MJointChain(self.nodes[idx])
        else:
            return MJoint(self.nodes[idx])

    @classmethod
    def create(cls, joints: list[str]) -> 'MJointChain':
        instance = super().create(joints)
        instance.parent_all()
        return cls(instance.node_names)

    @property
    def plane_normal(self):
        from XBase.MBaseFunctions import calculate_plane_normal
        vec1 = self[1].world_pos - self[0].world_pos
        vec2 = self[2].world_pos - self[1].world_pos
        normal = calculate_plane_normal(vec1, vec2)
        return normal

    def update_chain(self):
        self.unparent_all()
        self.parent_all()

    def convert_to_curve(self):
        pass

    def duplicate(self):
        pass

    def reorient(self, aim_aixs, up_axis, up_obj):
        previous_parent = self[0].parent
        self.unparent_all()
        for i, jnt in enumerate(self):
            if not i == self.length - 1:
                print(i, self.length)
                constraint_node = jnt.set_aim_constraint(
                    other=self.node_names[i + 1],
                    aim_vec=aim_aixs,
                    up_vec=up_axis,
                    up_type=WorldUpType.Object.value,
                    up_obj=up_obj
                )
            else:
                constraint_node = jnt.set_aim_constraint(
                    other=self.node_names[i - 1],
                    aim_vec=mb.revert_axis(aim_aixs),
                    up_vec=up_axis,
                    up_type=WorldUpType.Object.value,
                    up_obj=up_obj
                )
            mc.refresh()
            mc.delete(constraint_node)
            jnt.freeze()
        self.parent_all()
        self[0].set_parent(previous_parent)

    def reorient_to_plane_normal(self, aim_axis, up_axis):
        pre_parent = self[0].parent
        self.unparent_all()
        aim_vecs = []
        for i, jnt in enumerate(self):
            matrix = jnt.worldMatrix.value
            vec_array = [matrix[i:i + 4] for i in range(0, 16, 4)]
            if i != self.length - 1:
                jnt_aim_vec = [round(i, 10) for i in tuple((self[i + 1].world_pos - jnt.world_pos).normal())]
            else:
                jnt_aim_vec = aim_vecs[i - 1]

            aim_vecs.append(jnt_aim_vec)
            print(self.plane_normal, 'plane normal')
            print(jnt_aim_vec, 'aim')
            jnt.reorient(aim_axis=aim_axis,
                         aim_vec=mb.normalize_vector(jnt_aim_vec),
                         up_axis=up_axis,
                         up_vec=mb.normalize_vector(self.plane_normal))
            jnt.freeze()
        self.parent_all()
        self[0].set_parent(pre_parent)

    def reverse_chain(self):
        self.unparent_all()
        self.parent_all(reverse=True)

    def freeze(self):
        for jnt in self:
            jnt.freeze()


class MTripleJointChain(MJointChain):

    def __init__(self, joints):
        super().__init__(joints)

    def __getitem__(self, idx) -> Union[MJoint, 'MTripleJointChain']:
        if isinstance(idx, slice):
            return MTripleJointChain(self.nodes[idx])
        else:
            return MJoint(self.nodes[idx])

    @classmethod
    def create(cls, joints: list[str]) -> 'MTripleJointChain':
        if not len(joints) == 3:
            raise RuntimeError(f'Can not initialize MTripleJointChain from {joints} due to length of joints is not 3')
        instance = super().create(joints)
        return cls(joints)

    @property
    def vec_ab(self):
        vec_ab = self[1].world_pos - self[0].world_pos
        return vec_ab

    @property
    def vec_ac(self):
        vec_ac = self[2].world_pos - self[0].world_pos
        return vec_ac

    @property
    def vec_bc(self):
        vec_bc = self[2].world_pos - self[1].world_pos
        return vec_bc

    @property
    def pv_vec(self):
        '''
        a*b = |a|*|b|*cos
        --> a*b/|b| = |a|*cos
        --> 点乘结果除以b的模长等于a在b上的投影长度，再除以b的模长，等于投影在b上占的比例
        :return:
        '''

        factor = (self.vec_ab * self.vec_ac) / self.vec_ac.length() ** 2
        vec_db = self.vec_ab - self.vec_ac * factor

        return vec_db

    @property
    def normal(self):
        pass

    def get_pole_vec_pos(self, multiplier=2):
        pv_pos = self[1].world_pos + self.pv_vec * multiplier
        return pv_pos


class MQuadJointChain(MJointChain):

    def __init__(self, joints):
        super().__init__(joints)

    def __getitem__(self, idx) -> Union[MJoint, 'MQuadJointChain']:
        if isinstance(idx, slice):
            return MQuadJointChain(self.nodes[idx])
        else:
            return MJoint(self.nodes[idx])
