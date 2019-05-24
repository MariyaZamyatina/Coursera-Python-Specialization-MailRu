import tempfile
import os
import uuid


class File:

    def __init__(self, file_name):
        self.file_name = file_name
        self._current = 0

        with open(self.file_name, 'a') as fd:
            pass

    def __str__(self):
        return self.file_name

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.file_name, 'r') as fd:
            fd.seek(self._current)
            result = fd.readline()

            if not result:
                self._current = 0
                raise StopIteration()

            self._current = fd.tell()
        return result

    def write(self, text):
        with open(self.file_name, 'a') as fd:
            fd.write(text)

    def __add__(self, other):
        temp_file = os.path.join(tempfile.gettempdir(), str(uuid.uuid4().hex))
        new_file = File(temp_file)

        for line in self:
            new_file.write(line)
        for line in other:
            new_file.write(line)

        return new_file


