import bencode
import hashlib
import struct
import requests


class Torrent(object):
    '''
    Torrent meta-info. Not the actual data object
    to be downloaded itself.
    '''

    def __init__(self, torrent_file='tom.torrent'):
        self.torrent_file = torrent_file
        self._get_torrent_info()

    def _get_torrent_info(self):
        self._torrent_dict = bencode.bdecode(open('tom.torrent').read())
        self._info = self._torrent_dict['info']
        self.announce_url = self._torrent_dict['announce']
        self.length = self._info['length']
        self.piece_length = self._info['piece length']
        self.name = self._info['name']
        self.bencoded_info = bencode.bencode(self._info)


class Tracker(object):
    def __init__(self, torrent):
        self.torrent = torrent
        self.peer_id = '-HS455BROADWAY24816-'

    def _get_tracker_info(self):  # aka connect to tracker
        payload = self._build_payload()
        response = requests.get(self.torrent.announce_url, params=payload)
        return bencode.bdecode(response.content)

    def _build_payload(self):
        self.info_hash = hashlib.sha1(self.torrent.bencoded_info)
        self.left = self.torrent.length
        payload = {
            'info_hash': self.info_hash.digest(),
            'peer_id': self.peer_id,
            'left': self.left
        }
        return payload

    def get_peers(self):
        peer_data = self._get_tracker_info()['peers']
        byte_offset = 0
        peers = []
        if type(peer_data) == str:
            while byte_offset < len(peer_data):
                peer = struct.unpack_from('BBBBH', peer_data, byte_offset)
                peers.append(peer)
                byte_offset += 6
        peers = [('.'.join(repr(i) for i in peer[0:4]), peer[4]) for peer in peers]
        return peers


def main():
    torrent = Torrent()
    tracker = Tracker(torrent)
    print tracker.get_peers()


if __name__ == '__main__':
    main()
