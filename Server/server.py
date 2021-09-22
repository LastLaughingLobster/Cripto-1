import socket
import sys

SERVER_PORT = 5100

def server(SERVER_PORT):

    def start():
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = ('localhost', SERVER_PORT)
        print('starting up on %s port %s' % server_address, file=sys.stderr)
        _socket.bind(server_address)


        _socket.listen(1)

        while True:
            print('waiting for a connection', file=sys.stderr)
            connection, client_address = _socket.accept()

            try:
                print('connection from', client_address, file=sys.stderr)

                while True:
                    data = connection.recv(32)
                    print('received "%s"' % data, file=sys.stderr)
                    if data:
                        print('sending data back to the client', file=sys.stderr)
                        connection.sendall(data)
                    else:
                        print('no more data from', client_address, file=sys.stderr)
                        break
                    
            finally:
                connection.close()

    return start

a = server(SERVER_PORT)
a()


