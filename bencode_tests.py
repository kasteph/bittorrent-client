import unittest
from bencode import get_string, get_int, get_list


class TestBencode(unittest.TestCase):

    def test_get_string(self):
        self.assertEqual(get_string('4:spam'), ('spam', ''))
        self.assertEqual(get_string('6:foobar'), ('foobar', ''))
        self.assertEqual(get_string('5:hello3:heyi23e'), ('hello', '3:heyi23e'))
        self.assertEqual(get_string('3:foobaz:i4e'), ('foo', 'baz:i4e'))

    def test_get_string_error(self):
        self.assertRaises(ValueError, get_string, 'e3:bar')

    def test_get_int(self):
        self.assertEqual(get_int('i3e'), 3)
        self.assertEqual(get_int('i-3e'), -3)
        self.assertEqual(get_int('i04e'), 4)
        self.assertEqual(get_int('i0e'), 0)

    def test_get_list(self):
        self.assertEqual(get_list('l4:spam4:eggse'), ['spam', 'eggs'])