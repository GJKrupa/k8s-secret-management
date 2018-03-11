import uuid

from os import urandom

from click import ClickException

from lib.values.base import BaseValue

LOWER = "abcdefghijklmnopqrstuvwxyz"
UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGITS = "1234567890"


class UUID(BaseValue):
    def __init__(self, definition, parent):
        super(self.__class__, self).__init__(definition, parent)

    def filename(self, namespace):
        return super(self.__class__, self).filename(namespace) + '.txt'

    def generate(self, namespace, lookup):
        with self.write_to_file(namespace, 'w') as stream:
            stream.write(str(uuid.uuid1()))
        return {self.parent.name: True}

    def references(self, secret_name, value_name):
        return False


class RandomString(BaseValue):
    def __init__(self, definition, parent):
        super(RandomString, self).__init__(definition, parent)
        self.length = definition.get('length', 8)

    def filename(self, namespace):
        return super(RandomString, self).filename(namespace) + '.txt'

    def get_initial(self):
        raise NotImplementedError("Not implemented")

    def get_non_initial(self):
        raise NotImplementedError("Not implemented")

    def is_ok(self, text):
        raise NotImplementedError("Not implemented")

    def generate_str(self):
        rnd = urandom(self.length)
        result = ''
        selection = self.get_initial()
        for s in rnd:
            result = result + selection[ord(s) % len(selection)]
            selection = self.get_non_initial()
        return result

    def generate(self, namespace, lookup):
        result = self.generate_str()
        counter = 0
        while not self.is_ok(result):
            result = self.generate_str()
            counter = counter + 1
            if counter >= 50:
                raise ValueError("Unable to generate " + self.name + " after 50 iterations")

        with self.write_to_file(namespace, 'w') as stream:
            stream.write(result)

        return {self.parent.name: True}

    def references(self, secret_name, value_name):
        return False


class Username(RandomString):

    CHARACTERS_INITIAL = LOWER + UPPER
    CHARACTERS_EXTRA = CHARACTERS_INITIAL + DIGITS

    def __init__(self, definition, parent):
        super(Username, self).__init__(definition, parent)
        self.initial_palette = LOWER
        if definition.get('case-sensitive', False):
            self.initial_palette = self.initial_palette + UPPER
        self.non_initial_palette = self.initial_palette
        if definition.get('digits', False):
            self.non_initial_palette = self.non_initial_palette + DIGITS

    def get_initial(self):
        return self.initial_palette

    def get_non_initial(self):
        return self.non_initial_palette

    def is_ok(self, text):
        if self.definition.get('digits', False) and not(any(s in text for s in DIGITS)):
            return False
        if self.definition.get('case-sensitive', False) and not(any(s in text for s in UPPER)):
            return False
        if not(any(s in text for s in LOWER)):
            return False
        return True


class Password(RandomString):
    def __init__(self, definition, parent):
        super(Password, self).__init__(definition, parent)

        self.palette = LOWER
        if definition.get('uppercase', False):
            self.palette = self.palette + UPPER
        if definition.get('lowercase', False):
            self.palette = self.palette + LOWER
        if definition.get('digits', False):
            self.palette = self.palette + DIGITS
        if 'special' in definition:
            self.palette = self.palette + definition['special']

        if self.palette == '':
            raise ClickException('Password ' + self.name + ' in ' + self.parent.name + ' has no characteristics')

    def get_initial(self):
        return self.palette

    def get_non_initial(self):
        return self.palette

    def is_ok(self, text):
        if self.definition.get('digits', False) and not(any(s in text for s in DIGITS)):
            return False
        if self.definition.get('uppercase', False) and not(any(s in text for s in UPPER)):
            return False
        if self.definition.get('lowercase', False) and not(any(s in text for s in LOWER)):
            return False
        if not(any(s in text for s in self.definition.get('special', ''))):
            return False
        return True
