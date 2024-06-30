import socket
import threading

from .utils import *

class app:
    def __init__(self):
        self.sock: socket.socket # Server socket

        self.cupcakes = {}

        self._active_out_data = b''
        self._active_in_data = b''
    
    def connect(self, address: str, port: int = 4242):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((address, port))
        threading.Thread(target=self._connection,args=(), daemon=True).start()
    
    def disconnect(self):
        self.sock.close()
    
    def request(self, route: str, method: str='FETCH', input_data: dict = {}):
        '''
        Let route be the /resource/path/ the user wants to access

        And method be either `"FETCH"` or `"PUT"`
        '''
        self._active_out_data = (
            (b'\x02' if method == 'FETCH' else b'\x03')           +
            pack_str(route)                                       +
            (b'' if method == 'FETCH' else pack_dict(input_data)) +
            pack_dict( self.cupcakes )
        )
    
    def get_incoming_text(self): # Assuming only one chunk
        return unpack_str(self._active_in_data, 6)[0]


    def _connection(self):
        while True:
            if self._active_out_data:
                self.sock.send(self._active_out_data)
                self._active_out_data = b''

                self._active_in_data = self.sock.recv(1024) # Assuming only one chunk
                if not self._active_in_data: break
        self.disconnect()


    