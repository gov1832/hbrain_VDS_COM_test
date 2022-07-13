import socket

class Socket_function:
    def __init__(self):
        super().__init__()

        self.client_socket = None

    def socket_connect(self, ip, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))

    def socket_send_msg(self, send_msg):
        self.client_socket.send(send_msg.encode())

        # recv
        recv_msg = self.client_socket.recv(1024)
        print("recv: " + recv_msg.decode())

    def socket_read(self):
        return self.client_socket.recv(1)
