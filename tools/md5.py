import hashlib

def md5(str):

    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))

    return hl.hexdigest()