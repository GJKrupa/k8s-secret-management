import base64
import json
from os.path import join
from subprocess import check_output

from lib.values.base import BaseValue
from lib.values.files import TempDir, ReadFile


class SshKeyPair:

    def __init__(self, codec):
        self.codec = codec
        pass

    def create(self):
        result = {}
        with TempDir() as dir:
            private_file = join(dir, 'id')
            public_file = join(dir, 'id.pub')
            check_output(['ssh-keygen', '-t', self.codec, '-f', private_file, '-N', ''])
            with open(private_file, 'r') as stream:
                result['private'] = "".join(stream.readlines())
            with open(public_file, 'r') as stream:
                result['public'] = "".join(stream.readlines())
        return result


class SshPrivateKey(BaseValue):
    def __init__(self, definition, parent):
        super(SshPrivateKey, self).__init__(definition, parent)
        self.type = definition['subtype']

    def filename(self, namespace):
        return super(SshPrivateKey, self).filename(namespace) + '.json'

    def generate(self, namespace, lookup):
        affected = {self.parent.name: True}
        with self.write_to_file(namespace, 'w') as stream:
            stream.write(json.dumps(SshKeyPair(self.type).create(), indent=4))
        affected.update(lookup.references_to(self.parent.name, self.name))
        return affected

    def references(self, secret_name, value_name):
        return False

    def set_from_file(self, namespace, lookup, filename):
        raise NotImplementedError("Not implemented")

    def set_from_text(self, namespace, lookup, content):
        raise NotImplementedError("Not implemented")

    def to_base64(self, namespace, lookup):
        with ReadFile(self.filename(namespace)) as input:
            data = json.loads(input)
            return base64.standard_b64encode(data['private'])


class SshPublicKey(BaseValue):
    def __init__(self, definition, parent):
        super(SshPublicKey, self).__init__(definition, parent)
        self.ref_secret = definition['from']['secret']
        self.ref_value = definition['from']['value']

    def references(self, secret_name, value_name):
        return secret_name == self.ref_secret and value_name == self.ref_value

    def generate(self, namespace, lookup):
        return {}

    def set_from_file(self, namespace, lookup, filename):
        raise NotImplementedError("Not implemented")

    def set_from_text(self, namespace, lookup, content):
        raise NotImplementedError("Not implemented")

    def check(self, namespace, lookup):
        return lookup.find(self.ref_secret, self.ref_value).check(namespace, lookup)

    def to_base64(self, namespace, lookup):
        other = lookup.find(self.ref_secret, self.ref_value)
        with ReadFile(other.filename(namespace)) as input:
            data = json.loads(input)
            return base64.standard_b64encode(data['public'])
