import sys
import logging

import maya.cmds as mc
import maya.api.OpenMaya as om

from XBase.MShape import MNurbsSurfaceShape
from XBase.MTransform import MJoint, MLocator
from LoggingSetup import setup_global_logger

setup_global_logger()


def standalone():
    import maya.standalone
    maya.standalone.initialize()


def dev_reset_scene():
    mc.file(newFile=True, force=True)
    # mc.viewSet(front=True)

def dev_create_ik_joints(names=None):
    from XBase import MTransform as mt
    names = ['jnt1', 'jnt2', 'jnt3'] if not names else names
    jc = mt.MTripleJointChain.create(names)
    jc[1].tx.set(10)
    jc[2].tx.set(10)
    jc[0].ry.set(30)
    jc[1].ry.set(-60)
    jc.freeze()
    return jc
def dev_reload():
    from importlib import reload
    to_reload = []
    for key, value in sys.modules.items():
        if 'ProjectX' in str(value):
            to_reload.append(value)

    for m in to_reload:
        try:
            reload(m)
            print(f'{m} reloaded!')
        except ModuleNotFoundError:
            print(f'Failed to reload module:{m},module not found')


def reload_stdout():
    import sys
    import maya.app.startup.basic

    # Run the user's userSetup.py if it exists
    maya.app.startup.basic.executeUserSetup()

    import maya.app.baseUI
    import maya.utils

    # Replace sys.stdin with a GUI version that will request input from the user
    sys.stdin = maya.app.baseUI.StandardInput()

    # Replace sys.stdout and sys.stderr with versions that can output to Maya's
    # GUI
    sys.stdout = maya.utils.Output()
    sys.stderr = maya.utils.Output(error=1)


def dev():
    from XBase import MTransform as mt
    joint_chain = mt.MJointChain.create([f'joint_{i}' for i in range(10)])
    for jnt in joint_chain:
        print(jnt.dp_node)
        print(jnt.dag_path.fullPathName())


def dev_attribute():
    dev_reset_scene()
    from XBase import MTransform as mt
    from XBase.MNodes import MNode
    from XBase.MBaseFunctions import arg_match_attr
    jc = mt.MTransform.create('test')
    # j2 = mt.MJoint.create('joint_1')
    # jc.translateX.mount([1,2,3])
    print(arg_match_attr(1, jc.translateX.full_name))


def dev_print():
    data = {'name': {
        'pos_array': [1, 2, 3, 4]
    }}
    print(list(data.keys())[0])


def dev_mt():
    from XBase import MTransform as mt
    # mt_node = mt.MTransform.create('test', with_offset=True)
    mt2 = mt.MTransform.create('test2')
    mt2.insert_parent('offset')
    # mt2.set_parent(mt_node)


def dev_math():
    from XBase import MMathNode
    add = MMathNode.addDoubleLinear.create()


def dev_ui():
    # from PySide6 import QtWidgets
    # for widget in QtWidgets.QApplication.topLevelWidgets():
    #     if widget.windowTitle() == 'XRig':
    #         widget.deleteLater()
    # main_ui = XUI.XMainWindow.XRigMainWindow()
    # main_ui.show()
    pass


def dev_component():
    dev_reset_scene()
    from XBase.MTransform import MJointChain
    from XModules import MComponent
    jc = dev_create_ik_joints()
    # jc = MJointChain.create([f'jnt_{i}' for i in range(7)])
    # for jnt in jc[1:]:
    #     jnt.tx.mount(1)
    cp = MComponent.SurfaceBaseTwistComponent('LF_Arm_01_Twist', jc)
    cp.build()


def dev_create_skinned_mesh():
    from XBase import MTransform as mt
    plane = mc.polyPlane(subdivisionsX=5, subdivisionsY=5)[0]
    jnts = [mt.MJoint.create(f'test_jnt_{i}').name for i in range(10)]

    mc.skinCluster(*jnts, plane, dropoffRate=4.5)
    return plane, jnts


def dev_save_data():
    standalone()
    mesh, jnts = dev_create_skinned_mesh()
    from XBase import MGeometry
    from XBase.MData import MCurveData, MWeightData
    # weight = MSkinCluster.get_skin_cluster_from_node(mesh).collect_weight_data()
    # file_path = os.path.join(MCurveData.DATA_DIR,'nurbsCircleShape1.json')
    # data = MCurveData.load_from_file(file_path)
    # print(data)


