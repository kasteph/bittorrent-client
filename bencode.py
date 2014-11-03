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
    wanted_string = data[1][:length]
    remainder = data[1][length:]
    return wanted_string, remainder


def get_int(data):
    '''
    A valid bencoded integer is in the format ixe,
    where x is an integer, and i and e are the delimiters.
    '''
    assert data[0] == 'i'
    return int(data[1:data.index('e')])


def get_list(data):
    '''
    A valid bencoded list is in the format l<bencoded_vals>e,
    where l and e are the delimiters. Lists can contain any bencoded
    type.
    '''
    assert data[0] == 'l'
    return


def get_dict(data):
    pass


def bdecode(string):
    first = string[0]
    if first in '0123456789':
        wanted_string, remainder_string = get_string(string)
        return wanted_string, remainder_string
    if first == 'i':
        return get_int(string)
    if first == 'l':
        bdecoded_list = []
        for c in string:
            print(c)
            bdecoded_list.append(bdecode(string[1:]))
    if first == 'e':
        return bdecoded_list
    if first == 'd':
        bdecoded_dict = []
        bdecoded_dict.append(bdecoded_dict)
    return bdecode(string[1:])
