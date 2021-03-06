from lib.values.simple import Simple
from lib.values.ssh import SshPrivateKey, SshPublicKey
from lib.values.text import UUID, Username, Password


class ValueFactory:
    FACTORY_MAP = {
        "ssh_private_key": lambda x, y: SshPrivateKey(x, y),
        "ssh_public_key": lambda x, y: SshPublicKey(x, y),
        "uuid": lambda x, y: UUID(x, y),
        "username": lambda x, y: Username(x, y),
        "password": lambda x, y: Password(x, y),
        'simple': lambda x, y: Simple(x, y)
    }

    def __init__(self):
        self.x = True

    @staticmethod
    def supports(definition):
        return definition.get('type', 'simple') in ValueFactory.FACTORY_MAP

    @staticmethod
    def get_value(definition, parent):
        return ValueFactory.FACTORY_MAP.get(definition.get('type', 'simple'), )(definition, parent)
