from . import MComponent


class TestModule(object):

    def __init__(self, template, config):
        self.template = template
        self.config = config
        self.IK_component = MComponent.IKComponent.create(template, config)
        self.module_name = f'{template.alias}_Module'
        self.module_members = []

    def register_member(self, component):
        self.module_members.append(component)

    def build(self):
        pass

    def test(self):
        for i in range(10):
            self.register_member('')
