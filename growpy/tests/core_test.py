import unittest
from growpy.core.base import AESCipher
from growpy.core.base import Singleton


class TestAESCipher(unittest.TestCase):

    def test_aescipher(self):
        print("testeando aescipher...")
        aes_key = '9d8j6mfwy4n7c8!nffr'
        cipher = AESCipher(aes_key)
        mesg = "secret"
        secret = cipher.encrypt(mesg)
        print("hash of {} is: {}".format(mesg, secret))
        self.assertNotEqual(mesg, secret, "must be different but are equals")
        self.assertEqual(cipher.decrypt(secret), mesg, "must be equal but are different")


class TestSingle(Singleton):
    def __init__(self, name):
        self.name = name
        self.address = hex(id(self))


class TestSingleton(unittest.TestCase):

    def test_singleton(self):
        print("test singleton")
        a = TestSingle()
        b = TestSingle()
        b.name = "B"
        print(a.address, b.address)
        self.assertEqual(a.name, "B", "a.name must be B")
        self.assertEqual(a.address, b.address, "a is: {} and b is: {}".format(a.address,b.address))