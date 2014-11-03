'''
The <data> parameter in the functions below are
bencoded strings with type <str> in Python.
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
            wanted, remainder = bdecode(data)
            L.append(wanted)
            data = remainder


def get_dict(data):
    assert data[0] == 'd'
    D = {}
    data = data[1:]
    while len(data) > 0:
        assert data != ''
        if data[0] == 'e':
            return D, data[1:]
        else:
            wanted, remainder = bdecode(data)
            D[wanted], data = bdecode(remainder)


def bdecode(string):
    first = string[0]
    if first == 'l':
        return get_list(string)
    if first in '0123456789':
        return get_string(string)
    if first == 'i':
        return get_int(string)
    if first == 'd':
        return get_dict(string)
    return bdecode(string[1:])
