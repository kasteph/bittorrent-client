import unittest
from torrent import Torrent


class TestTorrent(unittest.TestCase):

    def setUp(self):
        self.torrent_file = open('tom.torrent').read()
        self.torrent = Torrent(self.torrent_file)

    def test_get_torrent_info(self):
        self.assertEqual(self.torrent.announce_url, 'http://thomasballinger.com:6969/announce')
        self.assertEqual(self.torrent.piece_length, 16384)
