from math import ceil

from .utils import *


class Response:
    '''
    Models a response to the client
    '''
    def __init__(self):
        '''
        Initializes the response
        '''
        self.error_code = 2 # Success
        self.opcode: int

        self.data: str # Will be converted into chunks
        self.cupcakes = {}

        self.dns_data = {}

    def dns(self):
        '''
        Package into a proper DNS response and return packet bytes
        '''

        return (
            b'\x01'                                  +
            self.error_code.to_bytes(1, 'big')       +
            pack_str8( self.dns_data['address'] )     +
            self.dns_data['port'].to_bytes(2, 'big')
        )

    def chunkify(self): # -> ChunkyMilk
        '''
        Chunky milk: https://youtu.be/k0hKMDMWYwU?si=Vi5Vvu9aKSddxDs0&t=7

        Does some math and hopefully divides the reponse packets into chunks, returning the chunks.
        '''
        raw_cupcakes = pack_dict(self.cupcakes)

        guess_len: int = ceil(( len(self.data) + len(raw_cupcakes) ) / 1024)
        l: int = len(self.data) + 8*guess_len + len(raw_cupcakes) # 8 = len(opcode) + len(error_code) + len(chunk_count) + len(chunk_id) + len(data_str_len_indicator); required for each chunk
        chunk_count: int = ceil(l / 1024) # Rounds up

        if chunk_count > 0xFFFF: # Content length exceeds 0xFFFF * 1024 = 67,107,840 characters/bytes
            self.error_code = 5
            return [
                self.opcode.to_bytes(1, 'big') +
                self.error_code.to_bytes(1, 'big') + 
                b'\x00\x01\x00\x00' + 
                pack_str('Server send you too big file (equal to or greater than ~67 megabytes). S-s-sorry!') +
                '\x00\x00'
            ]
            
        data_len = 1024-8-len(raw_cupcakes) # Data per chunk length, subtracting metadata and cupcakes
        chunks = [ 
            self.opcode.to_bytes(1, 'big')                   + # Your eyes are not deceiving you, this is a column of plus signs
            self.error_code.to_bytes(1, 'big')               + 
            l.to_bytes(2, 'big')                             + 
            i.to_bytes(2, 'big')                             +
            pack_str( self.data[i*data_len:(i+1)*data_len] ) +
            raw_cupcakes
            for i in range(chunk_count)
        ]

        return chunks