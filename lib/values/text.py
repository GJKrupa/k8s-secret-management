import uuid

from lib.values.base import BaseValue


class UUID(BaseValue):
    def __init__(self, definition, parent):
        super(self.__class__, self).__init__(definition, parent)

    def filename(self, namespace):
        return super(self.__class__, self).filename(namespace) + '.txt'

    def generate(self, namespace, lookup):
        with self.value_file(namespace, 'w') as stream:
            stream.write(str(uuid.uuid1()))
        return {self.parent.name: True}

    def references(self, secret_name):
        return False
