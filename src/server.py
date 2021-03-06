from cipher import xor_cypher, caesar_cypher
from random import randrange
import socket
import sys

SERVER_PORT = 5100
SERVER_ADRESS = 'localhost'

# PUBLIC_PRIME = 433494437
# PUBLIC_ROOT = 821

PUBLIC_PRIME = 99999996619
PUBLIC_ROOT = 900000547

PRIVATE_KEY = 0
PRIVATE_COMMOM_KEY = 0

def server(SERVER_PORT):

    def start():

        PRIVATE_KEY = randrange(1000,9999)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _socket:

            server_address = (SERVER_ADRESS, SERVER_PORT)
            print('starting up on %s port %s' % server_address, file=sys.stderr)
            _socket.bind(server_address)

            _socket.listen(1)
           
            print('waiting for a connection', file=sys.stderr)
            connection, client_address = _socket.accept()

            with connection:

                print('connection from', client_address, file=sys.stderr)

                public_key = PUBLIC_PRIME ** PRIVATE_KEY % PUBLIC_ROOT

                public_key = str(public_key)

                #KEY EXCHANGE
                while True:

                    data = connection.recv(256)
                    
                    if data:
                        if(data.decode('utf-8') == "ACK"):
                            break

                        print('\nReceived public key "%s" from Client' % data.decode('utf-8'), file=sys.stderr)
                    
                        print('\nSending my public key to Client "%s" ' % public_key, file=sys.stderr)

                        data = int(data.decode('utf-8'))
                        PRIVATE_COMMOM_KEY = data ** PRIVATE_KEY % PUBLIC_ROOT

                        print('SESSION TOKEN == {}'.format(PRIVATE_COMMOM_KEY))

                        connection.sendall(bytes(public_key, 'UTF-8'))
                    else:
                        print('no more data from', client_address, file=sys.stderr)
                        break
                #---------------------------------------

                #Receving cripto data 
                while True:

                    data = connection.recv(256)
                    
                    if data:

                        print('\nEncrypted message: {} '.format(data), file=sys.stderr)

                        data = data.decode('utf-8')
                        decrypted_message = xor_cypher(data, str(PRIVATE_COMMOM_KEY))
                        decrypted_message = caesar_cypher(decrypted_message, PRIVATE_COMMOM_KEY, decript=True)
                        
                        print('Decrypted message: {} \n'.format(decrypted_message), file=sys.stderr)

                        if(decrypted_message == "ACK"):
                            break

                        print('Waiting new message...')
                    # else:
                    #     print('no more data from', client_address, file=sys.stderr)
                    #     break

    return start


a = server(SERVER_PORT)
a()

# chanel = a("decrypt","hate")
# print('love xor hate = {}'.format(chanel))
# print('{} xor  hate= {}'.format(chanel, a(chanel, 'hate')))


