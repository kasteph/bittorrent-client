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

    @property
    def info_hash_peer_id(self):
        return (self.info_hash, self.peer_id,)


class Peer(object):
    '''Represents each peer that I'm connecting to.'''

    def __init__(self, peer, info_hash_peer_id):
        self.peer = peer
        pstr = 'BitTorrent protocol'
        pstrlen = len(pstr)
        reserved = '\x00' * 8
        info_hash, peer_id = info_hash_peer_id
        self.HANDSHAKE_MESSAGE = struct.pack('B', pstrlen) + \
            pstr + reserved + info_hash + peer_id

    def handshake(self):
        S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        S.connect(self.peer)
        S.send(self.HANDSHAKE_MESSAGE)
        data = S.recv(1024)
        S.close()
        return data


def main():
    torrent = Torrent('tom.torrent')
    tracker = Tracker(torrent)
    peers = tracker.get_peers()[1:] # 0-th element is my IP and port 0
    for peer in peers:
        active_peer = Peer(peer, tracker.info_hash_peer_id)
        print(active_peer.handshake())

if __name__ == '__main__':
    main()
