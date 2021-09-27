from random import randrange
from cipher import xor_cypher, caesar_cypher
import socket
import sys

SERVER_ACCESS = ('localhost', 5100)

PUBLIC_PRIME = 99999996619
PUBLIC_ROOT = 900000547

PRIVATE_KEY = 0
PRIVATE_COMMOM_KEY = 0

def client(SERVER_ACCESS):

    def start():

        PRIVATE_KEY = randrange(1000,9999)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _socket:

            print('connecting to %s port: %s' % SERVER_ACCESS, file=sys.stderr)
            _socket.connect(SERVER_ACCESS)

            public_key = PUBLIC_PRIME ** PRIVATE_KEY % PUBLIC_ROOT

            public_key = str(public_key)

            print('\nSending public key to server "%s"' % public_key, file=sys.stderr)
            _socket.sendall(bytes(public_key, 'utf-8'))

            while True:
                data =  _socket.recv(256)
                if data:

                    print('\nReceived server public key "%s"' % data.decode('utf-8'), file=sys.stderr)

                    data = int(data.decode('utf-8'))
                    PRIVATE_COMMOM_KEY = data ** PRIVATE_KEY % PUBLIC_ROOT

                    print('\nSESSION TOKEN == {}'.format(PRIVATE_COMMOM_KEY))

                    _socket.sendall(bytes('ACK', 'utf-8'))

                    break
                else:
                    break

            print("\n\n\n")
    
            while True:
                message = input("\nType 256 CHAR message: ")
                
                if(len(message) > 256):
                    continue
                
                if(message == 'EXIT'):
                    break

                print('\nSending message: "%s"' % message, file=sys.stderr)

                message = caesar_cypher(message, PRIVATE_COMMOM_KEY)
                message = xor_cypher(message, str(PRIVATE_COMMOM_KEY))

                print('Encrypted format: "%s"'% message, file=sys.stderr)

                _socket.sendall(bytes(message, 'utf-8'))


    return start

a = client(SERVER_ACCESS)
a()