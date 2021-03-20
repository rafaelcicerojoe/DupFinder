class File:
    def __init__(self, name, path, full_path, size, time, hash_id=""):
        self._name = name
        self._path = path
        self._full_path = full_path
        self._size = size
        self._time = time
        self._hash_id = hash_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def full_path(self):
        return self._full_path

    @full_path.setter
    def full_path(self, value):
        self._full_path = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    @property
    def hash_id(self):
        return self._hash_id

    @hash_id.setter
    def hash_id(self, value):
        self._hash_id = value

    def __str__(self):
        return "{}".format(self._name)

    def __repr__(self):
        return "{}".format(self._name)
