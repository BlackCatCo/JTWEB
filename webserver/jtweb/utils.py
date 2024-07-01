
def unpack_str(data: bytes, start: int):
    l = int.from_bytes(data[start:start+2], 'big')
    if l == 0: return None, start+2
    return data[start+2:start+l+2].decode(), start+2+l

def unpack_str8(data: bytes, start: int):
    l = data[start]
    if l == 0: return None, start+1 # There is no string
    return data[start+1:start+l+1].decode(), start+1+l
    
def pack_str(string: str):
    return len(string).to_bytes(2, 'big') + string.encode()

def pack_str8(string: str):
    return len(string).to_bytes(1, 'big') + string.encode()


def pack_dict(dictionary: dict) -> bytes:
    data = ''
    for k, v in dictionary.items():
        data += k+'='+v+','
    return pack_str( data.strip(',') )

# def ip_to_bytes(ip: str) -> bytes:
#     ip_b = b''
#     for i in ip.split('.'):
#         ip_b += int(i).to_bytes(1, 'big')
#     return ip_b