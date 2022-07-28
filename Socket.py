
import socket
from time import localtime

from other import Other_function

import random

class Socket_function:
    def __init__(self):
        super().__init__()

        self.server_socket = None
        self.client_socket = None

        self.ot = Other_function()

    def socket_server_open(self, ip, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((ip, port))
        self.server_socket.listen()

    def client_accept(self):
        self.client_socket, addr = self.server_socket.accept()
        return self.client_socket

    def socket_connect(self, ip, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, port))

    def socket_send_msg(self, send_msg):
        self.client_socket.send(send_msg.encode('utf-16'))
        print("TX_msg: /", send_msg, "/")
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
        point = chr(0x2D)
        opcode = chr(0xFF)
        data = chr(0x06) # ack
        length = self.ot.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_FE_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0xFE)
        length = self.ot.length_calc(1)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    # def send_01_res_msg(self, sender_ip, destination_ip):
    #     controller_kind = 'VD'
    #     controller_number = '12345'
    #     length = '0002'
    #     point = chr(0x2D)
    #     opcode = chr(0xFE)
    #     data = chr(0x06) # ack
    #     send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
    #     self.socket_send_msg(send_msg)

    def send_04_res_msg(self, sender_ip, destination_ip, frame, lane, traffic_data):
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0x04)
        frame_num = chr(frame)
        lane_num = chr(lane)

        # traffic data => [[차량수, 속도],[차량수, 속도]]
        lane_data = ''
        for i in traffic_data:
            lane_data = lane_data + chr(i[0]) + chr(i[1])
        data = frame_num + lane_num + lane_data
        length = self.ot.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
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

        data = lane
        for cg_data in lane_1:
            data = data + chr(cg_data[0])
            data = data + chr(cg_data[1])
        for cg_data in lane_2:
            data = data + chr(cg_data[0])
            data = data + chr(cg_data[1])

        length = self.ot.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data

        self.socket_send_msg(send_msg)

        # for i in range(len(send_msg)):
        #     print(i, "   ", send_msg[i])

    def send_07_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0x07)

        lane_1 = bytearray(2)
        lane_2 = bytearray(2)

        # num = random.randrange(0, 65535)
        num1 = random.randrange(0, 250)
        num1_high = num1 >> 8
        num1_low = num1 & 0xFF
        lane_1[0] = ord(chr(num1_high))
        lane_1[1] = ord(chr(num1_low))

        num2 = random.randrange(0, 300)
        num2_high = num2 >> 8
        num2_low = num2 & 0xFF
        lane_2[0] = ord(chr(num2_high))
        lane_2[1] = ord(chr(num2_low))

        data = chr(lane_1[0]) + chr(lane_1[1]) + chr(lane_2[0]) + chr(lane_2[1])
        length = self.ot.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_0C_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0x0C)
        data = chr(0x06) # ack
        length = self.ot.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_0D_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '54321'
        point = chr(0x2D)
        opcode = chr(0x0D)
        data = chr(0x06) # ack
        length = self.ot.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_0E_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0x0E)
        data = chr(0x06) # ack
        length = self.ot.length_calc(1 + len(data))
        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_0F_res_msg(self, sender_ip, destination_ip, index,
                        lane_num, collect_cycle, category_num, acc_speed, calc_speed, use_unexpected):
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0002'
        point = chr(0x2D)
        opcode = chr(0x0F)

        data = ''
        if index == 1:
            # 차로 계산 (1 << 차로-1)
            byte_1 = chr(1 << (lane_num - 1))
            byte_2 = chr(0)
            data = byte_1 + byte_2
        elif index == 3:
            # 수집주기 기본 30, 변경값 60
            byte_1 = chr(collect_cycle)
            data = byte_1
        elif index == 5:
            # 차량 속도 category 단위 기본 10
            byte_1 = chr(category_num[0])
            byte_2 = chr(category_num[1])
            byte_3 = chr(category_num[2])
            byte_4 = chr(category_num[3])
            byte_5 = chr(category_num[4])
            byte_6 = chr(category_num[5])
            byte_7 = chr(category_num[6])
            byte_8 = chr(category_num[7])
            byte_9 = chr(category_num[8])
            byte_10 = chr(category_num[9])
            byte_11 = chr(category_num[10])
            byte_12 = chr(category_num[11])
            data = byte_1 + byte_2 + byte_3 + byte_4 + byte_5 + byte_5 + byte_6 + \
                   byte_7 + byte_8 + byte_9 + byte_10 + byte_11 + byte_12
        elif index == 7:
            data = chr(index)
            # 속도별 누적치 계산 기본 1(사용)
            byte_1 = chr(acc_speed)
            data = data + byte_1
        elif index == 9:
            data = chr(index)
            # 속도 계산 가능 여부 기본 1(사용)
            byte_1 = chr(calc_speed)
            data = data + byte_1
        elif index == 19:
            data = chr(index)
            # 돌발 사용 여부 기본 0(사용안함)
            byte_1 = chr(use_unexpected)
            data = data + byte_1

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_11_res_msg(self, sender_ip, destination_ip, connect_time, request_time):
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0x11)
        if connect_time != None and request_time != None:
            time_cha = int(request_time - connect_time)
            time_1 = time_cha & 0xFF
            time_2 = (time_cha >> 8) & 0xFF
            time_3 = (time_cha >> 16) & 0xFF
            time_4 = (time_cha >> 24) & 0xFF
            data = chr(time_3) + chr(time_3) + chr(time_2) + chr(time_1)
            length = self.ot.length_calc(1 + len(data))

            send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
            self.socket_send_msg(send_msg)
        else:
            print("Please connect 0xFF")

    def send_13_res_msg(self, sender_ip, destination_ip, msg):
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0x13)
        data = msg[44:]
        length = self.ot.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_15_res_msg(self, sender_ip, destination_ip, version_list):
        if version_list == '':
            print("version_list is None")
        else:
            controller_kind = 'VD'
            controller_number = '12345'
            point = chr(0x2D)
            opcode = chr(0x15)
            version = version_list[1] << 4
            release = version_list[2] & 0x0F
            version_num = chr(version + release)
            make_year = chr(version_list[3])
            make_month = chr(version_list[4])
            make_day = chr(version_list[5])
            data = version_num + make_year + make_month + make_day
            length = self.ot.length_calc(1 + len(data))

            send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
            self.socket_send_msg(send_msg)

    # 개별 차량 데이터 응답
    def send_16_res_msg(self, sender_ip, destination_ip, frame, individual_traffic_data):
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0x16)
        car_count = chr(len(individual_traffic_data) >> 8) + chr(len(individual_traffic_data) & 0xFF)
        data = frame + car_count
        for i in individual_traffic_data:
            data = data + str(i[0]) + str(i[1]) + str(i[2])

        length = self.ot.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    # 정지 영상 응답
    def send_17_res_msg(self, sender_ip, destination_ip, cam):
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0x17)
        image_count = chr(1)
        image_info = '1111' + '122334454524ofkcdo'
        data = cam + image_count + image_info

        length = self.ot.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    # RTC 변경 응답
    def send_18_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0x18)
        data = chr(0x06)  # ack
        length = self.ot.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    # 돌발 상황 정보
    def send_19_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0xFE)
        data = '100000001233444444444455555555556666'
        length = self.ot.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_1E_res_msg(self, sender_ip, destination_ip):
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0x1E)
        data = chr(0x00) + chr(0x00) + chr(0x01) + chr(0x09) + chr(0x09) + chr(0x09) + chr(0x09) + chr(0x09) + chr(0x01) + chr(40) + chr(220) + chr(220)
        length = self.ot.length_calc(1 + len(data))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    # endregion

    def send_FF_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = self.ot.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0xFF)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)
    #
    # def send_FE_msg(self):
    #     sender_ip = '123.456.789.123'
    #     destination_ip = '127.000.000.001'
    #     controller_kind = 'VD'
    #     controller_number = '12345'
    #     length = self.length_calc(1)
    #     point = chr(0x2D)
    #     opcode = chr(0xFE)
    #
    #     send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
    #     self.socket_send_msg(send_msg)

    def send_01_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0x01)
        data_frame = chr(120)
        length = self.ot.length_calc(2)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data_frame
        self.socket_send_msg(send_msg)

    def send_04_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = self.ot.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0x04)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_05_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = self.ot.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0x05)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_07_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = self.ot.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0x07)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_0C_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = self.ot.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0x0C)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_0D_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0x0D)
        length = self.ot.length_calc(1)

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
        index_list = [1, 3, 5, 7, 9, 21]
        index = random.choice(index_list)

        data = ''
        if index == 1:
            data = chr(index)
            # 차로 계산 (1 << 차로-1)
            byte_1 = chr(1 << (2-1))
            byte_2 = chr(0)
            data = data + byte_1 + byte_2
        elif index == 3:
            data = chr(index)
            # 수집주기 기본 30, 변경값 60
            byte_1 = chr(60)
            data = data + byte_1
        elif index == 5:
            data = chr(index)
            # 차량 속도 category 단위 기본 10
            byte_1 = chr(10)
            byte_2 = chr(10)
            byte_3 = chr(10)
            byte_4 = chr(10)
            byte_5 = chr(10)
            byte_6 = chr(10)
            byte_7 = chr(10)
            byte_8 = chr(10)
            byte_9 = chr(10)
            byte_10 = chr(10)
            byte_11 = chr(10)
            byte_12 = chr(10)
            data = data + byte_1 + byte_2 + byte_3 + byte_4 + byte_5 + byte_5 + byte_6 + \
                   byte_7 + byte_8 + byte_9 + byte_10 + byte_11 + byte_12
        elif index == 7:
            data = chr(index)
            # 속도별 누적치 계산 기본 1(사용)
            byte_1 = chr(0)
            data = data + byte_1
        elif index == 9:
            data = chr(index)
            # 속도 계산 가능 여부 기본 1(사용)
            byte_1 = chr(0)
            data = data + byte_1
        elif index == 21:
            data = chr(index)
            # 속도 계산 가능 여부 기본 0(사용안함)
            byte_1 = chr(1)
            data = data + byte_1

        length = self.ot.length_calc(1 + data)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + data
        self.socket_send_msg(send_msg)

    def send_0F_msg(self):
        point = chr(0x2D)
        opcode = chr(0x0F)
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        index_list = [1, 3, 5, 7, 9, 21]
        index = chr(random.choice(index_list))
        length = self.ot.length_calc(1 + len(index))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + index
        self.socket_send_msg(send_msg)

    def send_11_msg(self):
        point = chr(0x2D)
        opcode = chr(0x11)
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = self.ot.length_calc(1)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_13_msg(self):
        point = chr(0x2D)
        opcode = chr(0x13)
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        echo_msg = 'qwelkjdasoiweoi2390weiodskl'
        length = self.ot.length_calc(1 + len(echo_msg))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + echo_msg
        self.socket_send_msg(send_msg)

    def send_15_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = self.ot.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0x15)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_16_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = self.ot.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0x16)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_17_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        point = chr(0x2D)
        opcode = chr(0x17)
        cam = chr(random.randrange(0, 3))
        length = self.ot.length_calc(1 + len(cam))

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode + cam
        self.socket_send_msg(send_msg)

    def send_18_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = '0008'
        point = chr(0x2D)
        opcode = chr(0x18)
        # change_rtc_tune =

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)

    def send_1E_msg(self):
        sender_ip = '123.456.789.123'
        destination_ip = '127.000.000.001'
        controller_kind = 'VD'
        controller_number = '12345'
        length = self.ot.length_calc(1)
        point = chr(0x2D)
        opcode = chr(0x1E)

        send_msg = sender_ip + point + destination_ip + point + controller_kind + controller_number + length + opcode
        self.socket_send_msg(send_msg)


