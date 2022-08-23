# API
class Comm:
    def __init__(self):
        pass

    def setup(self, *args):
        raise NotImplementedError

    def open(self, *args):
        raise NotImplementedError

    def close(self, *args):
        raise NotImplementedError

    def is_available(self, *args):
        raise NotImplementedError

    def number_available(self, *args):
        raise NotImplementedError

    def read(self, *args):
        raise NotImplementedError
