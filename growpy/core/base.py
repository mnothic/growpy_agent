__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "$"
__version__ = "$"
__author__ = "theManda"


class Singleton(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class FS(object):
    _id = None
    _name = None
    _size = None
    _used = None
    _mount_on = None

    def __init__(self, name, mount_on, size, used):
        self.set_name(name)
        self.set_mount_on(mount_on)
        self.set_size(size)
        self.set_used(used)

    def set_id(self, fid):
        self._id = fid

    def get_id(self):
        return self._id

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_size(self, size):
        self._size = size

    def get_size(self):
        return self._size

    def set_used(self, used):
        self._used = used

    def get_used(self):
        return self._used

    def set_mount_on(self, mount_on):
        self._mount_on = mount_on

    def get_mount_on(self):
        return self._mount_on


class Node(object):
    _id = None
    _os = None
    _name = None
    _port = None
    _user = None
    _password = None

    def __init__(self, **kwargs):
        for key in kwargs:
            if key == 'id':
                self.setId(kwargs[key])
            if key == 'name':
                self.setName(kwargs[key])
            if key == 'osname':
                self.setOSName(kwargs[key])
            if key == 'port':
                self.setPort(kwargs[key])
            if key == 'user':
                self.setUser(kwargs[key])
            if key == 'password':
                self.setPassword(kwargs[key])

    def setId(self, node_id):
        self._id = node_id

    def getId(self):
        return self._id

    def setOSName(self, os):
        self._os = os

    def getOSName(self):
        return self._os

    def setName(self, name):
        self._name = name

    def getName(self):
        return self._name

    def setPort(self, port):
        self._port = port

    def getPort(self):
        return self._port

    def setUser(self, user):
        self._user = user

    def getUser(self):
        return self._user

    def setPassword(self, port):
        self._password = port

    def getPassword(self):
        return self._password