def dev_geo():
    from XTools import XWeightTool
    XWeightTool.WeightDataCollector()


def dev_generate_node_slot():
    from XBase import BuildNodeCache
    BuildNodeCache.build_math_node_cache()


def dev_matrix():
    standalone()
    # dev_reset_scene()
    from XBase.MGeometry import MMesh
    from XBase.MTransform import MLocator
    import XBase.MMathNode as mn
    plane = MMesh.create('test_plane')

    loc1 = MLocator.create('loc1')
    loc2 = MLocator.create('loc2')

    mulMat1 = mn.multMatrix.create('mul1')
    mulMat2 = mn.multMatrix.create('mul2')

    dMat1 = mn.decomposeMatrix.create('dMat1')
    dMat2 = mn.decomposeMatrix.create('dMat2')

    mdl1 = mn.multDoubleLinear.create('mdl1')
    mdl2 = mn.multDoubleLinear.create('mdl2')

    loc1.worldPosition.connect(mulMat1.matrixIn)
    mulMat1.matrixSum.connect(dMat1.inputMatrix)
    dMat1.outputTranslateZ.connect(mdl1.input1)


def dev_create_joints(num, alias='', offset=1, parent=True, attr='tx'):
    jnts = []
    for i in range(num):
        jnt_name = f'{alias}_{i + 1:02d}_Jnt'
        jnt = mc.createNode('joint', name=f'{alias}_{i + 1:02d}_Jnt')
        jnts.append(jnt)
        if parent:
            if i > 0:
                print(jnt, jnts[i - 1])
                mc.parent(jnt, jnts[i - 1])
        if offset and i > 0:
            mc.setAttr(f'{jnt}.{attr}', offset)

    return jnts


def dev_reoient():
    # dev_reset_scene()
    from XBase.MConstant import Axis
    from XBase.MTransform import MJointChain
    jnts = MJointChain(mc.ls(selection=True))
    jnts.reorient_to_plane_normal(Axis.Y.name, Axis.X.name)


def dev_template():
    # dev_reset_scene()
    standalone()
    names = ['Shoulder', 'Elbow', 'Wrist']
    # jnts = dev_create_joints(num=3, alias='Test', offset=10, parent=True, attr='tx')
    # for i, jnt in enumerate(jnts):
    #     mc.rename(jnt, names[i])


def dev_build_node_slot():
    # standalone()
    from XBase import BuildNodeCache
    attrs = BuildNodeCache.build_math_node_cache()
    print(attrs)


