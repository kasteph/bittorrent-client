import bencode
import hashlib
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


def main():
    torrent = Torrent()
    print(torrent.announce_url)
    # talk to trackers!
    info_hash = hashlib.sha1(torrent.bencoded_info)
    peer_id = '-HS455BROADWAY24816-'
    left = torrent.length
    payload = {
        'info_hash': info_hash.digest(),
        'peer_id': peer_id,
        'left': left
    }
    response = requests.get(torrent.announce_url, params=payload)
    print(info_hash.digest())
    print(response, response.content)


if __name__ == '__main__':
    main()
