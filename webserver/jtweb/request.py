from .utils import *

class Request:
    '''
    Class describing a client's request
    '''
    def __init__(self, client_addr: str, client_port: int, data: bytes):
        '''
        Initializes the request and unpacks the requested route and served cupcakes
        '''
        self.client_addr = client_addr
        self.client_port = client_port
        self.client_str = f'{client_addr}:{client_port}'

        self.data = data

        i = 1 # Move along the packet data and unpack strings
        self.route, i = unpack_str(self.data, i)

        raw_cupcakes, i = unpack_str(self.data, i) # Currently doesn't fully unpack the yummy cupcakes
        self.cupcakes = {}
    
    def get_opcode(self) -> int:
        '''
        Returns the request opcode
        '''
        return self.data[0]
    
    def print_action(self, action: str):
        '''
        Prints an action on behalf of the current request with the format of:

        ip:port: action

        or

        127.0.0.1:35456: /I/eat/cheese
        '''
        print(f'{self.client_str}: {action}')