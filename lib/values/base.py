class BaseValue(object):
    def __init__(self, definition):
        self.name = definition['name']

    def generate(self, lookup):
        raise NotImplementedError("Abstract method")

    def to_base64(self, lookup):
        raise NotImplementedError("Abstract method")
