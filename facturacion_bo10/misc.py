def tohex(s):
    """Convert a string to hexadecimal"""
    return ''.join([hex(ord(c))[2:].zfill(2) for c in s])


