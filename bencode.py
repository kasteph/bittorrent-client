isa = isinstance


def get_string(data):
    '''
    Where [data] is a string. A valid bencoded
    string is in the format of x:y, where x is
    an int and y the contents of the string.

    get_string assumes that if the first element
    of data cannot be type converted into an int,
    then it is not a valid bencoded string.
    '''
    data = data.split(':')
    try:
        data[0] = int(data[0])
    except ValueError:
        raise ValueError('Not a valid bencoded string.')
    return data[1]