__copyright__ = "Copyright (C) 2013 Jorge A. Medina"
__revision__ = "1"
__version__ = "1.0"
__author__ = "theManda"
import base64
from Crypto import Random
from Crypto.Cipher import AES


# works in Python 2 & 3
class _Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})): pass



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

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]


class FS(object):

    def __init__(self, name, mount_on, size, used):
        self.name = name
        self.mount_on = mount_on
        self.size = size
        self.used = used


