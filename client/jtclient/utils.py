
def unpack_str(data: bytes, start: int):
    l = int.from_bytes(data[start:start+2], 'big')
    if l == 0: return None, start+2
    return data[start+2:start+l+2].decode(), start+2+l
    
def pack_str(string: str, size_len: int=2):
    return len(string).to_bytes(size_len, 'big') + string.encode()

def pack_dict(dictionary: dict) -> bytes:
    data = ''
    for k, v in dictionary.items():
        data += k+'='+v+','
    return pack_str( data.strip(',') )

if __name__ == '__main__':
    print(pack_dict({}))

