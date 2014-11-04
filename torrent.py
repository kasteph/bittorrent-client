import bencode
import hashlib
import struct
import socket
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
        self._torrent_dict = bencode.bdecode(open(self.torrent_file).read())
        print self._torrent_dict.keys()
        self._info = self._torrent_dict['info']
        self.announce_url = self._torrent_dict['announce']
        print self.announce_url
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
        self.info_hash = hashlib.sha1(self.torrent.bencoded_info).digest()
        self.left = self.torrent.length
        payload = {
            'info_hash': self.info_hash,
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
                peer = struct.unpack_from('!BBBBH', peer_data, byte_offset)
                peers.append(peer)
                byte_offset += 6
        peers = [('.'.join(repr(i) for i in peer[0:4]), peer[4]) for peer in peers]
        return peers


def main():
    torrent = Torrent('tom.torrent')
    tracker = Tracker(torrent)
    print tracker.get_peers()[1]
    my_peer = tracker.get_peers()[1]
    # CONNECT TO PEER
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(my_peer)
    pstr = 'BitTorrent protocol'
    pstrlen = len(pstr)
    res = '\x00' * 8
    info_hash = tracker.info_hash
    peer_id = tracker.peer_id
    MESSAGE = struct.pack('B', pstrlen)+pstr+res+info_hash+peer_id
    s.send(MESSAGE)
    data = s.recv(1024)
    s.close()

    print data


if __name__ == '__main__':
    main()
