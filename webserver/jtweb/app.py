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
            try:
                data = conn.recv(1024)
                if not data: break
            except ConnectionResetError:
                break
            
            chunks = self.process_packet(client_str, data)
            for c in chunks:
                conn.send(c)
            # print(f'{client_str}: {data.decode()}')
        print(f'{client_str} disconnected!')
        conn.close()
    
    def _unpack_str(self, data: bytes, start: int):
        l = int.from_bytes(data[start:start+2], 'little')
        if l == 0: return None, start+2
        return data[start+2:start+l+2].decode(), start+2+l
    
    def _pack_str(self, string: str):
        return len(string).to_bytes(2, 'little') + string.encode() # Might want to change to big


    # Takes in raw client -> server packet and returns chunks to send back to client
    def process_packet(self, client_str: str, data: bytes) -> list:
        print(data)
        if data[0] == 2: # Fetch request
            route, i = self._unpack_str(data, 1)
            cupcakes, i = self._unpack_str(data, i)
            if route == None:
                pass # Error, invalid resource
            else:
                print(f'{client_str}: {route}')
            
            try:
                res = self.pages[route]()
            except KeyError:
                res = 'Error'

        return [self._pack_str(res)]

    
    def run(self, address: str = 'localhost', port: int = 4242):
        self.sock.bind((address, port))
        print('Listening')
        while True:
            self.sock.listen()
            conn, conn_addr = self.sock.accept()
            threading.Thread(target=self.connection,args=(conn, conn_addr), daemon=True).start()
        
        self.sock.close()

        