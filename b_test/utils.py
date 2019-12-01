letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def numtoletter(n : int):
    if 0 < n <= 26:
        return chr(n + 64)
    else:
        return ''
def lettertonum(c : str):
    c = c.upper()
    if len(c) == 1 and c in letters:
        return ord(c) - 64
    else:
        return 0