def dev_skirt():
    from XBase import MTransform as mt
    from XBase.MMathNode import colorMath, dotProduct, setRange, remapValue
    from XBase.MConstant import Axis
    import math
    dev_reset_scene()

    test_scene_path = r'F:\作品集\Rig\Skirt\skirt_test_scene.mb'
    mc.file(test_scene_path, i=True)
    leg_jc = mt.MJointChain.create(['Leg_01_Jnt', 'Leg_02_Jnt'])
    leg_jc[1].ty.set(1.6)
    skirt_mesh = 'skirt_meshShape'
    origin_loc = mt.MTransform.create('origin_loc')
    origin_loc_tip = mt.MTransform.create('origin_loc_tip')
    mc.pointConstraint(leg_jc[1].name, origin_loc_tip.name)

    leg_vec_node = colorMath.create(name='leg_vec')
    leg_vec_node.operation.set(1)
    origin_loc_tip.translate.connect(leg_vec_node.colorB)
    origin_loc.translate.connect(leg_vec_node.colorA)

    raw_data_node = mt.MTransform.create('raw')
    remap_data_node = mt.MTransform.create('remap')
    leg_jc[0].add_attr(attr_name='param1', at='float', k=True)

    for idx in range(20):
        attr_name = f'Jnt_{idx}_dot'
        raw_data_node.add_attr(attr_name=attr_name, at='float', k=True)
        vtx = f'{skirt_mesh}.vtx[{idx}]'
        vtx_up = f'{skirt_mesh}.vtx[{idx + 20}]'

        jc = mt.MJointSet.create([f'Jnt_{vtx}', f'Jnt_{vtx_up}'])
        jc[0].translate.set(mc.xform(vtx, worldSpace=True, translation=True, q=True))
        jc[1].translate.set(mc.xform(vtx_up, worldSpace=True, translation=True, q=True))
        jc[1].set_parent(jc[0])

        # set orientation
        aim_vector = list((jc[0].world_pos - leg_jc[0].world_pos).normal())
        jc[0].reorient(aim_axis=Axis.X.name, aim_vec=aim_vector,
                       up_axis=Axis.Y.name, up_vec=[0.0, 1.0, 0.0])

        target_loc = mt.MTransform.create(f'target_loc_{vtx_up}')
        target_loc.translate.set(mc.xform(jc[1].name, worldSpace=True, translation=True, q=True))
        target_vec = colorMath.create(name=f'{target_loc.name}_vec')
        target_vec.operation.set(1)

        origin_loc.translate.connect(target_vec.colorB)
        target_loc.translate.connect(target_vec.colorA)

        dot = dotProduct.create(f'dot_{vtx_up}')

        leg_vec_node.outColor.connect(dot.input2)
        target_vec.outColor.connect(dot.input1)

        dot.output.connect(raw_data_node.attr(attr_name))

        remap = remapValue.create(f'remap_{attr_name}')
        raw_data_node.attr(attr_name).connect(remap.inputValue)
        remap.inputMin.set(-3.052)
        remap.inputMax.set(-2.668)

        remap.outputMin.set(0)
        remap.outputMax.set(1)

        remap_attr_name = f'Jnt_{idx}_remap'
        remap_data_node.add_attr(attr_name=remap_attr_name, at='float', k=True)

        remap.outValue.connect(f'{remap_data_node}.{remap_attr_name}')

        # getattr(sRange, remap_attr_name).connect()
        jc[0].freeze()

        rot_remap = remapValue.create(f'Jnt_{idx}_rot_remap')
        remap_data_node.attr(remap_attr_name).connect(rot_remap.inputValue)
        rot_remap.inputMin.set(0)
        rot_remap.inputMax.set(1)

        rot_remap.outputMin.set(-40)
        rot_remap.outputMax.set(0)

        rot_remap.outValue.connect(jc[0].rz)

        # mc.connectAttr(f'{leg_jc[0].name}.param1', f'{rot_remap.name}.value[0].value_Position')
        leg_jc[0].attr('param1').connect(f'{rot_remap.name}.value[0].value_Position', compound=True)


def dev_triple_jc():
    from XBase.MTransform import MTripleJointChain, MTransform
    sel = mc.ls(selection=True)
    jc = MTripleJointChain.create(sel)
    # jc[0].rotateY.set(30)
    # jc[1].translateX.set(5)
    # jc[1].rotateY.set(-60)
    # jc[2].translateX.set(5)
    loc = MTransform.create(posisition=jc.get_pole_vec_pos())
    loc.match(jc[1].name, rotation=True)


def dev_create_psd_locs():
    # dev_reset_scene()
    # path = r'F:\作品集\Rig\Girl\test_adv_scene.mb'
    # mc.file(path, i=True)
    import XBase.MTransform as mt
    from XBase.MMathNode import vectorProduct
    jnt_names = ['Hip', 'Knee', 'Ankle', 'Shoulder', 'Elbow', 'Wrist']
    dot_value_collect_node = mt.MTransform('dot_value_collect')
    for side in ['L', 'R']:
        factor = 1 if side == 'R' else -1
        for jnt in jnt_names:
            jnt_name = f'{jnt}_{side}'
            jnt_node = mt.MTransform(jnt_name)

            root_space_grp = mt.MTransform.create(f'{jnt_name}_Root_Space', under=jnt_node.parent)
            root_space_grp.match(jnt_node)

            origin_loc = mt.MLocator.create(f'{jnt_name}_Origin_Loc', parent=root_space_grp, match=jnt_name)
            # vector
            move_loc = mt.MLocator.create(f'{jnt_name}_Move_Loc', match_parent=jnt_node)
            move_loc.tx.set(factor * 100.0)
            move_vec = move_loc.shape.worldPosition.subtract(origin_loc.shape.worldPosition, 'test')

            for axis in ['y', 'z']:
                for angle in [90]:
                    origin_tip_loc = mt.MLocator.create(f'{jnt_name}_OriginTip{axis.capitalize()}{angle}_Loc',
                                                        match_parent=root_space_grp
                                                        )

                    par = origin_tip_loc.insert_parent(f'{origin_tip_loc.name}_Offset')
                    par.attr(f'r{axis}').set(angle)

                    origin_tip_loc.tx.set(factor * 100.0)
                    axis_vec = origin_tip_loc.shape.worldPosition.subtract(origin_loc.shape.worldPosition, 'test')
                    cos = om.MVector(*move_vec.outColor.value).normal() * om.MVector(
                        *axis_vec.outColor.value).normal()
                    dot = vectorProduct.create(f'{origin_tip_loc}_dot')
                    dot.dot(move_vec, axis_vec)

                    dot_value_collect_node.add_attr(attr_name=f'{origin_tip_loc}_dot_value', at='float', k=True)
                    dot_value_collect_node.add_attr(attr_name=f'{origin_tip_loc}_cos', at='float', k=True)
                    dot.outputX.connect(dot_value_collect_node.attr(f'{origin_tip_loc}_dot_value'))
                    dot_value_collect_node.attr(f'{origin_tip_loc}_cos').set(cos)


