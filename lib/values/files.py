import os
import errno
import shutil
import tempfile


class TempDir:
    def __init__(self):
        pass

    def __enter__(self):
        self.dir = tempfile.mkdtemp()
        return self.dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.dir)


class ValueFile:
    def __init__(self, filename, mode):
        self.mode = mode
        self.filename = filename

    def __enter__(self):
        base = os.path.dirname(self.filename)
        try:
            os.makedirs(base, 0o0755)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        self.fd = open(self.filename, self.mode)
        return self.fd

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fd.close()
