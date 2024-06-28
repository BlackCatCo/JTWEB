import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connection(conn, addr):
    print(f'Connection received from {addr[0]}:{addr[1]}')
    while True:
        data = conn.recv(1024)
        conn.send(b'Hello there!')
        if not data: break
        print(data.decode())
    conn.close()


def main():
    sock.bind(('localhost', 4242))

    print('Listening')
    while True:
        sock.listen()
        conn, conn_addr = sock.accept()
        threading.Thread(target=connection,args=(conn, conn_addr), daemon=True).start() 
        

    sock.close()


if __name__ == '__main__':
    main()