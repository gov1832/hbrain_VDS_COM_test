from PyQt5.QtCore   import QTimer
from PyQt5.QtWidgets import *

import time

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

    def time_bar_timeout(self):
        now = time.localtime()
        self.ui.time_bar.setText(str("%04d/%02d/%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)))

    def set_ui(self):
        # socket
        self.ui.sock_ip_input.setText("127.0.0.1")
        self.ui.sock_port_input.setText("3333")

    def btn_event(self):
        # test
        self.ui.test_btn.clicked.connect(self.test_btn_click)

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
        # endregion


    def test_btn_click(self):
        self.sock.socket_send_msg("testttttt")

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
            # read 스레드 시작 while

    def db_connect_btn_click(self):
        print("db..")
        self.db.test()

    def op_FF_btn_click(self):
        print("btn_click")

    def op_FE_btn_click(self):
        print("btn_click")

    def op_01_btn_click(self):
        print("btn_click")

    def op_04_btn_click(self):
        print("btn_click")

    def op_05_btn_click(self):
        print("btn_click")

    def op_07_btn_click(self):
        print("btn_click")

    def op_0C_btn_click(self):
        print("btn_click")

    def op_0D_btn_click(self):
        print("btn_click")

    def op_0E_btn_click(self):
        print("btn_click")

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