import random


def stoi(mes):
    r = 0
    for c in mes:
        r = (r << 8) + ord(c)
    return r

def itos(mes):
    n = int(mes)
    str = ""
    while n > 0:
        str = chr(n % 256) + str
        n >>= 8
    return str


def dec_to(n, private_key = None):
    base_list = [chr(i) for i in (list(range(33, 47)) + list(range(58, 127))) if i not in [34, 39, 43, 92, 96]]
    if private_key is None:
        raise ValueError("Miss private key!")
    else:
        base = min(len(base_list), stoi(private_key) % 100)

    base_crypt = ''
    c = random.choice(base_list)
    while len(base_crypt) < base:
        if c not in base_crypt:
            base_crypt += c
        c = random.choice(base_list)
    ans = ''
    while n > 0:
        ans = base_crypt[n % base] + ans
        n //= base
    pos = 0
    for c in str(stoi(f"{base_crypt}{base}") + stoi(private_key)):
        pos = random.choice(list(range(pos + 1, pos + 5 + pos % 5)))
        ans = ans[:pos] + c + ans[pos:]
    return ans


def to_dec(s, private_key = None):
    if private_key is None:
        raise ValueError("Miss private key!")
    try:
        de_base = ''
        for c in s:
            if 48 <= ord(c) <= 57:
                de_base += c
        de_base = itos(int(de_base) - stoi(private_key))
        if 48 <= ord(de_base[-2]) <= 57:
            base_crypt = de_base[:-2]
            base = int(de_base[-2:])
        else:
            base_crypt = de_base[:-1]
            base = int(de_base[-1])
        n = 0
        for c in s:
            if c in base_crypt:
                n = n * base + base_crypt.index(c)
        return n
    except:
        return 0


def encrypt(mes, private_key = None):
    return dec_to(stoi(mes), private_key)


def decrypt(mes, private_key):
    if len(itos(to_dec(mes, private_key))) == 0:
        return "Error password!"
    else:
        return itos(to_dec(mes, private_key))
