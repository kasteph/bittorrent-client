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
    return int(data[1:data.index('e')])


def get_list(data):
    '''
    A valid bencoded list is in the format l<bencoded_vals>e,
    where l and e are the delimiters. Lists can contain any bencoded
    type.
    '''
    pass
