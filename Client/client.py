import socket
import sys

SERVER_ACCESS = ('localhost', 5100)

def client(SERVER_ACCESS):

    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start():
        print('connecting to %s port %s' % SERVER_ACCESS, file=sys.stderr)
        _socket.connect(SERVER_ACCESS)

        try:
            message = 'This is the message.  It will be repeated.'
            print('sending "%s"' % message, file=sys.stderr)
            send_string(message)

            amount_received = 0
            amount_expected = len(message)
            
            while amount_received < amount_expected:
                data =  _socket.recv(32)
                amount_received += len(data)
                print('received "%s"' % data, file=sys.stderr)

        finally:
            print('closing socket', file=sys.stderr)
            _socket.close()

    def send_string(string):
        _socket.sendall(bytes(string, 'utf-8'))

    return start

a = client(SERVER_ACCESS)
a()