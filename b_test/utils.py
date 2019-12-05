letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def numtoletter(n : int):
    """
    Converts an interger to a letter
    """
    if 0 < n <= 26:
        return chr(n + 65)
    else:
        return ''
def lettertonum(c : str):
    """
    converts a letter to an integer
    """
    c = c.upper()
    if len(c) == 1 and c in letters:
        return ord(c) - 65
    else:
        return 0