import unittest
from torrent import Torrent, Tracker, Peer


class TestTorrent(unittest.TestCase):

    def setUp(self):
        self.torrent_file = 'tom.torrent'
        self.torrent = Torrent(self.torrent_file)
        self.tracker = Tracker(self.torrent)

    def test_get_torrent_info(self):
        url = 'http://thomasballinger.com:6969/announce'
        self.assertEqual(self.torrent.announce_url, url)
        self.assertEqual(self.torrent.piece_length, 16384)
        self.assertEqual(self.torrent.name, 'flag.jpg')

    @unittest.skip('s')
    def test_get_peers(self):
        # TODO write better test for this
        peers = [('74.212.183.186', 0), ('96.126.104.219', 62565)]
        self.assertEqual(self.tracker.get_peers()[:2], peers)

    def test_handshake(self):
        # check peer id is what I expected
        # check info_hash
        # handshake message should take same form as mine
        peer = self.tracker.get_peers()[1]
        peer = Peer(peer, self.tracker.info_hash_peer_id)
        self.assertEqual(self.tracker.info_hash, peer.handshake()[28:48])
