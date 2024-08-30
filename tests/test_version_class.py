import unittest

from versionlib.versions import Version


class TestVersionClass(unittest.TestCase):

    def test_correct_versions(self):
        a = Version("3.12.1.5.12")
        b = Version("3.12.1.5.06.1")
        self.assertTrue(a > b)
        self.assertTrue(a >= b)
        self.assertTrue(a != b)

        x = Version("3.12.1.5.12")
        y = Version("3.12.1.5.12.5")
        self.assertTrue(x < y)
        self.assertTrue(x <= y)
        self.assertTrue(x != y)

        c = Version("3.12.1.5")
        d = Version("3.12.1.5")
        self.assertTrue(c == d)
        self.assertTrue(c >= d)
        self.assertTrue(c <= d)

        e = Version("3.12.1.5.0")
        f = Version("3.12.1.5")
        self.assertTrue(e == f)
        self.assertTrue(e >= f)
        self.assertTrue(e <= f)

    def test_incorrect_versions(self):
        with self.assertRaises(TypeError):
            _ = Version(1.2)
        
        with self.assertRaises(ValueError):
            _ = Version("")

        with self.assertRaises(ValueError):
            _ = Version(" ")

        with self.assertRaises(ValueError):
            _ = Version("1.2.")

        with self.assertRaises(ValueError):
            _ = Version(".1.2")

