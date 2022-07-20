
import socket

import random

class Socket_function:
    def __init__(self):
        super().__init__()

        self.client_socket = None

    def socket_connect(self, ip, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))

    def socket_send_msg(self, send_msg):
        self.client_socket.send(send_msg.encode('utf-16'))

        # recv
        # recv_msg = self.client_socket.recv(1024)
        # d_recv_msg = recv_msg.decode()
        # print("recv: " + recv_msg.decode())
        # for i in range(len(recv_msg)):
        #     print("msg[i]: ", recv_msg[i])
        #
        # for i in range(len(recv_msg)):
        #     print("de_msg[i]: ", recv_msg[i])

    def socket_read(self):
        return self.client_socket.recv(1024)

    # region msg response
    def send_FF_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFF)
        data = chr(0x06) # ack
        # opcode = bytes([0xff])
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    def send_FE_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06) # ack
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    # def send_01_res_msg(self, sender_ip, destination_ip):
    #     controller_kind = 'VD'
    #     controller_number = '12345'
    #     length = '0002'
    #     point = chr(0x2D)
    #     opcode = chr(0xFE)
    #     data = chr(0x06) # ack
    #     send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
    #     print(send_msg)
    #     self.socket_send_msg(send_msg)

    def send_04_res_msg(self, sender_ip, destination_ip, frame_number):
        controller_kind = 'VD'
        controller_number = '12345'
        # length 변경 해야함
        length = '0010'
        point = chr(0x2D)
        opcode = chr(0x04)
        frame_num = frame_number
        lane_err = '0000'
        lane_num = '2'
        lane_data = chr(0x0A) + chr(0x2B) + chr(0x09) + chr(0x2C)
        data = frame_num + lane_err + lane_num + lane_data

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    def send_05_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0x05)
        lane = '2' # 2차선
        lane_1 = [bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2),
                  bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2)]
        lane_2 = [bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2),
                  bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2), bytearray(2)]
        for i in range(len(lane_1)):
            temp = lane_1[i]

            # num = random.randrange(0, 65535)
            num = random.randrange(0, 300)
            if num > 255:
                num_high = num >> 8
                num_low = num & 0xFF
                temp[0] = ord(chr(num_high))
                temp[1] = ord(chr(num_low))
            else:
                temp[1] = ord(chr(num))

        for i in range(len(lane_2)):
            temp = lane_2[i]

            # num = random.randrange(0, 65535)
            num = random.randrange(0, 300)
            if num > 255:
                num_high = num >> 8
                num_low = num & 0xFF
                temp[0] = ord(chr(num_high))
                temp[1] = ord(chr(num_low))
            else:
                temp[1] = ord(chr(num))

        print("1: ", lane_1)
        print("2: ", lane_2)
        data = ''
        for cg_data in lane_1:
            data = data + chr(cg_data[0])
            data = data + chr(cg_data[1])
        for cg_data in lane_2:
            data = data + chr(cg_data[0])
            data = data + chr(cg_data[1])

        length = chr(1 + len(data))
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)

        for i in range(len(send_msg)):
            print(i, "   ", send_msg[i])
        # self.socket_send_msg(send_msg)

    def send_07_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06) # ack
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    def send_0C_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06) # ack
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    def send_0D_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06) # ack
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    def send_0E_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06) # ack
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    def send_0F_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06) # ack
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    def send_11_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06)  # ack
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    def send_12_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06)  # ack
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    def send_13_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06)  # ack
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    def send_15_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06)  # ack
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    def send_16_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06)  # ack
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    def send_17_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06)  # ack
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    def send_18_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06)  # ack
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    def send_19_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06)  # ack
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    def send_1E_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = chr(0x06)  # ack
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        print(send_msg)
        self.socket_send_msg(send_msg)

    # endregion

    def send_FF_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0001'
        point = chr(0x2D)
        opcode = chr(0xFF)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_FE_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0001'
        point = chr(0x2D)
        opcode = chr(0xFE)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_01_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0x01)
        data_frame = chr(120)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data_frame
        self.socket_send_msg(send_msg)

    def send_04_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0001'
        point = chr(0x2D)
        opcode = chr(0x04)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_05_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0001'
        point = chr(0x2D)
        opcode = chr(0x05)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_07_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0001'
        point = chr(0x2D)
        opcode = chr(0x07)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_0C_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0001'
        point = chr(0x2D)
        opcode = chr(0x0C)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_0D_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0001'
        point = chr(0x2D)
        opcode = chr(0x0D)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_0E_msg(self):
        point = chr(0x2D)
        opcode = chr(0x0E)
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        # length = '0001'
        # index = 1 -> 차로지정
        # index = 3 -> 수집주기
        # index = 5 -> 차량 속도 구분
        # index = 7 -> 속도별 누적치 계산
        index = '1'
        # data = '40'


        # send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        # self.socket_send_msg(send_msg)

