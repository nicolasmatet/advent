from abc import abstractmethod


class LineType(type):
    @classmethod
    @abstractmethod
    def content(cls):
        pass

    def __str__(mcs):
        return mcs.content()


class EmptyLine(metaclass=LineType):
    @classmethod
    def content(cls):
        return '~~ EMPTY LINE ~~'


class FileIterator:
    def __init__(self, file):
        self.file = file

    def __iter__(self):
        return self

    def __next__(self):
        next_row = next(self.file).replace('\n', '')
        if next_row:
            return next_row
        else:
            return EmptyLine


class FileReader:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename)
        return FileIterator(self.file)

    def __exit__(self, type, value, traceback):
        self.file.close()


def read_file(filename):
    return FileReader(filename)
