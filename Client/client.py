from bitarray import bitarray
import socket
import sys

SERVER_ACCESS = ('localhost', 5100)

PUBLIC_PRIME = 997
PUBLIC_ROOT = 821

PRIVATE_KEY = 404
PRIVATE_COMMOM_KEY = 0

def client(SERVER_ACCESS):


    def start():

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _socket:

            print('connecting to %s port %s' % SERVER_ACCESS, file=sys.stderr)
            _socket.connect(SERVER_ACCESS)

            public_key = PUBLIC_PRIME ** PRIVATE_KEY % PUBLIC_ROOT

            public_key = str(public_key)

            print('sending "%s"' % public_key, file=sys.stderr)
            _socket.sendall(bytes(public_key, 'utf-8'))

            while True:
                data =  _socket.recv(64)
                if data:
                    print('received "%s"' % data, file=sys.stderr)
                    data = int(data.decode('utf-8'))
                    PRIVATE_COMMOM_KEY = data ** PRIVATE_KEY % PUBLIC_ROOT
                    print('PRIVATE COMMON KEY == {}'.format(PRIVATE_COMMOM_KEY))
                    _socket.sendall(bytes('ACK', 'utf-8'))
                    break
                else:
                    break

            message = "This message has beeing encrypted"
            print('Sending message: "%s"' % message, file=sys.stderr)

            message =  xor_cypher(message, str(PRIVATE_COMMOM_KEY))
            print('Encrypted format: "%s"'% message, file=sys.stderr)
            _socket.sendall(bytes(message, 'utf-8'))
            
    
    def xor_cypher(string, key):

        def xor(bit1, bit2):
            return (bit1 + bit2) - 2*(bit1*bit2)

        if len(string) > len(key):
            key += (len(string) - len(key)) * '@'
        else:
            string += ( len(key) - len(string)) * '@'
        
        out = bitarray()

        bit_string = bitarray()
        bit_key = bitarray()

        bit_string.frombytes(string.encode('utf-8'))
        bit_key.frombytes(key.encode('utf-8'))

        for S_bit, K_bit in zip(bit_string, bit_key):
            out.append(xor(S_bit, K_bit))

        out = bitarray(out.tolist()).tobytes().decode('utf-8')

        return out

    return start

a = client(SERVER_ACCESS)
a()