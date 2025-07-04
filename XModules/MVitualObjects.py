from XBase.MTransform import MTransform, MJoint


class MVitualObject(object):

    def __init__(self):
        pass

    def instantiate(self):
        pass


class MVitualTransform(MVitualObject):
    VITUAL_NAME = 'VitualTransform'

    def __init__(self):
        super().__init__()

        self.name = self.VITUAL_NAME
        self.pos = [0, 0, 0]
        self.rotate = [0, 0, 0]
        self.scale = [0, 0, 0]

    def instantiate(self):
        instance = MTransform.create(self.name)
        instance.translate.set(self.pos)
        instance.rotate.set(self.rotate)
        instance.scale.set(self.scale)
        return instance


class MVitualJoint(MVitualTransform):

    def __init__(self):
        super().__init__()
        self.name = 'VitualJoint'
        self.rotate_order = 0

    def instantiate(self):
        pass


class MVitualHierarchy(object):

    def __init__(self):
        pass

    def instantiate(self):
        pass
