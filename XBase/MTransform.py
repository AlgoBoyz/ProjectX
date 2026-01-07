from typing import Iterator, Union

import maya.api.OpenMaya as om
import maya.cmds as mc

from XBase.MBaseFunctions import OMUtils, linear_space
from XBase.MNodes import MNode
from XBase.MShape import MLocatorShape
from XBase.MConstant import GlobalConfig, WorldUpType, Axis, ParentType


class MTransform(MNode):
    _CREATE_STR = 'transform'

    def __init__(self, name):
        super().__init__(name)
        self.top_group = None

    @classmethod
    def create(cls, name=None, **kwargs) -> 'MTransform':
        node = super().create(name).name

        under = kwargs.pop('under', None)
        match = kwargs.pop('match', None)
        pos = kwargs.pop('position', kwargs.pop('pos', None))
        if kwargs:
            raise ValueError(f'Parameter:{kwargs} is not supported!')

        if under:
            if isinstance(under, str):
                mc.parent(node, under)
            elif isinstance(under, cls):
                mc.parent(node, under.name)
        if match:
            mc.matchTransform(node, match)
        if pos:
            mc.xform(node, worldSpace=True, translation=pos)
        if GlobalConfig.transform_root and not under:
            mc.parent(node, GlobalConfig.transform_root)
        return cls(node)

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
        pos = mc.xform(self.name, worldSpace=False, translation=True, q=True)  # pos:list[3]
        return om.MVector(pos)

    @property
    def parent(self):
        p = mc.listRelatives(self.name, parent=True)
        if p is None:
            return None
        elif isinstance(p, list) and len(p) == 1:
            return MTransform(p[0])
        else:
            raise RuntimeError(f'Failed to retrieve parent of {self.name}\nresult:{p}')

    def create_loc(self, parent_type=ParentType.parent_constraint):

        loc_name = f'{self.name}_Loc'
        if not mc.objExists(loc_name):
            loc = MLocator.create(loc_name)
        else:
            loc = MLocator(loc_name, f'{loc_name}Shape')

        loc.match(self)

        if parent_type == ParentType.hierarchy:
            loc.set_parent(self)
        elif parent_type == ParentType.point_constraint:
            mc.pointConstraint(self.name, loc.name)
        elif parent_type == ParentType.parent_constraint:
            mc.parentConstraint(self.name, loc.name)
        return loc

    def set_parent(self, parent):

        if parent is None or parent == 'None':
            if self.parent is None:
                return True
            else:
                mc.parent(self.name, world=True)
                return True

        elif mc.objExists(str(parent)):
            if str(parent) == str(self.parent):
                print(f'{self.name} already a child of {parent}')
                pass
            else:
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
        pre_parent = self.parent
        instance = MTransform.create(name=name, match=self)
        self.set_parent(None)
        self.set_parent(instance)
        if pre_parent is not None:
            instance.set_parent(pre_parent)
        return instance

    def unparent(self):
        pass

    def lock_attrs(self, *attr_prefix, vis=True, hide=True):
        """
        attr_prefix:t,r,x
        """
        for axis in ['x', 'y', 'z']:
            for prefix in attr_prefix:
                if hide:
                    mc.setAttr(f'{self}.{prefix}{axis}', lock=True, keyable=False)
                    if vis:
                        mc.setAttr(f'{self}.v', lock=True, keyable=False)
                else:
                    mc.setAttr(f'{self}.{prefix}{axis}', lock=True)
                    if vis:
                        mc.setAttr(f'{self}.v', lock=True)

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

    def match_rotation(self, rot, world=True):
        mc.xform(self.name, worldSpace=world, rotation=rot, e=True)

    def move_by(self, vec, world=True):
        if isinstance(vec, list) and len(vec) == 3:
            vec = om.MVector(*vec)
        elif isinstance(vec, om.MVector):
            pass
        else:
            raise RuntimeError(f'Wrong vector format:{vec}')
        pos_after = self.world_pos + vec if world else self.local_pos + vec
        self.match_pos(pos_after)

    def mirror(self, plane='yz'):
        pre_pos = [i for i in self.world_pos]

        if plane == 'yz':
            pos = [pre_pos[0] * -1, pre_pos[1], pre_pos[2]]

    def set_visibility(self, visibility: bool):
        mc.setAttr(f'{self.name}.v', visibility)

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
        # todo:计算精度有问题，导致最后缩放会出现误差gb
        from XBase.MBaseFunctions import normalize_vector, cross_product
        axis_index_look_up = {Axis.X.name: 0, Axis.Y.name: 1, Axis.Z.name: 2}
        lst = [i for i in axis_index_look_up.values()]
        mat = self.get_world_matrix()
        aim_index = axis_index_look_up[aim_axis]
        up_index = axis_index_look_up[up_axis]

        lst.remove(aim_index)
        lst.remove(up_index)
        third_index = lst[0]

        third_vec = normalize_vector(cross_product(aim_vec, up_vec))
        aim_vec.append(0.0)
        up_vec.append(0.0)
        third_vec.append(0.0)
        mat[aim_index] = aim_vec[:4]
        mat[up_index] = up_vec[:4]
        mat[third_index] = third_vec[:4]

        reformat_mat = []
        for lst in mat:
            for i in lst:
                reformat_mat.append(i)
        mc.xform(self.name, matrix=reformat_mat)


