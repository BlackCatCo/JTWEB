import socket
import threading

from .utils import *

class app:
    '''
    Defines the interface that communicates with a valid jtweb server.
    '''
    def __init__(self):
        '''
        Initializes the app interface
        '''
        self.sock: socket.socket = None


        # self.open_connections = []

        self.cupcakes = {}

        self._active_out_data = b''
        self._active_in_data = b''
        self._new_in = False

        self._dns_active_out_data = b''
        self._dns_active_in_data = b''
        self._dns_new_in = False
    
    def setup_dns(self, dns_server_address: str, dns_server_port: int):
        '''
        Sets up and enables use of a socket to communicate with the chosen DNS server and port
        '''
        self.dns_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.dns_sock.connect((dns_server_address, dns_server_port))
        threading.Thread(target=self._dns_connection,args=(), daemon=True).start()
    
    def _dns_connection(self):
        '''
        Handles a dns connection, this should only be run in a thread.
        '''

        while True:
            if self._dns_active_out_data:
                self.dns_sock.send(self._dns_active_out_data)
                self._dns_active_out_data = b''

                self._dns_active_in_data = self.dns_sock.recv(1024)
                self._dns_new_in = True
                if not self._dns_active_in_data: break
        self.dns_sock.close()

    def dns_request(self, domain: str):
        self._dns_active_out_data = b'\x01' + pack_str8(domain)
    
    def get_incoming_dns(self):
        while not self._dns_new_in: pass
        self._dns_new_in = False

        domain, i = unpack_str8(self._dns_active_in_data, 2)
        ip = int.from_bytes(self._dns_active_in_data[i:i+2], 'big')


        return domain, ip
    
    def connect(self, address: str):
        '''
        Uses DNS to look up a domain, receive ip and port, and start a new thread to handle the connection. Check self._connection()

        WARNING: Do not open another connection without first closing the current connection. I, Thbop, will add support for multiple connections later...

        If the application quits or the server forcibly disconnects the client, the thread and connection will automatically close.
        
        Additionally, if a user wishes to close a page, that connection/thread should be terminated via self.disconnect()
        '''
        self.dns_request(address)
        ip, port = self.get_incoming_dns()

        # print(f'Connecting to {ip}:{port}')

        if self.sock: self.sock.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        threading.Thread(target=self._connection,args=(), daemon=True).start()
        # self.open_connections.append((address, port))

    
    def disconnect(self):
        '''
        Disconnects the current connection.
        '''
        self.sock.close()
    
    def request(self, route: str, method: str='FETCH', input_data: dict = {}):
        '''
        Let route be the /resource/path/ the user wants to access

        And method be either `"FETCH"` or `"PUT"`

        Using the current open connection, this FETCHes / PUTs data at a specific route on the server (bad explanation).
        '''
        self._active_out_data = (
            (b'\x02' if method == 'FETCH' else b'\x03')           +
            pack_str(route)                                       +
            (b'' if method == 'FETCH' else pack_dict(input_data)) +
            pack_dict( self.cupcakes )
        )
    
    def get_incoming_text(self) -> str: # Assuming only one chunk
        '''
        After a request, this returns a string containing the plaintext that will be parsed and rendered by JWEB.
        '''
        while not self._new_in: pass
        self._new_in = False
        return unpack_str(self._active_in_data, 6)[0]


    def _connection(self):
        '''
        Handles a connection, this should only be run in a thread.
        '''

        while True:
            if self._active_out_data:
                self.sock.send(self._active_out_data)
                self._active_out_data = b''

                self._active_in_data = self.sock.recv(1024) # Assuming only one chunk
                self._new_in = True
                if not self._active_in_data: break
        self.disconnect()


    