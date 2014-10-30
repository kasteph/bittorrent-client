import unittest
from bencode import get_string


class TestBencode(unittest.TestCase):

    def test_get_string(self):
        self.assertEqual(get_string('4:spam'), 'spam')

    def test_get_string_error(self):
        self.assertRaises(ValueError, get_string, 'e4:bar')

    def test_get_int(self):
        self.assertEqual(get_int('i3e'), 3)

