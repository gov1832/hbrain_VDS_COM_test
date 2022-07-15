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

        # value setting
        self.local_ip = '127.0.0.1'

    def time_bar_timeout(self):
        now = time.localtime()
        self.ui.time_bar.setText(str("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)))

    def set_ui(self):
        # socket
        self.ui.sock_ip_input.setText("127.0.0.1")
        self.ui.sock_port_input.setText("3333")

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
            self.ui.status_bar.setText("Socket server 연결중...")
            try:
                self.sock.socket_connect(sock_ip, sock_port)
            except Exception as e:
                self.ui.status_bar.setText("err socket connect: ", e)
            self.ui.status_bar.setText("Socket server '" + sock_ip + "', '" + str(sock_port) + "' connect !")

            # region test btn true
            self.ui.op_FF_btn.setEnabled(True)
            self.ui.op_FE_btn.setEnabled(True)
            self.ui.op_01_btn.setEnabled(True)
            self.ui.op_04_btn.setEnabled(True)
            self.ui.op_05_btn.setEnabled(True)
            self.ui.op_07_btn.setEnabled(True)
            self.ui.op_0C_btn.setEnabled(True)
            self.ui.op_0D_btn.setEnabled(True)
            self.ui.op_0D_btn.setEnabled(True)
            self.ui.op_0E_btn.setEnabled(True)
            self.ui.op_0F_btn.setEnabled(True)
            self.ui.op_11_btn.setEnabled(True)
            self.ui.op_12_btn.setEnabled(True)
            self.ui.op_13_btn.setEnabled(True)
            self.ui.op_15_btn.setEnabled(True)
            self.ui.op_16_btn.setEnabled(True)
            self.ui.op_17_btn.setEnabled(True)
            self.ui.op_18_btn.setEnabled(True)
            self.ui.op_19_btn.setEnabled(True)
            self.ui.op_1E_btn.setEnabled(True)
            # endregion

            # read 스레드 시작 while
            t = threading.Thread(target=self.read_socket_msg, args=())
            t.start()
            # read_socket = Process(target=self.read_socket_msg, args=())
            # read_socket.start()

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
        print("recv_msg: ", recv_msg)
        print("d_recv_msg: ", recv_msg.decode('utf-16'))
        d_recv_msg = recv_msg.decode('utf-16')

        for i in range(len(d_recv_msg)):
            print(i, "   ", d_recv_msg[i])
        # print(msg_op)
        if len(d_recv_msg) > 40:
            msg_op = d_recv_msg[43]
            if msg_op == chr(0xFF):
                sender_ip = d_recv_msg[0:15]
                self.sock.send_FF_res_msg(self.local_ip, sender_ip)


    # endregion

    # region test send msg
    def op_FF_btn_click(self):
        print("btn_click")
        self.sock.send_FF_msg()

    def op_FE_btn_click(self):
        print("btn_click")
        self.sock.send_FE_msg()

    def op_01_btn_click(self):
        print("btn_click")
        self.sock.send_01_msg()

    def op_04_btn_click(self):
        print("btn_click")
        self.sock.send_04_msg()

    def op_05_btn_click(self):
        print("btn_click")
        self.sock.send_05_msg()

    def op_07_btn_click(self):
        print("btn_click")
        self.sock.send_07_msg()

    def op_0C_btn_click(self):
        print("btn_click")
        self.sock.send_0C_msg()

    def op_0D_btn_click(self):
        print("btn_click")
        self.sock.send_0D_msg()

    def op_0E_btn_click(self):
        print("btn_click")
        self.sock.send_0E_msg()

    def op_0F_btn_click(self):
        print("btn_click")

    def op_11_btn_click(self):
        print("btn_click")

    def op_12_btn_click(self):
        print("btn_click")

    def op_13_btn_click(self):
        print("btn_click")

    def op_15_btn_click(self):
        print("btn_click")

    def op_16_btn_click(self):
        print("btn_click")

    def op_17_btn_click(self):
        print("btn_click")

    def op_18_btn_click(self):
        print("btn_click")

    def op_19_btn_click(self):
        print("btn_click")

    def op_1E_btn_click(self):
        print("btn_click")

    # endregion