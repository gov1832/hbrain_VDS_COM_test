from PyQt5.QtCore   import QTimer
from PyQt5.QtWidgets import *

import time
from multiprocessing import Process
import threading

from db import DB_function
from Socket import Socket_function

class main_function(QWidget):
    def __init__(self, ui):
        super().__init__()

        self.ui = ui

        self.db = DB_function()
        self.sock = Socket_function()

        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.time_bar_timeout)

        self.set_ui()
        self.btn_event()

        # system scenario value
        self.client_connect = None
        self.client_request_time = None
        self.recv_count = None
        self.fe_send_time = None
        self.fe_check = None
        self.fe_num = None
        self.request_timer = QTimer()
        self.request_timer.start(5000)
        self.request_timer.timeout.connect(self.request_check_timer)

        # S/W value
        self.local_ip = None
        self.center_ip = None
        self.client_socket = None
        self.frame_number_set = None
        self.connect_time = None
        self.lane_num = None
        self.collect_cycle = None
        self.category_num = None
        self.acc_speed = None
        self.calc_speed = None
        self.use_unexpected = None

        self.value_setting()

    def value_setting(self):
        # system scenario value
        self.fe_check = True
        self.fe_num = 0

        # S/W value
        self.client_connect = False
        # self.local_ip = '192.168.000.001'
        self.local_ip = '127.000.000.001'
        self.local_ex_ip = '183.99.41.239'
        self.center_ip = '123.456.789.123'
        self.lane_num = 2
        self.collect_cycle = 10
        self.category_num = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        self.acc_speed = 1
        self.calc_speed = 1
        self.use_unexpected = 1





    def time_bar_timeout(self):
        now = time.localtime()
        self.ui.time_bar.setText(str("%04d/%02d/%02d %02d:%02d:%02d" %
                                     (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)))

    def set_ui(self):
        # socket
        self.ui.sock_ip_input.setText("127.0.0.1")
        self.ui.sock_port_input.setText("30100")

        self.ui.op_FF_btn.setEnabled(False)
        self.ui.op_FE_btn.setEnabled(False)
        self.ui.op_01_btn.setEnabled(False)
        self.ui.op_04_btn.setEnabled(False)
        self.ui.op_05_btn.setEnabled(False)
        self.ui.op_07_btn.setEnabled(False)
        self.ui.op_0C_btn.setEnabled(False)
        self.ui.op_0D_btn.setEnabled(False)
        self.ui.op_0D_btn.setEnabled(False)
        self.ui.op_0E_btn.setEnabled(False)
        self.ui.op_0F_btn.setEnabled(False)
        self.ui.op_11_btn.setEnabled(False)
        self.ui.op_12_btn.setEnabled(False)
        self.ui.op_13_btn.setEnabled(False)
        self.ui.op_15_btn.setEnabled(False)
        self.ui.op_16_btn.setEnabled(False)
        self.ui.op_17_btn.setEnabled(False)
        self.ui.op_18_btn.setEnabled(False)
        self.ui.op_19_btn.setEnabled(False)
        self.ui.op_1E_btn.setEnabled(False)

    def btn_event(self):
        self.ui.socket_connect_btn.clicked.connect(self.socket_connect_btn_click)
        self.ui.db_connect_btn.clicked.connect(self.db_connect_btn_click)

        # region request btn event
        self.ui.op_FF_btn.clicked.connect(self.op_FF_btn_click)
        self.ui.op_FE_btn.clicked.connect(self.op_FE_btn_click)
        self.ui.op_01_btn.clicked.connect(self.op_01_btn_click)
        self.ui.op_04_btn.clicked.connect(self.op_04_btn_click)
        self.ui.op_05_btn.clicked.connect(self.op_05_btn_click)
        self.ui.op_07_btn.clicked.connect(self.op_07_btn_click)
        self.ui.op_0C_btn.clicked.connect(self.op_0C_btn_click)
        self.ui.op_0D_btn.clicked.connect(self.op_0D_btn_click)
        self.ui.op_0E_btn.clicked.connect(self.op_0E_btn_click)
        self.ui.op_0F_btn.clicked.connect(self.op_0F_btn_click)
        self.ui.op_11_btn.clicked.connect(self.op_11_btn_click)
        self.ui.op_12_btn.clicked.connect(self.op_12_btn_click)
        self.ui.op_13_btn.clicked.connect(self.op_13_btn_click)
        self.ui.op_15_btn.clicked.connect(self.op_15_btn_click)
        self.ui.op_16_btn.clicked.connect(self.op_16_btn_click)
        self.ui.op_17_btn.clicked.connect(self.op_17_btn_click)
        self.ui.op_18_btn.clicked.connect(self.op_18_btn_click)
        self.ui.op_19_btn.clicked.connect(self.op_19_btn_click)
        self.ui.op_1E_btn.clicked.connect(self.op_1E_btn_click)
        # test
        self.ui.test_btn.clicked.connect(self.test_btn_click)
        # endregion

    def test_btn_click(self):
        self.sock.socket_send_msg("/end")

    # region btn click function
    def socket_connect_btn_click(self):
        sock_ip = self.ui.sock_ip_input.text()
        sock_port = int(self.ui.sock_port_input.text())

        if sock_ip == '' or sock_port == '':
            self.ui.status_bar.setText("Socket IP, PORT를 입력해주세요!")
        else:
            self.ui.status_bar.setText("Socket server open..")
            try:
                self.sock.socket_server_open(sock_ip, sock_port)
            except Exception as e:
                self.ui.status_bar.setText("err socket open: ", e)
            self.ui.status_bar.setText("Socket server '" + sock_ip + "', '" + str(sock_port) + "' open !")

            # region test btn true
            self.ui.op_FF_btn.setEnabled(False)
            self.ui.op_FE_btn.setEnabled(True)
            self.ui.op_01_btn.setEnabled(False)
            self.ui.op_04_btn.setEnabled(False)
            self.ui.op_05_btn.setEnabled(False)
            self.ui.op_07_btn.setEnabled(False)
            self.ui.op_0C_btn.setEnabled(False)
            self.ui.op_0D_btn.setEnabled(False)
            self.ui.op_0D_btn.setEnabled(False)
            self.ui.op_0E_btn.setEnabled(False)
            self.ui.op_0F_btn.setEnabled(False)
            self.ui.op_11_btn.setEnabled(False)
            self.ui.op_12_btn.setEnabled(False)
            self.ui.op_13_btn.setEnabled(False)
            self.ui.op_15_btn.setEnabled(False)
            self.ui.op_16_btn.setEnabled(False)
            self.ui.op_17_btn.setEnabled(False)
            self.ui.op_18_btn.setEnabled(False)
            self.ui.op_19_btn.setEnabled(True)
            self.ui.op_1E_btn.setEnabled(False)
            # endregion

            # read 스레드 시작 while
            # t = threading.Thread(target=self.read_socket_msg, args=())
            # t.start()
            # read_socket = Process(target=self.read_socket_msg, args=())
            # read_socket.start()
            self.sock.client_accept()

            t = threading.Thread(target=self.read_socket_msg, args=())
            t.start()

    def db_connect_btn_click(self):
        print("db..")
        self.db.test()

    # endregion

    # region socket_msg

    def read_socket_msg(self):
        while 1:
            recv_msg = self.sock.socket_read()
            if recv_msg == '':
                break
            else:
                self.parsing_msg(recv_msg)

    def parsing_msg(self, recv_msg):
        d_recv_msg = recv_msg.decode('utf-16')

        # for i in range(len(d_recv_msg)):
        #     print(i, "   ", d_recv_msg[i])
        # print(msg_op)
        if len(d_recv_msg) > 42:
            # print("recv_msg: ", end=' ')
            # for data in d_recv_msg:
            #     print(hex(ord(data)), end='/')
            # print('')
            print("---------------------------------------------------------------------------")
            msg_op = d_recv_msg[43]
            msg_sender_ip = d_recv_msg[0:15]
            destination_ip = d_recv_msg[16:31]
            self.center_ip = msg_sender_ip

            # 수신메시지의 목적지 IP == local IP
            if destination_ip == self.local_ip:
                self.client_request_time = time.time()
                print("RX_msg: [", recv_msg.decode('utf-16'), "]")
                if msg_op == chr(0xFF):
                    self.sock.send_FF_res_msg(self.local_ip, self.center_ip)
                    self.client_connect = True
                    self.connect_time = time.time()
                elif msg_op == chr(0xFE):
                    # self.sock.send_FE_res_msg(self.local_ip, self.center_ip)
                    self.fe_check = True
                    print('0xFE response')
                elif msg_op == chr(0x01):
                    self.device_sync(msg_op, d_recv_msg)
                    # self.sock.send_01_res_msg(self.local_ip, sender_ip)
                    print("not ack")
                elif msg_op == chr(0x04):
                    self.sock.send_04_res_msg(self.local_ip, self.center_ip, self.collect_cycle)
                elif msg_op == chr(0x05):
                    self.db.get_speed()
                    self.sock.send_05_res_msg(self.local_ip, self.center_ip, sdsdfs)
                elif msg_op == chr(0x07):
                    self.sock.send_07_res_msg(self.local_ip, self.center_ip)
                elif msg_op == chr(0x0C):
                    self.device_sync(msg_op, d_recv_msg)
                    self.sock.send_0C_res_msg(self.local_ip, self.center_ip)
                elif msg_op == chr(0x0D):
                    self.sock.send_0D_res_msg(self.local_ip, self.center_ip)
                elif msg_op == chr(0x0E):
                    self.device_sync(msg_op, d_recv_msg)
                    self.sock.send_0E_res_msg(self.local_ip, self.center_ip)
                elif msg_op == chr(0x0F):
                    index = int(ord(d_recv_msg[44]))
                    self.sock.send_0F_res_msg(self.local_ip, self.center_ip, index,
                                              self.lane_num, self.collect_cycle, self.category_num, self.acc_speed, self.calc_speed, self.use_unexpected)
                elif msg_op == chr(0x11):
                    request_time = time.time()
                    self.sock.send_11_res_msg(self.local_ip, self.center_ip, self.connect_time, request_time)
                elif msg_op == chr(0x13):
                    self.sock.send_13_res_msg(self.local_ip, self.center_ip, d_recv_msg)
                elif msg_op == chr(0x15):
                    self.db.get_version_num()
                    self.sock.send_15_res_msg(self.local_ip, self.center_ip)
                elif msg_op == chr(0x16):
                    self.sock.send_16_res_msg(self.local_ip, self.center_ip)
                elif msg_op == chr(0x17):
                    self.sock.send_17_res_msg(self.local_ip, self.center_ip)
                elif msg_op == chr(0x18):
                    self.sock.send_18_res_msg(self.local_ip, self.center_ip)
                elif msg_op == chr(0x19):
                    self.sock.send_19_res_msg(self.local_ip, self.center_ip)
                elif msg_op == chr(0x1E):
                    self.sock.send_1E_res_msg(self.local_ip, self.center_ip)
            elif destination_ip == self.center_ip:
                print("msg   : [", recv_msg.decode('utf-16'), "]")
            else:
                print("TX_msg: [", recv_msg.decode('utf-16'), "]")
    # endregion

    def request_check_timer(self):
        if self.client_connect:
            now_time = time.time()
            time_delay = now_time - self.client_request_time
            # print("delay: ", time_delay)

            if (time_delay > 300) & self.fe_check:
                self.sock.send_FE_msg(self.local_ip, self.center_ip)
                self.fe_send_time = time.time()
                self.fe_check = False

            if not self.fe_check:
                fe_delay = now_time - self.fe_send_time
                if (fe_delay > 5) & (self.fe_num < 2):
                    self.sock.send_FE_msg(self.local_ip, self.center_ip)
                    self.fe_send_time = time.time()
                    self.fe_num += 1
                else:
                    self.client_connect = False
                    self.fe_num = 0

        else:
            print("client not connect")

    def device_sync(self, op, msg):
        lane = 1
        if op == chr(0x01):
            self.frame_number_set = msg[44]
        elif op == chr(0x0C):
            self.lane_num = 2
            self.collect_cycle = 30
            self.category_num = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
            self.acc_speed = 1
            self.calc_speed = 1
            self.use_unexpected = 1
            # 이외의 설정값 등 리셋
        elif op == chr(0x0E):
            index = int(ord(msg[44]))
            # 차로 지정
            if index == 1:
                data = msg[45:]
                data_1 = int(ord(data[0]))
                data_2 = int(ord(data[1]))
                if data_1 != 0:   # 1byte
                    for i in range(0, 8):
                        if (data_1 >> i) & 0x01 == 0x01:
                            self.lane_num = i + 1
                else: # 2 byte
                    for i in range(0, 8):
                        if (data_2 >> i) & 0x01 == 0x01:
                            self.lane_num = (i + 1) + 8
            # 수집 주기
            elif index == 3:
                data = int(ord(msg[45]))
                self.collect_cycle = data
            # 차량 속도 구분
            elif index == 5:
                data = msg[45:]
                for i in range(len(data)):
                    self.category_num[i] = int(ord(data[i]))
            elif index == 7:
                data = int(ord(msg[45]))
                self.acc_speed = data
            elif index == 9:
                data = int(ord(msg[45]))
                self.calc_speed = data
            elif index == 19:
                data = int(ord(msg[45]))
                self.use_unexpected = data

    # region test send msg
    def op_FF_btn_click(self):
        print("FF btn_click")
        self.sock.send_FF_msg()

    def op_FE_btn_click(self):
        print("FE btn_click")
        self.sock.send_FE_msg(self.local_ip, self.center_ip)

    def op_01_btn_click(self):
        print("01 btn_click")
        self.sock.send_01_msg()

    def op_04_btn_click(self):
        print("04 btn_click")
        self.sock.send_04_msg()

    def op_05_btn_click(self):
        print("05 btn_click")
        self.sock.send_05_msg()

    def op_07_btn_click(self):
        print("07 btn_click")
        self.sock.send_07_msg()

    def op_0C_btn_click(self):
        print("0C btn_click")
        self.sock.send_0C_msg()

    def op_0D_btn_click(self):
        print("0D btn_click")
        self.sock.send_0D_msg()

    def op_0E_btn_click(self):
        print("0E btn_click")
        self.sock.send_0E_msg()

    def op_0F_btn_click(self):
        print("0F btn_click")
        self.sock.send_0F_msg()

    def op_11_btn_click(self):
        print("11 btn_click")
        self.sock.send_11_msg()

    def op_12_btn_click(self):
        print("12 btn_click")
        self.sock.send_12_msg()

    def op_13_btn_click(self):
        print("13 btn_click")
        self.sock.send_13_msg()

    def op_15_btn_click(self):
        print("15 btn_click")
        self.sock.send_15_msg()

    def op_16_btn_click(self):
        print("16 btn_click")
        self.sock.send_16_msg()

    def op_17_btn_click(self):
        print("17 btn_click")
        self.sock.send_17_msg()

    def op_18_btn_click(self):
        print("18 btn_click")
        self.sock.send_18_msg()

    def op_19_btn_click(self):
        print("19 btn_click")

    def op_1E_btn_click(self):
        print("1E btn_click")
        self.sock.send_1E_msg()

    # endregion