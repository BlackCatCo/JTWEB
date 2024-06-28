import socket
import threading


class app:
    def __init__(self):
        self.pages = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def page(self, route):
        def wrapper(pg) -> str:
            self.pages[route] = pg
            def inner(*args, **kwargs):
                return pg(*args, **kwargs)
            return inner
        return wrapper
    
    
    def connection(self, conn, addr):
        client_str = f'{addr[0]}:{addr[1]}'
        print(f'Connection received from {client_str}')
        while True:
            data = conn.recv(1024)
            try:
                sdata = self.pages[data.decode()]().encode()
            except KeyError:
                sdata = b'Not found!'
            
            conn.send(sdata)
            if not data: break
            print(f'{client_str}: {data.decode()}')
        conn.close()
    
    def run(self, address: str = 'localhost', port: int = 4242):
        self.sock.bind((address, port))
        print('Listening')
        while True:
            self.sock.listen()
            conn, conn_addr = self.sock.accept()
            threading.Thread(target=self.connection,args=(conn, conn_addr), daemon=True).start()
        
        self.sock.close()

        