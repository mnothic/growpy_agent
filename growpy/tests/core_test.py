import unittest
from growpy.core.base import AESCipher


class TestAESCipher(unittest.TestCase):

    def setUp(self):
        pass

    def test_aescipher(self):
        print("testeando aescipher...")
        aes_key = '9d8j6mfwy4n7c8!nffr'
        cipher = AESCipher(aes_key)
        mesg = "secret"
        secret = cipher.encrypt(mesg)
        self.assertNotEqual(1, 2, "must be different but are equal")
        self.assertEqual(cipher.decrypt(secret), mesg, "must be equal but are different")

if __name__ == '__main__':
    unittest.main()