import asyncio
import socket


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 4242))
print('Listening')
sock.listen()
conn, conn_addr = sock.accept()
print(f'Connection received from {conn_addr[0]}:{conn_addr[1]}')
while True:
    data = conn.recv(1024)
    conn.send(b'Hello there!')
    if not data: break
    print(data.decode())
conn.close()

sock.close()