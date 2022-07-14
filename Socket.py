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
        d_recv_msg = recv_msg.decode()
        print("recv: " + recv_msg.decode())
        for i in range(len(recv_msg)):
            print("msg[i]: ", recv_msg[i])

        for i in range(len(recv_msg)):
            print("de_msg[i]: ", recv_msg[i])

    def socket_read(self):
        return self.client_socket.recv(1)

    def send_FF_msg(self):
        sender_ip = '123.456.789.123-'
        destination_ip = '127.000.000.001-'
        controller_kind = 'VD'
        controller_number = '00000'
        length = '0001'
        opcode = 'FF'

        send_msg = sender_ip + destination_ip + controller_kind + controller_number + length + opcode
        print(send_msg)
        self.socket_send_msg(send_msg)
