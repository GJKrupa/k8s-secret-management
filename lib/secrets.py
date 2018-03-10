from os import listdir
from os.path import isfile, join
from ruamel.yaml import YAML

from lib.values.factory import ValueFactory


class Secret:
    def __init__(self, filename):
        with open(filename, 'r') as stream:
            yaml = YAML()
            data = yaml.load(stream)
            print(data)
            self.name = data['name']
            self.description = data.get('description', None)
            self.values = [
                ValueFactory.get_value(value) for value in data['values'] if ValueFactory.supports(value)
            ]

    def generate(self, lookup):
        affected = {self.name: True}
        for value in self.values:
            affected.update(value.generate(lookup))
        return affected


class Secrets:
    def __init__(self):
        self.value_table = {}
        self.secrets = [
            Secret(join("definitions", f)) for f in listdir("definitions") if isfile(join("definitions", f)) and f.endswith(".yaml")
        ]

        for secret in self.secrets:
            self.value_table[secret.name] = secret

    def generate(self):
        affected = {}
        for secret in self.secrets:
            affected.update(secret.generate(self.value_table))
        return affected
