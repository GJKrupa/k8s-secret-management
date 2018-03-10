from lib.values.base import BaseValue


class SshPrivateKey(BaseValue):
    def __init__(self, definition):
        super(self.__class__, self).__init__(definition)
        self.type = definition['subtype']

    def generate(self, lookup):
        return {}


class SshPublicKey(BaseValue):
    def __init__(self, definition):
        super(self.__class__, self).__init__(definition)
        self.ref_secret = definition['from']['secret']
        self.ref_value = definition['from']['value']

    def generate(self, lookup):
        return {self.ref_secret: True}