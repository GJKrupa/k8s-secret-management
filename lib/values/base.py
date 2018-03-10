import os

from lib.values.files import ValueFile


class BaseValue(object):
    def __init__(self, definition, parent):
        self.name = definition['name']
        self.parent = parent

    def generate(self, namespace, lookup):
        raise NotImplementedError("Abstract method")

    def to_base64(self, namespace, lookup):
        raise NotImplementedError("Abstract method")

    def references(self, secret_name):
        raise NotImplementedError("Abstract method")

    def filename(self, namespace):
        return os.path.join("values", namespace, self.name)

    def value_file(self, namespace, mode):
        return ValueFile(self.filename(namespace), mode)
