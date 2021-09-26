from bitarray import bitarray
import socket
import sys

SERVER_PORT = 5100
SERVER_ADRESS = 'localhost'

PUBLIC_PRIME = 997
PUBLIC_ROOT = 821

PRIVATE_KEY = 505
PRIVATE_COMMOM_KEY = 0

def server(SERVER_PORT):

    def start():

        #GEnerate private key

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

                    data = connection.recv(64)
                    
                    if data:
                        if(data.decode('utf-8') == "ACK"):
                            break

                        print('Received public key "%s" from Bob' % data, file=sys.stderr)
                    
                        print('Sending my public key to Bob', file=sys.stderr)

                        data = int(data.decode('utf-8'))
                        PRIVATE_COMMOM_KEY = data ** PRIVATE_KEY % PUBLIC_ROOT

                        print('PRIVATE COMMON KEY == {}'.format(PRIVATE_COMMOM_KEY))

                        connection.sendall(bytes(public_key, 'UTF-8'))
                    else:
                        print('no more data from', client_address, file=sys.stderr)
                        break
                #---------------------------------------

                #Receving cripto data
                while True:

                    data = connection.recv(32)
                    
                    if data:
                        if(data.decode('utf-8') == "ACK"):
                            break

                        print('Received encrypted message: ' % data, file=sys.stderr)

                        data = data.decode('utf-8')
                        decrypted_message = xor_cypher(data, str(PRIVATE_COMMOM_KEY))
                        
                        print('Decrypted message: {}'.format(decrypted_message), file=sys.stderr)
                    else:
                        print('no more data from', client_address, file=sys.stderr)
                        break
                
                
    

        
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


a = server(SERVER_PORT)
a()

# chanel = a("decrypt","hate")
# print('love xor hate = {}'.format(chanel))
# print('{} xor  hate= {}'.format(chanel, a(chanel, 'hate')))


