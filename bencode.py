'''
The <data> parameter in the functions below are
bencoded strings with type <str> in Python.

The bencode function is Tom's. See:
https://github.com/thomasballinger/bittorrent/blob/master/bittorrent/bencode.py
'''


def get_string(data):
    '''
    A valid bencoded string is in the format of x:y,
    where x is an int and y the contents of the string.

    get_string assumes that if the first element
    of data cannot be type converted into an int,
    then it is not a valid bencoded string.
    '''
    data = data.split(':', 1)
    try:
        length = int(data[0])
        assert isinstance(length, int)
    except ValueError:
        raise ValueError('Not a valid bencoded string.')
    wanted = data[1][:length]
    remainder = data[1][length:]
    return wanted, remainder


def get_int(data):
    '''
    A valid bencoded integer is in the format ixe,
    where x is an integer, and i and e are the delimiters.
    '''
    assert data[0] == 'i'
    wanted = int(data[1:data.index('e')])
    remainder = data[data.index('e') + 1:]
    return wanted, remainder


def get_list(data):
    '''
    A valid bencoded list is in the format l<bencoded_vals>e,
    where l and e are the delimiters. Lists can contain any bencoded
    type.
    '''
    assert data[0] == 'l'
    L = []
    data = data[1:]
    while len(data) > 0:
        assert data != ''
        if data[0] == 'e':
            return L, data[1:]
        else:
            wanted, remainder = _bdecode_helper(data)
            L.append(wanted)
            data = remainder


def get_dict(data):
    '''
    A valid bencoded dict is in the format d<bencoded_vals>e,
    where d and e are the delimiters. Only strings may be keys
    but values can be any bencoded type.
    '''
    assert data[0] == 'd'
    D = {}
    data = data[1:]
    while len(data) > 0:
        assert data != ''
        if data[0] == 'e':
            return D, data[1:]
        else:
            wanted, remainder = _bdecode_helper(data)
            D[wanted], data = _bdecode_helper(remainder)


def bdecode(string):
    '''
    bdecode(string) -> string is a bencoded string of
    type <str>.
    Decode bencoded strings. Returns the decoded value
    in its corresponding Python type.
    '''
    wanted, remainder = _bdecode_helper(string)
    assert remainder == ''
    return wanted


def _bdecode_helper(string):
    '''
    _bdecode_helper(string) -> string is a bencoded string of
    type <str>. 
    Returns a tuple of the decoded values and a remainder.
    '''
    first = string[0]
    if first == 'l':
        return get_list(string)
    if first in '0123456789':
        return get_string(string)
    if first == 'i':
        return get_int(string)
    if first == 'd':
        return get_dict(string)
    return _bdecode_helper(string[1:])


encodings = {
    dict : lambda x: 'd'+''.join([bencode(str(k))+bencode(v) for k,v in sorted(x.items(), key=lambda kv: kv[0])])+'e',
    list : lambda x: 'l'+''.join([bencode(el) for el in x])+'e',
    str :  lambda x: str(len(x))+':'+x,
    int :  lambda x: 'i'+str(x)+'e'
}


def bencode(string):
    '''
    Doesn't reject invalid data structures very well
    >>> bencode({'e':3})
    'd1:ei3ee'
    >>> d = {'a': 1, 'b': [2,3,'asdf'], 'cdef': {'qwerty':4}}
    >>> bencode(d)
    'd1:ai1e1:bli2ei3e4:asdfe4:cdefd6:qwertyi4eee'
    '''
    return encodings[type(string)](string)
