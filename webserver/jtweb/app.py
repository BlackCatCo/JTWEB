import socket
import threading
import json


from .utils import *
from .request import *
from .response import *


class app:
    '''
    Defines the server application interface
    '''
    def __init__(self):
        '''
        Initializes the app interface
        '''
        self.pages = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.dns_enabled = False
        self.domains: list
    
    def setup_dns(self, enable: bool=True, dns_path: str='domains.json'):
        '''
        Will this webserver also act as a DNS server?

        dns_path points to a json file of the format:
        ```json
        [
            {
                "domain":"thbop.code",
                "address:"127.0.0.1",
                "port":4242
            }
        ]
        ```
        '''
        self.dns_enabled = enable
        with open(dns_path) as f:
            self.domains = json.load(f)


    def page(self, route: str):
        '''
        Defines a page decorator accepting the route supplied.

        Example:
        ```py
        @app.page('blogs/coolcodes/')
        def codes():
            return 'codes'
        ```
        '''
        def wrapper(pg) -> str:
            self.pages[route] = pg
            def inner(*args, **kwargs):
                return pg(*args, **kwargs)
            return inner
        return wrapper
    
    
    def _connection(self, conn, addr):
        '''
        Handles a single connection started by a thread and reponds via `self.process_packet()`
        '''

        client_str = f'{addr[0]}:{addr[1]}'
        print(f'Connection received from {client_str}')
        while True:
            try:
                data = conn.recv(1024)
                if not data: break
            except ConnectionResetError:
                break
            
            req = Request(addr[0], addr[1], data)
            res = self.process_packet(req)
            if self.dns_enabled and req.get_opcode() == 1:
                conn.send(res.dns())
            else:
                for c in res.chunkify():
                    conn.send(c)
            # print(f'{client_str}: {data.decode()}')
        print(f'{client_str} disconnected')
        conn.close()
    


    # Takes in raw client -> server packet and returns chunks to send back to client
    def process_packet(self, req: Request) -> Response:
        '''
        Takes in a `Reqest` object, processes it, and returns the appropriate `Response` object.
        '''
        res = Response() # Will be passed into the page function
        res.opcode = req.get_opcode() # Set return opcode... hopefully it's valid :)

        if self.dns_enabled and req.get_opcode() == 1: # DNS Server request
            res.error_code = 1
            req_domain = unpack_str8(req.data, 1)[0]
            req.print_action(f'Requests {req_domain}')
            if req_domain:
                for d in self.domains:
                    if d['domain'] == req_domain:
                        res.dns_data = d
                        res.error_code = 2

        elif req.get_opcode() == 2: # Fetch request
            if req.route == None:
                res.error_code = 3
                res.data = 'You dun did it now! Error 3' # Probably only technical users (aspiring exploiters) could get this message
            else:
                req.print_action(req.route)
            
                try:
                    res.data = self.pages[req.route]()
                except KeyError:
                    res.data = 'Error 4'
                    res.error_code = 4
        else:
            res.error_code = 0
            res.data = 'You dun did it now! Error 0'
            # Maybe do some other stuff...
        return res

    
    def run(self, address: str = 'localhost', port: int = 4242):
        '''
        Runs the application
        '''

        self.sock.bind((address, port))
        print('Listening')
        while True:
            self.sock.listen()
            conn, conn_addr = self.sock.accept()
            threading.Thread(target=self._connection,args=(conn, conn_addr), daemon=True).start()
        
        self.sock.close()

        