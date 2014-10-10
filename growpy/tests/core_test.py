import unittest

from growpy.core.base import AESCipher
from growpy.core.base import Singleton
from growpy.core.config import config


class TestCore(unittest.TestCase):

    def test_aescipher(self):
        aes_key = 'basura'
        cipher = AESCipher(aes_key)
        mesg = "passphrase"
        secret = cipher.encrypt(mesg)
        self.assertNotEqual(mesg, secret, "must be different but are equals")
        self.assertEqual(cipher.decrypt(secret), mesg, "must be equal but are different")

    def test_singleton(self):
        a = TestSingle("A")
        b = TestSingle("C")
        b.name = "B"
        print(a.address, b.address)
        self.assertEqual(a.name, "B", "a.name must be B")
        self.assertEqual(a.address, b.address, "a is: {} and b is: {}".format(a.address, b.address))

    def test_config(self):
        pass

    def test_collector(self):
        pass

    def test_fs_exist(self):
        pass

    def test_set_fs_list(self):
        pass

    def test_config_get_by_key(self):
        self.assertEqual(config['core']['pidfile'], '/var/run/growpy.pid')


class TestSingle(metaclass=Singleton):

    def __init__(self, name=None):
        self.name = name
        self.address = hex(id(self))

