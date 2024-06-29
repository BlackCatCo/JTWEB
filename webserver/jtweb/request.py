from .utils import *

# Class describing a client's request
class Request:
    def __init__(self, client_addr: str, client_port: int, data: bytes):
        self.client_addr = client_addr
        self.client_port = client_port
        self.client_str = f'{client_addr}:{client_port}'

        self.data = data

        i = 1 # Move along the packet data and unpack strings
        self.route, i = unpack_str(self.data, i)

        raw_cupcakes, i = unpack_str(self.data, i)
        self.cupcakes = {}
    
    def get_opcode(self) -> int:
        return self.data[0]
    
    def print_action(self, action: str):
        print(f'{self.client_str}: {action}')