class MLocator(MTransform):
    _CREATE_STR = 'locator'

    def __init__(self, name, shape=None):
        super().__init__(name)
        if shape is None:
            shape = f'{name}Shape'
        self.shape = MLocatorShape(shape)

    @classmethod
    def create(cls, name=None, **kwargs) -> 'MLocator':
        if name is None:
            name = cls._CREATE_STR
        shape = mc.createNode('locator', name=f'{name}Shape')
        transform = mc.listRelatives(shape, parent=True)[0]
        instance = cls(transform, shape)
        instance.rename(name)
        if GlobalConfig.locator_root:
            instance.set_parent(GlobalConfig.locator_root)
        under = kwargs.pop('under', '')
        if under:
            instance.set_parent(under)
        match = kwargs.pop('match', '')
        if match:
            instance.match(MTransform(match))
        match_parent = kwargs.pop('match_parent', '')
        if match_parent:
            instance.set_parent(match_parent)
            instance.match(MTransform(match_parent))

        return instance


class MJoint(MTransform):
    _CREATE_STR = 'joint'


class MTransformList(object):
    MEMBER_TYPE = MTransform

    def __init__(self, mt_names):
        self.node_names = mt_names
        self.nodes = []
        self._init_node_list()
        self.len = len(self.node_names)

    def __getitem__(self, idx) -> MTransform:
        return self.nodes[idx]

    def __iter__(self) -> Iterator[MTransform]:
        return iter(self.nodes)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.len}):{self.node_names}'

    def _init_node_list(self):
        from XBase.MBaseFunctions import get_list_types
        lst_types = get_list_types(self.node_names)
        if isinstance(lst_types, list) and len(lst_types) > 1:
            raise ValueError(f'Input node list:{self.nodes} has more than one type:{lst_types}')
        if lst_types == str:
            self.nodes = [self.MEMBER_TYPE(name) for name in self.node_names]
        elif lst_types == self.MEMBER_TYPE:
            self.nodes = self.node_names
            self.node_names = [jnt.name for jnt in self.node_names]

    @classmethod
    def create(cls, names: list):
        from XBase.MBaseFunctions import check_list_exist
        exist = check_list_exist(names)
        nodes_created = []
        if not exist:
            for name in names:
                node = cls.MEMBER_TYPE.create(name=name)
                nodes_created.append(node)
            return cls(nodes_created)
        else:
            return cls(names)

    @property
    def pos_array(self):
        positions = []
        for i in self:
            pos = mc.xform(i.name, q=True, worldSpace=True, translation=True)
            positions.append(pos)
        return positions

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
        if GlobalConfig.transform_root:
            self.nodes[0].set_parent(GlobalConfig.transform_root)


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

    def __len__(self):
        return len(self.node_names)


