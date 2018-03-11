from lib.values.base import BaseValue


class Simple(BaseValue):
    def __init__(self, definition, parent):
        super(self.__class__, self).__init__(definition, parent)

    def generate(self, namespace, lookup):
        return {}

    def references(self, secret_name, value_name):
        return False
