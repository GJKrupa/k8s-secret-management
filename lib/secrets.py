from os import listdir
from os.path import isfile, join
from ruamel.yaml import YAML

from lib.values.factory import ValueFactory


class Lookup:
    def __init__(self):
        self.table = {}

    def __setitem__(self, key, value):
        self.table[key] = value

    def references_to(self, name):
        result = {}
        for secret in self.table.values():
            for value in secret.values:
                if value.references(name):
                    result[secret.name] = True
        return result


class Secret:
    def __init__(self, filename):
        with open(filename, 'r') as stream:
            yaml = YAML()
            data = yaml.load(stream)
            self.name = data['name']
            self.description = data.get('description', None)
            self.values = [
                ValueFactory.get_value(value, self) for value in data['values'] if ValueFactory.supports(value)
            ]

    def generate(self, namespace, lookup, filter_value):
        affected = {}
        for value in self.values:
            if filter_value is None or filter_value==value.name:
                affected.update(value.generate(namespace, lookup))
        return affected


class Secrets:
    def __init__(self):
        self.lookup = Lookup()
        self.secrets = [
            Secret(join("definitions", f)) for f in listdir("definitions") if isfile(join("definitions", f)) and f.endswith(".yaml")
        ]

        for secret in self.secrets:
            self.lookup[secret.name] = secret

    def generate(self, namespace, filter_secret, filter_value):
        affected = {}
        for secret in self.secrets:
            if filter_secret is None or secret.name==filter_secret:
                affected.update(secret.generate(namespace, self.lookup, filter_value))
        return affected
