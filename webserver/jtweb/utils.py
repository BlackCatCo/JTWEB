
def unpack_str(data: bytes, start: int):
    l = int.from_bytes(data[start:start+2], 'big')
    if l == 0: return None, start+2
    return data[start+2:start+l+2].decode(), start+2+l
    
def pack_str(string: str):
    return len(string).to_bytes(2, 'big') + string.encode()


def pack_dict(dictionary: dict) -> bytes:
    data = ''
    for k, v in dictionary.items():
        data += k+'='+v+','
    return pack_str( data.strip(',') )