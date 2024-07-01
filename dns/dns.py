import socket
import threading
import json

# import os
# os.chdir(os.path.dirname(__file__))

def ip_to_bytes(ip: str) -> bytes:
    ip_b = b''
    for i in ip.split('.'):
        ip_b += int(i).to_bytes(1, 'big')
    return ip_b

def unpack_str(data: bytes, start: int):
    l = data[start]
    if l == 0: return None, start+1 # There is no string
    return data[start+1:start+l+1].decode(), start+2+l

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



with open('domains.json') as f:
    domains = json.load(f)


def process_packet(data: bytes) -> bytes:
    error_code = 1
    ip = b'\x00\x00\x00\x00' # NULL ip
    port = 0
    if data[0] == 1: # Proper DNS Request opcode
        req_domain = unpack_str(data, 1)[0]
        if req_domain:
            for d in domains:
                if d['domain'] == req_domain:
                    address = ip_to_bytes(d['address'])
                    port = d['port']
                    error_code = 2
    else:
        error_code = 0

    return b'\x01' + error_code.to_bytes(1, 'big') + address + port.to_bytes(2, 'big')

def connection(conn, addr):
    print(f'Connection received from {addr[0]}:{addr[1]}')
    while True:
        data = conn.recv(1024)
        if not data: break
        conn.send(process_packet(data))
        # print(data.decode())
    conn.close()


def main():
    sock.bind(('localhost', 4545)) # Gotta add this to the documentation

    print('Listening')
    while True:
        sock.listen()
        conn, conn_addr = sock.accept()
        threading.Thread(target=connection,args=(conn, conn_addr), daemon=True).start() 
        

    sock.close()


if __name__ == '__main__':
    main()
    # print(unpack_str(b'\x04Hello World!', 0))