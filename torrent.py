import bencode
import hashlib
import struct
import socket
import requests


class Torrent(object):
    def __init__(self, torrent_file='tom.torrent'):
        '''
        Torrent meta-info. Not the actual data object
        to be downloaded itself.
        '''
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
        '''
        Tracker(torrent) -> <torrent> is a Torrent object.
        Contains tracker information, and gets peers.
        '''
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
        '''
        Get the list of peers (a tuple of IP and port) in a swarm.
        '''
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
    def __init__(self, peer, info_hash_peer_id):
        '''
        Peer(peer, info_hash_peer_id) -> <peer> is a tuple
        of (IP address, port). <info_hash_peer_id> is a tuple of
        (info_hash, peer_id) and can be obtained from the Torrent
        object.

        Represents each peer that I'm connecting to.'''
        self.peer = peer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        pstr = 'BitTorrent protocol'
        pstrlen = len(pstr)
        reserved = '\x00' * 8
        info_hash, peer_id = info_hash_peer_id
        self.HANDSHAKE_MESSAGE = struct.pack('B', pstrlen) + \
            pstr + reserved + info_hash + peer_id

    def connect(self):
        self.socket.connect(self.peer)

    def handshake(self):
        self.socket.send(self.HANDSHAKE_MESSAGE)
        data = self.socket.recv(1024)
        more_data = self.socket.recv(1024)
        self.socket.close()
        return data, more_data

    def get_new_message(self):
        self.socket.connect()

def main():
    torrent = Torrent('tom.torrent')
    tracker = Tracker(torrent)
    peer = tracker.get_peers()[1]  # 0-th element is my IP and port 0
    active_peer = Peer(peer, tracker.info_hash_peer_id)
    active_peer.connect()
    print(active_peer.handshake())

if __name__ == '__main__':
    main()
