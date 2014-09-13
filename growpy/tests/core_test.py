import unittest

from growpy.core.base import AESCipher
from growpy.core.base import Singleton


class TestCore(unittest.TestCase):

    def test_aescipher(self):
        print("testeando aescipher...")
        aes_key = 'basura'
        cipher = AESCipher(aes_key)
        mesg = "passphrase"
        secret = cipher.encrypt(mesg)
        print("hash of {} is: {}".format(mesg, secret))
        self.assertNotEqual(mesg, secret, "must be different but are equals")
        self.assertEqual(cipher.decrypt(secret), mesg, "must be equal but are different")

    def test_singleton(self):
        print("test singleton")
        a = TestSingle("A")
        b = TestSingle("C")
        b.name = "B"
        print(a.address, b.address)
        self.assertEqual(a.name, "B", "a.name must be B")
        self.assertEqual(a.address, b.address, "a is: {} and b is: {}".format(a.address, b.address))


class TestSingle(metaclass=Singleton):

    def __init__(self, name=None):
        self.name = name
        self.address = hex(id(self))

