import errno
import os
import shutil
import tempfile
from os.path import isfile
from subprocess import check_call

MAX_FILE_SIZE = 128*1024


class TempDir:
    def __init__(self):
        pass

    def __enter__(self):
        self.dir = tempfile.mkdtemp()
        return self.dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.dir)


class WriteToFile:
    def __init__(self, filename, mode):
        self.mode = mode
        self.filename = filename

    def __enter__(self):
        parent_dir = os.path.dirname(self.filename)
        try:
            os.makedirs(parent_dir, 0o0755)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        self.fd = open(self.filename, self.mode)
        return self.fd

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.isfile(self.filename + '.gpg'):
            check_call(["blackbox_edit_end", self.filename])
        else:
            print(["blackbox_register_new_file", self.filename])
            check_call(["sh", "-c", "blackbox_register_new_file", self.filename])
        self.fd.close()


class UpdateFile:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        parent_dir = os.path.dirname(self.filename)
        try:
            os.makedirs(parent_dir, 0o0755)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if os.path.isfile(self.filename + '.gpg'):
            check_call(["blackbox_edit_end", self.filename], shell=True)
        else:
            check_call(["sh", "-c", "blackbox_register_new_file", self.filename], shell=True)
        pass


class InspectFile:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def exists(self):
        return isfile(self.filename)


class ReadFile:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        with open(self.filename, "rb") as stream:
            self.data = stream.read(MAX_FILE_SIZE)
        return self.data

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass