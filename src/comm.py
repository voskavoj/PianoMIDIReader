# API
class Comm:
    def __init__(self):
        pass

    def setup(self, *args):
        raise NotImplementedError

    def open(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def is_available(self):
        raise NotImplementedError

    def number_available(self):
        raise NotImplementedError

    def read(self, number=None):
        raise NotImplementedError
