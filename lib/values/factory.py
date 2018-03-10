from lib.values.ssh import SshPrivateKey, SshPublicKey


class ValueFactory:
    FACTORY_MAP = {
        "ssh_private_key": lambda x: SshPrivateKey(x),
        "ssh_public_key": lambda x: SshPublicKey(x)
    }

    def __init__(self):
        self.x = True

    @staticmethod
    def supports(definition):
        return definition['type'] in ValueFactory.FACTORY_MAP

    @staticmethod
    def get_value(definition):
        return ValueFactory.FACTORY_MAP.get(definition['type'], )(definition)
