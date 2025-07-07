from XBase.MNodes import MNode, MAttribute


class MShapeNode(object):

    def __init__(self, shape_name):
        self.shape_name = shape_name

    def __getattr__(self, item):
        return MAttribute(self.name, item)


class MLocatorShape(MShapeNode):

    def __init__(self, shape_name):
        super().__init__(shape_name)
