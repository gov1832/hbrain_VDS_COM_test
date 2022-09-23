import os.path

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

import time
from datetime import datetime
import queue
from multiprocessing import Process
import threading
# import win32api

import numpy as np
import cv2

from db import DB_function
from Socket import Socket_function
from other import Other_function
from log import Log_function


class main_function(QWidget):
    def __init__(self, ui):
        super().__init__()

        self.ui = ui

        self.db = DB_function()
        self.sock = Socket_function()
        self.ot = Other_function()
        self.log = Log_function()

        self.timer = QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.time_bar_timeout)

        self.set_ui()
        self.ui_event()

        exe_path = os.path.abspath(".")
        log_folder = "Log"
        folder_path = os.path.join(exe_path, log_folder)
        self.log.make_directory(folder_path=folder_path)

        # system scenario value
        self.client_test = None
        self.client_connect = None
        self.client_request_time = None
        self.recv_count = None
        self.fe_send_time = None
        self.fe_check = None
        self.fe_num = None
        self.read_thread = None
        self.dsocket_thread = None
        # self.d
        self.request_timer = QTimer()
        self.request_timer.start(5000)
        self.request_timer.timeout.connect(self.request_check_timer)

        # S/W value
        self.local_ip = None
        self.center_ip = None
        self.db_ip = None
        self.db_port = None
        self.db_id = None
        self.db_pw = None
        self.db_name = None
        self.controller_type = None
        self.controller_index = None
        self.client_socket = None
        self.frame_number_04 = None
        self.frame_number_16 = None
        self.connect_time = None
        self.sync_time = None
        self.lane_num = None
        self.collect_cycle = None
        self.category_num = None
        self.use_ntraffic = None
        self.use_category_speed = None
        self.use_unexpected = None
        self.individual_traffic_data = None
        self.traffic_data = None
        self.ntraffic_data = None
        self.speed_data = None
        self.controllerBox_state_list = None
        self.m_log_save = None
        self.value_setting()

    def value_setting(self):
        # system scenario value
        self.fe_check = True
        self.fe_num = 0
        self.read_thread = []
        # self.client_test = []

        # S/W value
        self.client_connect = False
        self.local_ip = self.ot.make_16ip(sip=self.ui.sock_ip_input.text())
        self.center_ip = '000.000.000.000'
        self.controller_type = 'VD'
        self.controller_index = self.ot.get_controller_number(self.ui.cont_num_edit.text())
        self.controller_station = self.controller_type + self.controller_index
        self.lane_num = 6
        self.collect_cycle = 30
        self.category_num = [0, 11, 21, 31, 41, 51, 61, 71, 81, 91, 101, 111]
        self.use_ntraffic = 1
        self.use_category_speed = 1
        self.use_unexpected = 1
        self.m_log_save = True

    def time_bar_timeout(self):
        now = time.localtime()
        self.ui.time_bar.setText(str("%04d/%02d/%02d %02d:%02d:%02d" %
                                     (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)))

    def set_ui(self):
        # socket
        self.ui.sock_ip_input.setText("127.0.0.1")
        self.ui.sock_port_input.setText("30100")
        # self.ui.dp_ip_input.setText("input")
        # self.ui.db_ip_input.setText("183.98.24.70")
        # self.ui.db_port_input.setText("53307")
        # self.ui.db_id_input.setText("admin")
        # self.ui.db_name_input.setText("hbrain_vds")
        self.ui.db_ip_input.setText("183.99.41.239")
        self.ui.db_port_input.setText("23306")
        self.ui.db_id_input.setText("root")
        self.ui.db_name_input.setText("hbrain_vds")
        self.ui.db_pw_input.setText("hbrain0372!")
        self.ui.db_name_input.setEnabled(False)

        self.ui.socket_open_btn.setEnabled(False)

        # region send test btn
        # self.ui.op_FF_btn.setEnabled(False)
        # self.ui.op_FE_btn.setEnabled(False)
        # self.ui.op_01_btn.setEnabled(False)
        # self.ui.op_04_btn.setEnabled(False)
        # self.ui.op_05_btn.setEnabled(False)
        # self.ui.op_07_btn.setEnabled(False)
        # self.ui.op_0C_btn.setEnabled(False)
        # self.ui.op_0D_btn.setEnabled(False)
        # self.ui.op_0D_btn.setEnabled(False)
        # self.ui.op_0E_btn.setEnabled(False)
        # self.ui.op_0F_btn.setEnabled(False)
        # self.ui.op_11_btn.setEnabled(False)
        # self.ui.op_12_btn.setEnabled(False)
        # self.ui.op_13_btn.setEnabled(False)
        # self.ui.op_15_btn.setEnabled(False)
        # self.ui.op_16_btn.setEnabled(False)
        # self.ui.op_17_btn.setEnabled(False)
        # self.ui.op_18_btn.setEnabled(False)
        # self.ui.op_19_btn.setEnabled(False)
        # self.ui.op_1E_btn.setEnabled(False)
        # endregion

        self.ui.tx_table.setColumnWidth(0, 180)
        self.ui.tx_table.setColumnWidth(1, 80)
        self.ui.tx_table.setColumnWidth(2, 90)
        self.ui.tx_table.setColumnWidth(3, 200)
        self.ui.rx_table.setColumnWidth(0, 180)
        self.ui.rx_table.setColumnWidth(1, 80)
        self.ui.rx_table.setColumnWidth(2, 90)
        self.ui.rx_table.setColumnWidth(3, 200)

        if not self.ui.Log_check_box.isChecked():
            self.ui.Log_check_box.toggle()

    def ui_event(self):
        # region btn event
        self.ui.socket_open_btn.clicked.connect(self.socket_open_btn_click)
        self.ui.db_connect_btn.clicked.connect(self.db_connect_btn_click)
        self.ui.cont_num_change_btn.clicked.connect(self.cont_num_change_btn_click)
        # endregion

        # region ui event
        self.ui.Log_check_box.stateChanged.connect(self.log_check_box_check)
        # endregion

        # region request btn event
        # self.ui.op_FF_btn.clicked.connect(self.op_FF_btn_click)
        # self.ui.op_FE_btn.clicked.connect(self.op_FE_btn_click)
        # self.ui.op_01_btn.clicked.connect(self.op_01_btn_click)
        # self.ui.op_04_btn.clicked.connect(self.op_04_btn_click)
        # self.ui.op_05_btn.clicked.connect(self.op_05_btn_click)
        # self.ui.op_07_btn.clicked.connect(self.op_07_btn_click)
        # self.ui.op_0C_btn.clicked.connect(self.op_0C_btn_click)
        # self.ui.op_0D_btn.clicked.connect(self.op_0D_btn_click)
        # self.ui.op_0E_btn.clicked.connect(self.op_0E_btn_click)
        # self.ui.op_0F_btn.clicked.connect(self.op_0F_btn_click)
        # self.ui.op_11_btn.clicked.connect(self.op_11_btn_click)
        # self.ui.op_12_btn.clicked.connect(self.op_12_btn_click)
        # self.ui.op_13_btn.clicked.connect(self.op_13_btn_click)
        # self.ui.op_15_btn.clicked.connect(self.op_15_btn_click)
        # self.ui.op_16_btn.clicked.connect(self.op_16_btn_click)
        # self.ui.op_17_btn.clicked.connect(self.op_17_btn_click)
        # self.ui.op_18_btn.clicked.connect(self.op_18_btn_click)
        # self.ui.op_19_btn.clicked.connect(self.op_19_btn_click)
        # self.ui.op_1E_btn.clicked.connect(self.op_1E_btn_click)
        # # test
        # self.ui.test_btn.clicked.connect(self.test_btn_click)
        # endregion

    def test_btn_click(self):
        self.log.log_save()

    # region btn click function
    def socket_open_btn_click(self):
        self.local_ip = self.ot.make_16ip(sip=self.ui.sock_ip_input.text())
        self.controller_index = self.ot.get_controller_number(self.ui.cont_num_edit.text())
        if self.controller_index != '':
            sock_ip = self.ui.sock_ip_input.text()
            sock_port = int(self.ui.sock_port_input.text())

            if sock_ip == '' or sock_port == '':
                self.update_Statusbar_text("Socket IP, PORT를 입력해주세요!")
            else:
                self.update_Statusbar_text("Socket server open..")
                try:
                    self.sock.socket_server_open(sock_ip, sock_port)
                    self.update_Statusbar_text("Socket server '" + sock_ip + "', '" + str(sock_port) + "' open !")
                    self.ui.socket_open_btn.setEnabled(False)
                    t = threading.Thread(target=self.client_accept_check, args=(), daemon=True)
                    t.start()
                except Exception as e:
                    self.update_Statusbar_text("socket server open fail")

                # region test btn true
                # self.ui.op_FF_btn.setEnabled(False)
                # self.ui.op_FE_btn.setEnabled(True)
                # self.ui.op_01_btn.setEnabled(False)
                # self.ui.op_04_btn.setEnabled(False)
                # self.ui.op_05_btn.setEnabled(False)
                # self.ui.op_07_btn.setEnabled(False)
                # self.ui.op_0C_btn.setEnabled(False)
                # self.ui.op_0D_btn.setEnabled(False)
                # self.ui.op_0D_btn.setEnabled(False)
                # self.ui.op_0E_btn.setEnabled(False)
                # self.ui.op_0F_btn.setEnabled(False)
                # self.ui.op_11_btn.setEnabled(False)
                # self.ui.op_12_btn.setEnabled(False)
                # self.ui.op_13_btn.setEnabled(False)
                # self.ui.op_15_btn.setEnabled(False)
                # self.ui.op_16_btn.setEnabled(False)
                # self.ui.op_17_btn.setEnabled(False)
                # self.ui.op_18_btn.setEnabled(False)
                # self.ui.op_19_btn.setEnabled(True)
                # self.ui.op_1E_btn.setEnabled(False)
                # endregion


        else:
            self.update_Statusbar_text("controller number는 10자로 입력해주세요")

    def client_accept_check(self):
        while True:
            self.client_test = self.sock.client_accept()
            # read thread
            t = threading.Thread(target=self.read_socket_msg, args=(), daemon=True)
            self.read_thread.append(t)
            if len(self.read_thread) > 2:
                self.read_thread.pop(0)
            self.read_thread[-1].start()
            # 돌발 thread
            self.dsocket_thread = threading.Thread(target=self.read_dsocket_msg, args=(), daemon=True)
            # dt.start()
            # 파라미터값 초기화
            parameter_list = self.db.get_parameter_data(host=self.db_ip, port=int(self.db_port), user=self.db_id, password=self.db_pw, db=self.db_name, charset='utf8')
            if parameter_list:
                self.lane_num = parameter_list[0]
                self.collect_cycle = parameter_list[1]
                self.category_num = parameter_list[2]
                self.use_ntraffic = parameter_list[3]
                self.use_category_speed = parameter_list[4]
                self.use_unexpected = parameter_list[5]
            else:
                self.lane_num = 6
                self.collect_cycle = 30
                self.category_num = [0, 11, 21, 31, 41, 51, 61, 71, 81, 91, 101, 111]
                self.use_ntraffic = 1
                self.use_category_speed = 1
                self.use_unexpected = 1

    def db_connect_btn_click(self):
        try:
            self.db_ip = self.ui.db_ip_input.text()
            self.db_port = self.ui.db_port_input.text()
            self.db_id = self.ui.db_id_input.text()
            self.db_pw = self.ui.db_pw_input.text()
            self.db_name = self.ui.db_name_input.text()
            if self.db.db_connection_check(host=self.db_ip, port=int(self.db_port), user=self.db_id, password=self.db_pw, db=self.db_name, charset='utf8'):
                self.ui.socket_open_btn.setEnabled(True)
                self.ui.db_connect_btn.setEnabled(False)
                self.update_Statusbar_text("DB connect success")

        except Exception as e:
            self.update_Statusbar_text("DB connect fail")


    def cont_num_change_btn_click(self):
        cont_num = self.ot.get_controller_number(self.ui.cont_num_edit.text())
        self.controller_index = cont_num
        self.controller_station = self.controller_type + self.controller_index
        if self.controller_index == '':
            self.update_Statusbar_text("controller number는 10자로 입력해주세요")
        else:
            self.update_Statusbar_text("controller number: " +
                                       str(hex(ord(self.controller_index[0]))) + "/" +
                                       str(hex(ord(self.controller_index[1]))) + "/" +
                                       str(hex(ord(self.controller_index[2]))) + "/" +
                                       str(hex(ord(self.controller_index[3]))) + "/" +
                                       str(hex(ord(self.controller_index[4]))))
    # endregion

    # region ui click function
    def log_check_box_check(self):
        if self.ui.Log_check_box.isChecked():
            self.m_log_save = True
        else:
            self.m_log_save = False

        print(self.m_log_save)
    # endregion

    # region socket_msg

    def read_socket_msg(self):
        while 1:
            recv_msg = self.sock.socket_read()
            if recv_msg == '':
                # if len(self.read_thread) > 1:
                # self.read_thread.pop(0)
                # self.sock.client_socket_close()
                break
            else:
                self.parsing_msg(recv_msg)
                # print(recv_msg.decode('utf-16'))
        # self.sock.client_socket_close()
        self.client_connect = False
        print("client close")

    # 돌발
    def read_dsocket_msg(self):
        while self.client_connect:
            # if self.client_connect:
            outbreakdata = self.db.get_outbreak(lane=self.lane_num, host=self.db_ip, port=int(self.db_port), user=self.db_id, password=self.db_pw, db=self.db_name)
            if outbreakdata:
                # print
                print("0x19 돌발: ", outbreakdata)
                if self.use_unexpected:
                    self.sock.send_19_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, outbreakdata)
                    self.update_TX_Log(chr(0x19), [0])

    def parsing_msg(self, recv_msg):
        print("---------------------------------------------------------------------------")
        d_recv_msg = recv_msg.decode('utf-16')
        # for i in range(len(d_recv_msg)):
        #     print(i,": ", ord(d_recv_msg[i]))
        if (d_recv_msg[43] == chr(0xFE)) or (d_recv_msg[43] == chr(0x19)):
            if d_recv_msg[44] == chr(0x06):
                self.update_RX_Log(d_recv_msg[43], [1])
            elif d_recv_msg[44] == chr(0x15):
                self.update_RX_Log(d_recv_msg[43], [2, d_recv_msg[45]])
        else:
            self.update_RX_Log(d_recv_msg[43], [0])

        result = self.ot.nack_find(msg=d_recv_msg, csn=self.controller_station)
        if result[0] == True:
            msg_op = d_recv_msg[43]
            msg_sender_ip = d_recv_msg[0:15]
            destination_ip = d_recv_msg[16:31]

            # 수신메시지의 목적지 IP == local IP
            if destination_ip == self.local_ip:
                self.center_ip = msg_sender_ip
                self.client_request_time = time.time()
                # print("RX_msg: [", recv_msg.decode('utf-16'), "]")
                # print("RX: [", recv_msg, "]")
                print("RX OPCode: ", "0x{:02X}".format(ord(msg_op)))
                if msg_op == chr(0xFF):
                    self.sock.send_FF_res_msg(self.local_ip, self.center_ip, self.controller_type,
                                              self.controller_index)
                    self.update_TX_Log(chr(0xFF), [1])
                    self.client_connect = True
                    if not self.dsocket_thread.is_alive():
                        self.dsocket_thread.start()
                    self.connect_time = time.time()
                elif msg_op == chr(0xFE):
                    self.fe_check = True
                    print('0xFE response')
                elif msg_op == chr(0x01):
                    # self.device_sync(msg_op, d_recv_msg)
                    self.frame_number_04 = d_recv_msg[44]
                    self.frame_number_16 = d_recv_msg[44]
                    self.sync_time = time.time()
                    print("not ack")
                elif msg_op == chr(0x04):
                    self.traffic_data = self.db.get_traffic_data(cycle=self.collect_cycle, sync_time=self.sync_time, lane=self.lane_num, host=self.db_ip, port=int(self.db_port), user=self.db_id, password=self.db_pw, db=self.db_name)
                    if self.traffic_data != [] and self.frame_number_04 is not None:
                        # print
                        print("0x04 교통량: ", self.traffic_data)
                        self.sock.send_04_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, self.frame_number_04, self.lane_num, self.traffic_data)
                        self.update_TX_Log(chr(0x04), [1])
                        # self.frame_number_04 = None
                    else:
                        list = [False, chr(0x04), chr(0x06)]
                        self.sock.send_nack_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, list)
                        self.update_TX_Log(chr(0x04), [2, list[2]])
                elif msg_op == chr(0x05):
                    self.speed_data = self.db.get_speed_data(sync_time=self.sync_time, lane=self.lane_num, cnum=self.category_num, host=self.db_ip, port=int(self.db_port), user=self.db_id, password=self.db_pw, db=self.db_name)
                    if self.speed_data:
                        # print
                        print("0x05 차로 카테고리별 속도: ", self.speed_data)
                        if self.use_category_speed:
                            self.sock.send_05_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, self.speed_data)
                            self.update_TX_Log(chr(0x05), [1])
                elif msg_op == chr(0x07):
                    self.ntraffic_data = self.db.get_ntraffic_data(lane=self.lane_num, host=self.db_ip, port=int(self.db_port), user=self.db_id, password=self.db_pw, db=self.db_name)
                    if self.ntraffic_data:
                        # print
                        print("0x07 누적교통량: ", self.ntraffic_data)
                        if self.use_ntraffic:
                            self.sock.send_07_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, self.ntraffic_data)
                            self.update_TX_Log(chr(0x07), [1])
                elif msg_op == chr(0x0C):
                    self.device_sync(msg_op, d_recv_msg)
                    self.sock.send_0C_res_msg(self.local_ip, self.center_ip, self.controller_type,
                                              self.controller_index)
                    self.update_TX_Log(chr(0x0C), [1])
                elif msg_op == chr(0x0D):
                    self.sock.send_0D_res_msg(self.local_ip, self.center_ip, self.controller_type,
                                              self.controller_index)
                    self.update_TX_Log(chr(0x0D), [1])
                elif msg_op == chr(0x0E):
                    self.device_sync(msg_op, d_recv_msg)
                    self.sock.send_0E_res_msg(self.local_ip, self.center_ip, self.controller_type,
                                              self.controller_index)
                    self.update_TX_Log(chr(0x0E), [1])
                elif msg_op == chr(0x0F):
                    index = int(ord(d_recv_msg[44]))
                    self.sock.send_0F_res_msg(self.local_ip, self.center_ip, self.controller_type,
                                              self.controller_index, index,
                                              self.lane_num, self.collect_cycle, self.category_num, self.use_ntraffic,
                                              self.use_category_speed, self.use_unexpected)
                    self.update_TX_Log(chr(0x0F), [1])
                elif msg_op == chr(0x11):
                    request_time = time.time()
                    if self.connect_time is not None:
                        self.sock.send_11_res_msg(self.local_ip, self.center_ip, self.controller_type,
                                                  self.controller_index, self.connect_time, request_time)
                        self.update_TX_Log(chr(0x11), [1])
                    else:
                        list = [False, chr(0x11), chr(0xFF)]
                        self.sock.send_nack_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, list)
                        self.update_TX_Log(chr(0x11), [2, list[2]])
                elif msg_op == chr(0x13):
                    self.sock.send_13_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, d_recv_msg)
                    self.update_TX_Log(chr(0x13), [1])

                elif msg_op == chr(0x15):
                    version_list = self.db.get_version_num(host=self.db_ip, port=int(self.db_port), user=self.db_id, password=self.db_pw, db=self.db_name)
                    if version_list:
                        self.sock.send_15_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, version_list)
                        self.update_TX_Log(chr(0x15), [1])
                    else:
                        list = [False, chr(0x15), chr(0x06)]
                        self.sock.send_nack_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, list)
                        self.update_TX_Log(chr(0x15), [2, list[2]])

                elif msg_op == chr(0x16):
                    self.individual_traffic_data = self.db.get_individual_traffic_data(cycle=self.collect_cycle, sync_time=self.sync_time, lane=self.lane_num, host=self.db_ip, port=int(self.db_port), user=self.db_id, password=self.db_pw, db=self.db_name)
                    if self.individual_traffic_data != [] and self.frame_number_16 is not None:
                        # print
                        print("0x16 개별차랑: ", self.individual_traffic_data)
                        self.sock.send_16_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, self.frame_number_16, self.individual_traffic_data)
                        self.update_TX_Log(chr(0x16), [1])
                        # self.frame_number_16 = None
                    else:
                        list = [False, chr(0x16), chr(0x06)]
                        self.sock.send_nack_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, list)
                        self.update_TX_Log(chr(0x16), [2, list[2]])

                elif msg_op == chr(0x17):
                    cap = cv2.VideoCapture(self.ui.ImgURL_Edit.text())
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
                    _, img = cap.read()
                    if str(type(img)) != "<class 'NoneType'>":
                        self.sock.send_17_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, img)
                        self.update_TX_Log(chr(0x17), [1])
                    else:
                        list = [False, chr(0x17), chr(0x06)]
                        self.sock.send_nack_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, list)
                        self.update_TX_Log(chr(0x17), [2, list[2]])


                elif msg_op == chr(0x18):
                    result = self.device_sync(msg_op, d_recv_msg)
                    if True in result:
                        self.sock.send_18_res_msg(self.local_ip, self.center_ip, self.controller_type,
                                                  self.controller_index)
                        self.update_TX_Log(chr(0x18), [1])
                    else:
                        list = result
                        self.sock.send_nack_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, list)
                        self.update_TX_Log(chr(0x18), [2, list[2]])
                elif msg_op == chr(0x19):
                    # msg read와 별개의 스레드를 돌면서 돌발 테이블을 계속 확인.
                    # 확인하다가 걸리면 밑에 코드 사용
                    # send함수 파라미터로 보낼 데이터 전송해야함 -> db모듈에서 get
                    if self.use_unexpected == 1:
                        self.sock.send_19_res_msg(self.local_ip, self.center_ip, self.controller_type,
                                                  self.controller_index)
                        self.update_TX_Log(chr(0x19), [1])
                elif msg_op == chr(0x1E):
                    self.controllerBox_state_list = self.db.get_controllerBox_state_data(host=self.db_ip, port=int(self.db_port), user=self.db_id, password=self.db_pw, db=self.db_name)
                    if self.controllerBox_state_list:
                        self.sock.send_1E_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, self.controllerBox_state_list)
                        self.update_TX_Log(chr(0x1E), [1])
                    else:
                        list = [False, chr(0x1E), chr(0x06)]
                        self.sock.send_nack_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, list)
                        self.update_TX_Log(chr(0x1E), [2, list[2]])

            elif destination_ip == self.center_ip:
                print("msg   : [", recv_msg.decode('utf-16'), "]")
            else:
                print("TX_msg: [", recv_msg.decode('utf-16'), "]")
        else:
            self.center_ip = d_recv_msg[0:15]
            list = result
            self.sock.send_nack_res_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index, list)
            self.update_TX_Log(chr(0xFF), [2, list[2]])
    # endregion

    def request_check_timer(self):
        if self.client_connect:
            now_time = time.time()
            time_delay = now_time - self.client_request_time
            # print("delay: ", time_delay)

            if (time_delay > 300) and self.fe_check:
                self.sock.send_FE_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index)
                self.update_TX_Log(chr(0xFE), [0])
                self.fe_send_time = time.time()
                self.fe_check = False

            if not self.fe_check:
                fe_delay = now_time - self.fe_send_time
                if (fe_delay > 5) and (self.fe_num < 2):
                    self.sock.send_FE_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index)
                    self.update_TX_Log(chr(0xFE), [0])
                    self.fe_send_time = time.time()
                    self.fe_num += 1
                # else:
                #     self.client_connect = False
                #     self.fe_num = 0
            if self.fe_num == 2:
                self.client_connect = False
                self.fe_num = 0
                self.fe_check = True

        else:
            print("Waiting for Client...")
            self.update_Statusbar_text("Waiting for Client...")

    def device_sync(self, op, msg):
        lane = 1
        # if op == chr(0x01):
        #     self.frame_number_set = msg[44]
        if op == chr(0x0C):
            self.lane_num = 6
            self.collect_cycle = 30
            self.category_num = [0, 11, 21, 31, 41, 51, 61, 71, 81, 91, 101, 111]
            self.use_ntraffic = 1
            self.use_category_speed = 1
            self.use_unexpected = 1
            # 이외의 설정값 등 리셋
        elif op == chr(0x0E):
            index = int(ord(msg[44]))
            # 차로 지정
            if index == 1:
                data = msg[45:]
                data_1 = int(ord(data[0]))
                data_2 = int(ord(data[1]))
                if data_1 != 0:  # 1byte
                    for i in range(0, 8):
                        if (data_1 >> i) & 0x01 == 0x01:
                            self.lane_num = (8-i)
                else:  # 2 byte
                    for i in range(0, 8):
                        if (data_2 >> i) & 0x01 == 0x01:
                            self.lane_num = (8 - i) + 8
            # 수집 주기
            elif index == 3:
                data = int(ord(msg[45]))
                self.collect_cycle = data
            # 차량 속도 구분
            elif index == 5:
                data = msg[45:]
                print(len(data))
                for i in range(len(data)):
                    self.category_num[i] = int(ord(data[i]))
            # 누적 교통량
            elif index == 7:
                data = int(ord(msg[45]))
                self.use_ntraffic = data
            # 속도 데이터 (카테고리)
            elif index == 9:
                data = int(ord(msg[45]))
                self.use_category_speed = data
            # 돌발 사용 여부
            elif index == 19:
                data = int(ord(msg[45]))
                self.use_unexpected = data
        elif op == chr(0x18):
            data = msg[44:]
            day_list = list()
            for i in data:
                temp = hex(ord(i))
                day_list.append(temp[2:])
            try:
                self.ot.win_set_time(day_list)
                return [True]
            except Exception as e:
                return [False, chr(0x18), chr(0x01)]

        parameter_list = [self.lane_num, self.collect_cycle, self.category_num, self.use_ntraffic, self.use_category_speed, self.use_unexpected]
        self.db.set_paramete_data(parameter_list=parameter_list, host=self.db_ip, port=int(self.db_port), user=self.db_id, password=self.db_pw, db=self.db_name)

    # region test send msg
    # def op_FF_btn_click(self):
    #     print("FF btn_click")
    #     self.sock.send_FF_msg()
    #
    # def op_FE_btn_click(self):
    #     print("FE btn_click")
    #     self.sock.send_FE_msg(self.local_ip, self.center_ip, self.controller_type, self.controller_index)
    #
    # def op_01_btn_click(self):
    #     print("01 btn_click")
    #     self.sock.send_01_msg()
    #
    # def op_04_btn_click(self):
    #     print("04 btn_click")
    #     self.sock.send_04_msg()
    #
    # def op_05_btn_click(self):
    #     print("05 btn_click")
    #     self.sock.send_05_msg()
    #
    # def op_07_btn_click(self):
    #     print("07 btn_click")
    #     self.sock.send_07_msg()
    #
    # def op_0C_btn_click(self):
    #     print("0C btn_click")
    #     self.sock.send_0C_msg()
    #
    # def op_0D_btn_click(self):
    #     print("0D btn_click")
    #     self.sock.send_0D_msg()
    #
    # def op_0E_btn_click(self):
    #     print("0E btn_click")
    #     self.sock.send_0E_msg()
    #
    # def op_0F_btn_click(self):
    #     print("0F btn_click")
    #     self.sock.send_0F_msg()
    #
    # def op_11_btn_click(self):
    #     print("11 btn_click")
    #     self.sock.send_11_msg()
    #
    # def op_12_btn_click(self):
    #     print("12 btn_click")
    #
    # def op_13_btn_click(self):
    #     print("13 btn_click")
    #     self.sock.send_13_msg()
    #
    # def op_15_btn_click(self):
    #     print("15 btn_click")
    #     self.sock.send_15_msg()
    #
    # def op_16_btn_click(self):
    #     print("16 btn_click")
    #     self.sock.send_16_msg()
    #
    # def op_17_btn_click(self):
    #     print("17 btn_click")
    #     self.sock.send_17_msg()
    #
    # def op_18_btn_click(self):
    #     print("18 btn_click")
    #     self.sock.send_18_msg()
    #
    # def op_19_btn_click(self):
    #     print("19 btn_click")
    #
    # def op_1E_btn_click(self):
    #     print("1E btn_click")
    #     self.sock.send_1E_msg()

    # endregion

    # region ui update
    def update_Statusbar_text(self, msg):
        self.ui.status_bar.setText(msg)

    def update_RX_Log(self, OPCODE, list):
        log_list = []

        date_s = (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        numRows = self.ui.rx_table.rowCount()
        self.ui.rx_table.insertRow(numRows)
        # Add text to the row
        self.ui.rx_table.setItem(numRows, 0, QTableWidgetItem(date_s))
        self.ui.rx_table.setItem(numRows, 1, QTableWidgetItem("0x{:02X}".format(ord(OPCODE))))
        log_list.append(date_s)
        log_list.append("0x{:02X}".format(ord(OPCODE)))
        # list[0] { 0 : None, 1 : ACK, 2 : NACK}
        if list[0] == 1:
            self.ui.rx_table.setItem(numRows, 2, QTableWidgetItem('ACK'))
            log_list.append('ACK')
        elif list[0] == 2:
            self.ui.rx_table.setItem(numRows, 2, QTableWidgetItem('NACK'))
            log_list.append('NACK')
            if list[1] == chr(0x01):
                self.ui.rx_table.setItem(numRows, 3, QTableWidgetItem('System Error'))
                log_list.append('System Error')
            elif list[1] == chr(0x02):
                self.ui.rx_table.setItem(numRows, 3, QTableWidgetItem('Data Length Error'))
                log_list.append('Data Length Error')
            elif list[1] == chr(0x03):
                self.ui.rx_table.setItem(numRows, 3, QTableWidgetItem('CSN Error'))
                log_list.append('CSN Error')
            elif list[1] == chr(0x04):
                self.ui.rx_table.setItem(numRows, 3, QTableWidgetItem('OP Code Error'))
                log_list.append('OP Code Error')
            elif list[1] == chr(0x05):
                self.ui.rx_table.setItem(numRows, 3, QTableWidgetItem('Out of Index Error'))
                log_list.append('Out of Index Error')
            elif list[1] == chr(0x06):
                self.ui.rx_table.setItem(numRows, 3, QTableWidgetItem('Not Ready Error'))
                log_list.append('Not Ready Error')
            elif list[1] == chr(0xFF):
                self.ui.rx_table.setItem(numRows, 3, QTableWidgetItem('Error'))
                log_list.append('Error')
            else:
                self.ui.rx_table.setItem(numRows, 3, QTableWidgetItem('Reserved'))
                log_list.append('Reserved')

        if self.m_log_save:
            self.log.log_save(log_list)
            self.db.save_Log_data(msg_list=log_list, host=self.db_ip, port=int(self.db_port), user=self.db_id, password=self.db_pw, db=self.db_name)
        self.ui.rx_table.scrollToBottom()

    def update_TX_Log(self, OPCODE, list):
        log_list = []

        date_s = (datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
        numRows = self.ui.tx_table.rowCount()
        self.ui.tx_table.insertRow(numRows)
        # Add text to the row
        self.ui.tx_table.setItem(numRows, 0, QTableWidgetItem(date_s))
        self.ui.tx_table.setItem(numRows, 1, QTableWidgetItem("0x{:02X}".format(ord(OPCODE))))
        log_list.append(date_s)
        log_list.append("0x{:02X}".format(ord(OPCODE)))
        # list[0] { 0 : None, 1 : ACK, 2 : NACK}
        if list[0] == 1:
            self.ui.tx_table.setItem(numRows, 2, QTableWidgetItem('ACK'))
            log_list.append('ACK')
        elif list[0] == 2:
            self.ui.tx_table.setItem(numRows, 2, QTableWidgetItem('NACK'))
            log_list.append('NACK')
            if list[1] == chr(0x01):
                self.ui.tx_table.setItem(numRows, 3, QTableWidgetItem('System Error'))
                log_list.append('System Error')
            elif list[1] == chr(0x02):
                self.ui.tx_table.setItem(numRows, 3, QTableWidgetItem('Data Length Error'))
                log_list.append('Data Length Error')
            elif list[1] == chr(0x03):
                self.ui.tx_table.setItem(numRows, 3, QTableWidgetItem('CSN Error'))
                log_list.append('CSN Error')
            elif list[1] == chr(0x04):
                self.ui.tx_table.setItem(numRows, 3, QTableWidgetItem('OP Code Error'))
                log_list.append('OP Code Error')
            elif list[1] == chr(0x05):
                self.ui.tx_table.setItem(numRows, 3, QTableWidgetItem('Out of Index Error'))
                log_list.append('Out of Index Error')
            elif list[1] == chr(0x06):
                self.ui.tx_table.setItem(numRows, 3, QTableWidgetItem('Not Ready Error'))
                log_list.append('Not Ready Error')
            elif list[1] == chr(0xFF):
                self.ui.tx_table.setItem(numRows, 3, QTableWidgetItem('Error'))
                log_list.append('Error')
            else:
                self.ui.tx_table.setItem(numRows, 3, QTableWidgetItem('Reserved'))
                log_list.append('Reserved')

        if self.m_log_save:
            self.log.log_save(log_list)
            self.db.save_Log_data(msg_list=log_list, host=self.db_ip, port=int(self.db_port), user=self.db_id, password=self.db_pw, db=self.db_name)
        self.ui.tx_table.scrollToBottom()

    # endregion