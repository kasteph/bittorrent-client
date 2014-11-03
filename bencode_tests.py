import unittest
from bencode import get_string, get_int, get_list, get_dict, bdecode


class TestBencode(unittest.TestCase):

    def test_get_string(self):
        self.assertEqual(get_string('4:spam'), ('spam', ''))
        self.assertEqual(get_string('6:foobar'), ('foobar', ''))
        self.assertEqual(get_string('5:hello3:heyi2e'), ('hello', '3:heyi2e'))
        self.assertEqual(get_string('3:foobaz:i4e'), ('foo', 'baz:i4e'))

    def test_get_string_error(self):
        self.assertRaises(ValueError, get_string, 'e3:bar')

    def test_get_int(self):
        self.assertEqual(get_int('i3e'), (3, ''))
        self.assertEqual(get_int('i-3e'), (-3, ''))
        self.assertEqual(get_int('i04e'), (4, ''))
        self.assertEqual(get_int('i0e'), (0, ''))

    def test_get_list(self):
        self.assertEqual(get_list('l4:spam4:eggse'), (['spam', 'eggs'], ''))
        self.assertEqual(get_list('l4:spam4:eggsi42ee'), (['spam', 'eggs', 42], ''))
        self.assertEqual(get_list('li1ei2ei3ee'), ([1, 2, 3], ''))
        self.assertEqual(get_list('li1eli2eee'), ([1, [2]], ''))
        self.assertEqual(get_list('le'), ([], ''))
        self.assertEqual(get_list('ld3:cow3:moo4:spam4:eggsee'), ([{'cow': 'moo', 'spam': 'eggs'}], ''))

    def test_get_dict(self):
        self.assertEqual(get_dict('d3:cow3:moo4:spam4:eggse'), ({'cow': 'moo', 'spam': 'eggs'}, ''))
        self.assertEqual(get_dict('d3:cow3:moo4:spaml3:foo3:baree'), ({'cow': 'moo', 'spam': ['foo', 'bar']}, ''))
        self.assertEqual(get_dict('de'), ({}, ''))
        self.assertEqual(get_dict('d1:ai1ee'), ({'a': 1}, ''))
