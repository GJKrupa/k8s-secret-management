import os

from click import BadParameter
from shutil import copyfile

from lib.values.files import WriteToFile, UpdateFile


class BaseValue(object):
    def __init__(self, definition, parent):
        self.name = definition['name']
        self.parent = parent
        self.definition = definition

    def generate(self, namespace, lookup):
        raise NotImplementedError("Abstract method")

    def to_base64(self, namespace, lookup):
        raise NotImplementedError("Abstract method")

    def references(self, secret_name, value_name):
        raise NotImplementedError("Abstract method")

    def filename(self, namespace):
        return os.path.join("values", namespace, self.parent.name, self.name)

    def write_to_file(self, namespace, mode):
            return WriteToFile(self.filename(namespace), mode)

    def update_file(self, namespace):
        return UpdateFile(self.filename(namespace))

    def set_from_file(self, namespace, lookup, filename):
        affected = {self.parent.name: True}
        affected.update(lookup.references_to(self.parent.name, self.name))
        if not(os.path.isfile(filename)):
            raise BadParameter(filename + " does not exist")
        with self.update_file(namespace) as out:
            copyfile(filename, out.filename)
        return affected

    def set_from_text(self, namespace, lookup, content):
        affected = {self.parent.name: True}
        affected.update(lookup.references_to(self.parent.name, self.name))
        with self.write_to_file(namespace, 'w') as stream:
            stream.write(content)
        return affected
