import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('localhost', 4242))


while True:
    sdata = input('> ').encode()
    sock.send(sdata)

    data = sock.recv(1024)
    if not data: break
    print('<', data.decode())

sock.close()