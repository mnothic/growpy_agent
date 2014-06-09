__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "$"
__version__ = "$"
__author__ = "theManda"
import base64
from Crypto import Random
from Crypto.Cipher import AES


class Singleton(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class AESCipher:
    def __init__(self, key):
        self.bs = 32
        if len(key) >= 32:
            self.key = key[:32]
        else:
            self.key = self._pad(key)

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]


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
                self.set_id(kwargs[key])
            if key == 'name':
                self.set_name(kwargs[key])
            if key == 'osname':
                self.set_os(kwargs[key])
            if key == 'port':
                self.set_port(kwargs[key])
            if key == 'user':
                self.set_user(kwargs[key])
            if key == 'password':
                self.set_password(kwargs[key])

    def set_id(self, node_id):
        self._id = node_id

    def get_id(self):
        return self._id

    def set_os(self, os):
        self._os = os

    def get_os(self):
        return self._os

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def set_port(self, port):
        self._port = port

    def get_port(self):
        return self._port

    def set_user(self, user):
        self._user = user

    def get_user(self):
        return self._user

    def set_password(self, port):
        self._password = port

    def get_password(self):
        return self._password