def dev_MShape():
    from XBase.MData import MCurveData
    from XBase.MGeometry import MNurbsSurface
    from XBase.MShape import MNurbsCurveShape
    from XBase.MTransform import MTransform
    from XBase.MConstant import Axis
    surface = MNurbsSurface(MTransform('LF_Arm_01_Twist_Surface'),MNurbsSurfaceShape('LF_Arm_01_Twist_SurfaceShape'))
    surface.create_joint_on('test_jnt',uv=(0.5,0.5),aim_axis=Axis.X.name,up_axis=Axis.Y.name)
def dev_rename():
    import maya.cmds as mc
    sel = mc.ls(selection=True, long=True)
    alias = 'LF_Sleeve_01'
    for i, jnt in enumerate(sel):
        print(i)
        mc.rename(jnt, f'{alias}_{i + 1:02d}_Jnt')


def dev_redirect_sdk():
    from XBase import MTransform as mt
    driver_attr = 'dot_value_collect.Shoulder_R_OriginTipNZ90_0_Loc_dot_value'
    driver_value = mc.getAttr(driver_attr)
    grp_suffix = f'test_grp'
    sel = mc.ls(selection=True)
    for i, node in enumerate(sel):
        mt_node = mt.MTransform(node)
        driven_grp = mt.MTransform.create(f'{node}_NRZ90', match=mt_node)
        driven_grp.set_parent(mt_node.parent)
        mt_node.set_parent(driven_grp)
        for axis in ['x', 'y', 'z']:
            for t in ['t', 'r', 's']:
                attr = f'{driven_grp.name}.{t}{axis}'
                attr_defalut_value = mc.attributeQuery(f'{t}{axis}', node=driven_grp.name, listDefault=True)[0]
                attr_value = mc.getAttr(attr)
                print(attr, attr_value, attr_defalut_value)
                # if attr_value - attr_defalut_value < 0.0001:
                #     continue
                mc.setDrivenKeyframe(attr,
                                     currentDriver=driver_attr,
                                     driverValue=0,
                                     value=attr_defalut_value,
                                     inTangentType='linear',
                                     outTangentType='linear')
                mc.setDrivenKeyframe(attr,
                                     currentDriver=driver_attr,
                                     driverValue=driver_value,
                                     value=attr_value,
                                     inTangentType='linear',
                                     outTangentType='linear'
                                     )
        mt_node.t.set([0, 0, 0])
        mt_node.r.set([0, 0, 0])
        mt_node.jointOrient.set([0, 0, 0])


def dev_add_mirror_joint_to_cluster():
    from XBase import MBaseFunctions
    infs = MBaseFunctions.get_mesh_infs(mc.ls(selection=True)[0])
    # LF_Joints = [i for i in infs if 'LF' in i]
    # RT_Joints = [i.replace('LF', 'RT') for i in LF_Joints]
    # sc = MBaseFunctions.get_skin_cluster(mc.ls(selection=True)[0])
    # for jnt in RT_Joints:
    #     if jnt in infs:
    #         continue
    #     if mc.objExists(jnt):
    #         mc.skinCluster(sc, e=True, addInfluence=jnt, weight=0.0)
    #         print(f'Add {jnt} to {sc}')
    #     else:
    #         print(f'{jnt} do not exist!')

    for i in infs:
        print(i)
    print(len(infs))


def create_ctrl_for_jnts():
    from XBase import MTransform as mt
    sel = mc.ls(selection=True)
    for jnt in sel:
        jnt_mt = mt.MTransform(jnt)
        if jnt_mt.children is None:
            continue
        ctrl = mc.duplicate('Cube_Prototype')[0]
        ctrl_mt = mt.MTransform(ctrl)
        ctrl_mt.rename(f'{jnt}_Ctrl')
        ctrl_mt.match(jnt_mt)
        ctrl_mt.set_parent(jnt_mt.parent)
        jnt_mt.set_parent(ctrl_mt)
        ctrl_mt.insert_parent(f'{ctrl_mt.name}_Grp')
        ctrl_mt.insert_parent(f'{ctrl_mt.name}_Offset')


