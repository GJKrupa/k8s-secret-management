from os import listdir
from os.path import isfile, join
from ruamel.yaml import YAML

from lib.values.factory import ValueFactory


class Lookup:
    def __init__(self):
        self.table = {}

    def __setitem__(self, key, value):
        self.table[key] = value

    def references_to(self, secret_name, value_name):
        result = {}
        for secret in self.table.values():
            for value in secret.values:
                if value.references(secret_name, value_name):
                    result[secret.name] = True
        return result

    def find(self, secret_name, value_name):
        return next(value for value in self.table[secret_name].values if value_name == value.name)


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

    def set_from_file(self, namespace, lookup, value_name, filename):
        affected = {}
        for value in self.values:
            if value_name == value.name:
                affected.update(value.set_from_file(namespace, lookup, filename))
        return affected

    def set_from_text(self, namespace, lookup, value_name, content):
        affected = {}
        for value in self.values:
            if value_name == value.name:
                affected.update(value.set_from_text(namespace, lookup, content))
        return affected

    def check(self, namespace, lookup):
        affected = []
        for value in self.values:
            if not(value.check(namespace, lookup)):
                affected.append(value.name)
        return {self.name: affected}


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
            if filter_secret is None or secret.name == filter_secret:
                affected.update(secret.generate(namespace, self.lookup, filter_value))
        return affected

    def set_from_file(self, namespace, secret_name, value_name, filename):
        affected = {}
        for secret in self.secrets:
            if secret.name == secret_name:
                affected.update(secret.set_from_file(namespace, self.lookup, value_name, filename))
        return affected

    def set_from_text(self, namespace, secret_name, value_name, content):
        affected = {}
        for secret in self.secrets:
            if secret.name == secret_name:
                affected.update(secret.set_from_text(namespace, self.lookup, value_name, content))
        return affected

    def check(self, namespace, secret_name):
        affected = {}
        for secret in self.secrets:
            if secret_name is None or secret.name == secret_name:
                affected.update(secret.check(namespace, self.lookup))
        return affected
