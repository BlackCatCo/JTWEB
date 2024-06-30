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
        self.sock: socket.socket

        # self.open_connections = []

        self.cupcakes = {}

        self._active_out_data = b''
        self._active_in_data = b''
    
    def connect(self, address: str, port: int = 4242):
        '''
        Opens a connection to a given ip address and port and starts a new thread to handle the connection. Check self._connection()

        WARNING: Do not open another connection without first closing the current connection. I, Thbop, will add support for multiple connections later...

        If the application quits or the server forcibly disconnects the client, the thread and connection will automatically close.
        
        Additionally, if a user wishes to close a page, that connection/thread should be terminated via self.disconnect()
        '''
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address, port))
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
                if not self._active_in_data: break
        self.disconnect()


    