class MJointChain(MJointSet):
    # todo :修改成员的名字后，没有同步更新,需要改进
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
        if GlobalConfig.transform_root:
            instance[0].set_parent(GlobalConfig.transform_root)
        return cls(instance.node_names)

    @classmethod
    def create_from_spline(cls, alias, spline: str, count: int, uniformed=True):
        """
        提供三种根据曲线生成骨骼的方法
        根据cv位置生成 count=-1
        根据曲线长度均匀生成 uniformed=True
        根据曲线参数域均匀生成 uniformed=False
        """
        # if not mc.objectType(spline) == 'nurbsCurve':
        #     raise ValueError(f'Input spline:{spline} is not nurbsCurve')
        shape_fn = OMUtils.get_nurbsCurve_fn_from(spline)
        generated = []
        if count == -1:
            for i in range(shape_fn.numCVs):
                pos = shape_fn.cvPosition(i)
                jnt = MJoint.create(f'{alias}_{i + 1:02d}_Jnt')
                jnt.translate.set(list(pos))
                generated.append(jnt)
        else:
            for i, percent in enumerate(linear_space(0, 1, count)):
                if uniformed:
                    length = percent * shape_fn.length()
                    real_u = shape_fn.findParamFromLength(length)
                else:
                    min_u, max_u = shape_fn.knotDomain
                    real_u = (percent * (max_u - min_u)) + min_u
                pos = shape_fn.getPointAtParam(real_u)
                jnt = MJoint.create(f'{alias}_{i + 1:02d}_Jnt')
                jnt.translate.set(list(pos))
                generated.append(jnt)
        instance = cls(generated)
        instance.parent_all()
        return instance

    @property
    def plane_normal(self):
        from XBase.MBaseFunctions import cross_product
        vec1 = self[1].world_pos - self[0].world_pos
        vec2 = self[2].world_pos - self[1].world_pos
        normal = cross_product(vec1, vec2)
        return normal

    @classmethod
    def duplicate(cls, other):
        pass

    def rename_chain(self, new_names):
        for i, jnt in enumerate(self):
            jnt.rename(new_names[i])
        self.node_names[:len(new_names)] = new_names
        self.nodes = [MJoint(i) for i in self.node_names]

    def update_chain(self):
        self.unparent_all()
        self.parent_all()

    def convert_to_curve(self):
        pass

    def duplicate(self):
        pass

    def reorient(self, aim_axis, up_axis, up_obj):
        from XBase.MBaseFunctions import revert_axis
        previous_parent = self[0].parent
        self.unparent_all()
        for i, jnt in enumerate(self):
            if not i == len(self) - 1:
                print(i, len(self))
                constraint_node = jnt.set_aim_constraint(
                    other=self.node_names[i + 1],
                    aim_vec=aim_axis,
                    up_vec=up_axis,
                    up_type=WorldUpType.Object.value,
                    up_obj=up_obj
                )
            else:
                constraint_node = jnt.set_aim_constraint(
                    other=self.node_names[i - 1],
                    aim_vec=revert_axis(aim_axis),
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
        from XBase.MBaseFunctions import normalize_vector
        pre_parent = self[0].parent
        self.unparent_all()
        aim_vecs = []
        for i, jnt in enumerate(self):
            if i != len(self) - 1:
                jnt_aim_vec = [round(i, 10) for i in tuple((self[i + 1].world_pos - jnt.world_pos).normal())]
            else:
                jnt_aim_vec = aim_vecs[i - 1]

            aim_vecs.append(jnt_aim_vec)
            jnt.reorient(aim_axis=aim_axis,
                         aim_vec=normalize_vector(jnt_aim_vec),
                         up_axis=up_axis,
                         up_vec=normalize_vector(self.plane_normal))
            jnt.freeze()
        self.parent_all()
        self[0].set_parent(pre_parent)

    def reverse_chain(self):
        self.unparent_all()
        self.parent_all(reverse=True)

    def freeze(self):
        for jnt in self:
            jnt.freeze()

    def resample_by_proportion(self, count):
        from XBase.MBaseFunctions import linear_space
        if self.len != 2:
            raise RuntimeError(f'Can not resample joint chain,length of chain should be 2')
        vec_to_scale = [i for i in self.nodes[-1].world_pos - self.nodes[0].world_pos]
        linear_indecies = linear_space(0, 1, count - 1)
        new_chain = []
        for i, factor in enumerate(linear_indecies):
            new_jnt = MJoint.create(f'tmp_{i + 1}')
            new_jnt.match(self.nodes[0])
            new_jnt.move_by([factor * j for j in vec_to_scale])
            new_chain.append(new_jnt)
        new_m_jnt_chain = MJointChain(new_chain)
        new_m_jnt_chain.parent_all()
        new_m_jnt_chain.freeze()


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
        super().create(joints)
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
    def total_length(self):
        return self.vec_ab.length() + self.vec_bc.length()

    @property
    def pv_vec(self) -> om.MVector:
        """
        a*b = |a|*|b|*cos
        → a*b/|b| = |a|*cos
        → 点乘结果除以b的模长等于a在b上的投影长度，再除以b的模长，等于投影在b上占的比例
        """

        factor = (self.vec_ab * self.vec_ac) / self.vec_ac.length() ** 2
        vec_db = self.vec_ab - self.vec_ac * factor

        return vec_db

    @property
    def normal(self):
        from XBase.MBaseFunctions import cross_product
        return cross_product(self.vec_ab, self.vec_bc)

    def get_pole_vec_pos(self, multiplier=2):
        vec: om.MVector = self.pv_vec * multiplier
        pv_pos = self[1].world_pos + vec
        return pv_pos


class MQuadJointChain(MJointChain):

    def __init__(self, joints):
        super().__init__(joints)

    def __getitem__(self, idx) -> Union[MJoint, 'MQuadJointChain']:
        if isinstance(idx, slice):
            return MQuadJointChain(self.nodes[idx])
        else:
            return MJoint(self.nodes[idx])
