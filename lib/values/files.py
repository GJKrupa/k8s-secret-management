import errno
import os
import shutil
import tempfile
from os.path import isfile
from subprocess import check_output

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
        self.fd.close()
        if os.path.isfile(self.filename + '.gpg'):
            check_output(["sh", "-c", "blackbox_edit_end " + self.filename])
        else:
            check_output(["sh", "-c", "blackbox_register_new_file " + self.filename])


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
            check_output(["sh", "-c", "blackbox_edit_end " + self.filename])
        else:
            check_output(["sh", "-c", "blackbox_register_new_file " + self.filename])
        pass


class InspectFile:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def exists(self):
        return isfile(self.filename + ".gpg")


class ReadFile:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        check_output(["sh", "-c", "blackbox_edit_start " + self.filename])
        with open(self.filename, "rb") as stream:
            self.data = stream.read(MAX_FILE_SIZE)
        return self.data

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove(self.filename)