def dev_set_color(shapes=None):
    color = [0, 0, 1]
    from XBase import MTransform as mt
    sel = mc.ls(selection=True)
    if shapes is None:
        shapes = sel
    for node in shapes:
        node_mt = mt.MTransform(node)
        node_mt.overrideEnabled.set(1)
        node_mt.overrideRGBColors.set(1)
        node_mt.overrideColorRGB.set(color)


def dev_symetry_loc_on_select():
    from XBase import MTransform as mt
    sel = mc.ls(selection=True)[0] or None
    if sel is None:
        raise RuntimeError(f'Select a node')
    loc = mt.MLocator.create(match=sel)
    loc.tx.set(loc.tx.value * -1)


def dev_extarct_bind_joints():
    from XBase import MTransform as mt
    sc = mc.ls(type='skinCluster')
    bind_infs = []
    print(bind_infs)
    for skin in sc:
        infs = [i for i in mc.listHistory(skin) if mc.objectType(i) == 'joint']
        for inf in infs:
            if inf in bind_infs:
                continue
            bind_infs.append(inf)
    jnt_data = []
    for jnt in bind_infs:
        world_mat = mc.getAttr(f'{jnt}.worldMatrix')
        parent = mc.listRelatives(jnt, parent=True)
        while not mc.objectType(parent) == 'joint':
            parent = mc.listRelatives(parent, parent=True)
            if parent is None:
                parent = None
                break
        jnt_data.append([world_mat, parent])
    out_jnts = []
    for jnt, data in zip(bind_infs, jnt_data):
        new_jnt = mc.createNode('joint', name=f'{jnt}_output')
        mc.xform(new_jnt, worldSpace=True, matrix=data[0])
        out_jnts.append(new_jnt)

    for i, jnt in enumerate(out_jnts):
        if jnt_data[i][1] is None:
            continue
        mc.parent(jnt, f'{jnt_data[i][1][0]}_output')
        jnt_mt = mt.MTransform(jnt)
        jnt_mt.freeze()


def dev_rebuild_constraint():
    from XBase import MTransform as mt
    sel = mc.ls(selection=True)
    for jnt in mc.listRelatives(sel, allDescendents=True, children=True):
        # jnt_mt = mt.MTransform(jnt)
        # jnt_mt.freeze()
        origin = jnt.replace('_output', '')
        mc.parentConstraint(origin, jnt)


def dev_redirect_sc():
    sc = mc.ls(type='skinCluster')
    bind_infs = []
    for skin in sc:
        infs = [i for i in mc.listHistory(skin) if mc.objectType(i) == 'joint']
        for inf in infs:
            if inf in bind_infs:
                continue
            bind_infs.append(inf)
    for jnt in bind_infs:

        attrs = [i for i in mc.listConnections(jnt, destination=True, source=True, plugs=True) if
                 'bindPose' in i or '_sc' in i]
        print(jnt)
        print(attrs)
        output_jnt = f'{jnt}_output'
        data = []
        for attr in attrs:
            source_attr = mc.listConnections(attr, source=True, plugs=True)[0]
            output_jnt_attr = source_attr.replace(jnt, output_jnt)
            data.append([output_jnt_attr, attr])
        for a1, a2 in data:
            try:
                mc.connectAttr(a1, a2, force=True)
            except:
                print(a1, a2)


def dev_create_pivot_follicle():
    import XBase.MTransform as mt
    import XBase.MNodes as mn
    sel = mc.ls(selection=True)
    for grp in sel:
        u = 0.5
        v = 0.5
        np = mc.nurbsPlane(width=0.5, degree=2)
        np_mt = mt.MTransform(np[0])
        np_mt.rename(f'{grp}_Surface')
        np_mt.match(grp)
        np_shape = np_mt.child
        fol = mc.createNode('follicle', name=f'{grp}_folShape')
        print(fol)
        mc.connectAttr(f'{np_shape.name}.local', f'{fol}.inputSurface')
        mc.connectAttr(f'{np_shape}.worldMatrix', f'{fol}.inputWorldMatrix')
        fol_trans = mc.listRelatives(fol, parent=True)[0]
        mc.rename(fol_trans, f'{grp}_fol')
        mc.connectAttr(f'{fol}.outTranslate', f'{fol_trans}.translate')

        mc.setAttr(f'{fol}.parameterU', u)
        mc.setAttr(f'{fol}.parameterV', v)


def dev_create_tip():
    from XBase import MTransform as mt
    sel = mc.ls(selection=True)
    for jnt in sel:
        child = mc.listRelatives(jnt, children=True, allDescendents=True)[0]

        child_mt = mt.MTransform(child)
        tip = mt.MJoint.create(name=f'{child}_tip', under=child, match=child)
        tip.tx.set(10)
        tip.freeze()


def dev_skin_weight():
    dev_reset_scene()
    path = r'F:\TMP\test.fbx'
    if not mc.pluginInfo("fbxmaya", q=True, loaded=True):
        mc.loadPlugin("fbxmaya")
    mc.file(path, i=True, type='FBX', ignoreVersion=True)
    from XBase.MDeformer import MSkinCluster
    from XBase.MBaseFunctions import compress_list, decompress_lst

    sc_name = [i for i in mc.listHistory('F01_MacheLotus01_UpBody_HDShape') if mc.objectType(i) == 'skinCluster'][0]
    msc = MSkinCluster('F01_MacheLotus01_UpBody_HDShape', sc_name)

    weight = msc.get_weight_array()
    compressed_weight = compress_list(list(weight))
    # decompressed_weight = decompress_lst(compressed_weight)
    inf_matrix = [MJoint(i).worldMatrix.value for i in msc.influences]
    inf_parens = [MJoint(i).parent.name for i in msc.influences]
    with open('./test.txt', 'w') as f:
        f.write(str([sc_name, msc.influences, inf_parens, inf_matrix, compressed_weight]))


def dev_load_skin_weight():
    dev_reset_scene()
    import ast
    from XBase.MBaseFunctions import compress_list, decompress_lst, OMUtils
    from XBase.MTransform import MJoint
    from XBase.MDeformer import MSkinCluster
    data_path = r'F:\Code\Python\ProjectX\test.txt'
    path = r'F:\TMP\cloth_geo.fbx'
    if not mc.pluginInfo("fbxmaya", q=True, loaded=True):
        mc.loadPlugin("fbxmaya")
    mc.file(path, i=True, type='FBX', ignoreVersion=True)
    with open(data_path, 'r') as f:
        data = ast.literal_eval(f.read())
        infs = [i.replace('_output', '') for i in data[1]]
        parents = data[2]
        matrices = data[3]
        weight = decompress_lst(data[4])
    for i, inf in enumerate(infs):
        jnt = MJoint.create(inf)
        mc.xform(jnt.name, worldSpace=True, matrix=matrices[i])
        jnt.freeze()
    for i, jnt in enumerate(infs):
        try:
            jnt_mt = MJoint(jnt)
            jnt_mt.set_parent(parents[i].replace('_output', ''))
        except:
            pass
    sc = mc.skinCluster(*infs, 'F01_MacheLotus01_UpBody_HD')[0]
    msc = MSkinCluster('F01_MacheLotus01_UpBody_HDShape', sc)
    mapper = [msc.skin_fn.indexForInfluenceObject(OMUtils.get_dag_path(i)) for i in
              [jnt.replace('_output', '') for jnt in infs]]
    weight_data = decompress_lst(weight)
    # final_weight = msc.rearrange_weight(weight_data,mapper)
    msc.set_weight(weight_data, [i for i in range(len(infs))])


def dev_ast():
    from XBase.MNodeGraph import Lexer
    txt = 'a.tx + b.ty+z.tz'
    Lexer(txt).get_tokens()

def dev_spline():
    dev_reset_scene()
    from XBase.MGeometry import MNurbsCurve
    from XBase.MTransform import MLocator
    curve = MNurbsCurve.create_by_points('test_curve',[[0,0,0],[1,0,0],[2,0,0],[3,0,0],[8,0,0]])
    point=curve.shape.shape_fn.getPointAtParam(1)
    print(point)
    print(curve.shape.minValue.value)
    print(curve.shape.maxValue.value)
    locator = MLocator.create('test_loc')
    locator.match_pos([i for i in list(point)[:3]])
if __name__ == '__main__':
    # help(om.MVector)
    standalone()
    dev_build_node_slot()
