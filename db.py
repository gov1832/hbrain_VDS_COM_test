# import pymysql
import pymssql
from datetime import datetime, timedelta
import time
import math

from calc import CALC_function


class DB_function:
    def __init__(self):
        super().__init__()
        self.calc = CALC_function()

        self.distlong_diff = 30
        # print(self.get_congestion_data(congestion=43, cycle=30, zone=60, sync_time=time.time(), host='127.0.0.1', port=1433, user='sa', password='hbrain0372!', db='hbrain_vds', charset='utf8'))
        print(self.get_location_data(host='127.0.0.1', port=1433, user='sa', password='hbrain0372!', db='hbrain_vds', charset='utf8'))
    # DB 초기 데이터베이스 및 테이블 존재 여부 및 생성
    def create_init_DB(self, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        db_connect = pymssql.connect(server=host, port=port, user=user, password=password, charset=charset, autocommit=True)
        cur = db_connect.cursor()
        use_db = False
        while not use_db:
            sql = 'select name from sys.sysdatabases'
            cur.execute(sql)
            result = cur.fetchall()
            for result_db in result:
                if result_db[0] == db:
                    print("database ", result_db[0], " fine")
                    use_db = True
                    break

            if not use_db:
                print("database ", db, " not find! ")
                sql = "create database " + db
                try:
                    cur.execute(sql)
                    print(sql)
                except Exception as e:
                    print("create database error")
            time.sleep(1)
        db_connect.close()

        # region sql 구문
        create_obj_info = "IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='obj_info' and xtype='U') CREATE TABLE obj_info(time datetime NOT NULL, ID TINYINT NOT NULL, DistLat FLOAT default NULL, DistLong FLOAT default NULL, VrelLat FLOAT default NULL, VrelLong FLOAT default NULL, Velocity FLOAT default NULL, RCS FLOAT default NULL, ProbOfExist TINYINT default NULL, ArelLat FLOAT default NULL, ArelLong FLOAT default NULL, Class TINYINT default NULL, Length FLOAT default NULL, Width FLOAT default NULL, Zone TINYINT default NULL, Lane TINYINT default NULL, PRIMARY KEY(time, ID));"
        create_traffic_detail = "IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Traffic_Detail' and xtype='U') CREATE TABLE Traffic_Detail(time datetime NOT NULL, ID TINYINT NOT NULL, Velocity FLOAT default NULL, Zone TINYINT default NULL, category TINYINT default NULL, PRIMARY KEY(time, ID));"
        create_traffic_info = "IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Traffic_Info' and xtype='U') CREATE TABLE Traffic_Info(Lane TINYINT NOT NULL, nTraffic INT default NULL, totalVelocity FLOAT default NULL, PRIMARY KEY(Lane));"
        create_outbreak = "IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='outbreak' and xtype='U') CREATE TABLE outbreak(time datetime NOT NULL, idx TINYINT NOT NULL, Class TINYINT NOT NULL, Zone TINYINT default NULL, DistLat FLOAT default NULL, DistLong FLOAT default NULL, Distance FLOAT default NULL, PRIMARY KEY(time, Idx, Class));"
        create_parameter = "IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Parameter' and xtype='U') CREATE TABLE Parameter(Param TINYINT NOT NULL, Nbyte TINYINT NOT NULL, Data TINYINT default NULL, PRIMARY KEY (Param, Nbyte));"
        create_vds_version = "IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='vds_version' and xtype='U') CREATE TABLE vds_version(time DATE default NULL, version_No TINYINT NOT NULL, release_No TINYINT NOT NULL, year TINYINT default NULL, month TINYINT default NULL, day TINYINT default NULL, PRIMARY KEY (version_No, release_No));"
        create_sw_parameter = "IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='sw_parameter' and xtype='U') CREATE TABLE sw_parameter(Param CHAR(64) NOT NULL, value CHAR(32) default NULL, PRIMARY KEY(param));"
        create_controlBox_status = "IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='controlBox_Status' and xtype='U') CREATE TABLE controlBox_Status(Param CHAR(64) NOT NULL, Data TINYINT default NULL, PRIMARY KEY (Param));"
        create_log_communication = "IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Log_communication' and xtype='U') CREATE TABLE Log_communication(time datetime NOT NULL, opcode CHAR(4) default NULL, acknack CHAR(4) default NULL, reason CHAR(20) default NULL, PRIMARY KEY(time));"

        insert_traffic_info = "INSERT INTO Traffic_Info VALUES(1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0), (5, 0, 0), (6, 0, 0);"
        insert_parameter = "INSERT INTO Parameter VALUES(1, 0, 4), (1, 1, 0), (3, 0, 30), (5, 0, 0), (5, 1, 11), (5, 2, 21), (5, 3, 31), (5, 4, 41), (5, 5, 51), (5, 6, 61), (5, 7, 71), (5, 8, 81), (5, 9, 91), (5, 10, 101), (5, 11, 111), (7, 0, 1), (9, 0, 1), (19, 0, 1);"
        insert_vds_version = "INSERT INTO vds_version VALUES('2022-07-25', 1, 1, 22, 7, 25), ('2022-08-02', 1, 2, 22, 8, 2);"
        # 점유율 구간
        insert_sw_parameter_1 = "INSERT INTO sw_parameter VALUES" \
                              "('1_occupancy_min', '45'), ('1_occupancy_max', '70')," \
                              "('2_occupancy_min', '45'), ('2_occupancy_max', '75')," \
                              "('3_occupancy_min', '45'), ('3_occupancy_max', '80')," \
                              "('4_occupancy_min', '35'), ('4_occupancy_max', '75')," \
                              "('5_occupancy_min', '35'), ('5_occupancy_max', '80')," \
                              "('6_occupancy_min', '35'), ('6_occupancy_max', '85');"
        # 교통 정보 수집
        insert_sw_parameter_2 = "INSERT INTO sw_parameter VALUES('1_traffic', '60'), ('2_traffic', '55');"
        # 차선 정보
        insert_sw_parameter_3 = "INSERT INTO sw_parameter VALUES" \
                                "('1_lanePoint', '3.3'), " \
                                "('2_lanePoint', '3.3'), " \
                                "('3_lanePoint', '3.3'), " \
                                "('4_lanePoint', '3.3'), " \
                                "('5_lanePoint', '3.3'), " \
                                "('6_lanePoint', '3.3');"
        insert_sw_parameter_4 = "INSERT INTO sw_parameter VALUES" \
                                "('1_laneShift', '0'), " \
                                "('2_laneShift', '0'), " \
                                "('3_laneShift', '0'), " \
                                "('4_laneShift', '0'), " \
                                "('5_laneShift', '0'), " \
                                "('6_laneShift', '0'), " \
                                "('7_laneShift', '0'), " \
                                "('8_laneShift', '0'), " \
                                "('9_laneShift', '0');"
        insert_sw_parameter_5 = "INSERT INTO sw_parameter VALUES('radarAngle', '0');"
        insert_sw_parameter_6 = "INSERT INTO sw_parameter VALUES('radarShift', '0');"
        insert_sw_parameter_7 = "INSERT INTO sw_parameter VALUES('last_time_Cspeed', NULL);"
        insert_sw_parameter_8 = "INSERT INTO sw_parameter VALUES('RADAR_ID', '0'), ('radarAngle', '0'), ('radarShift', '0.0');"
        insert_sw_parameter_9 = "INSERT INTO sw_parameter VALUES('doKalman', '1'),('doInterpolation', '1'),('doTracking', '1');"
        insert_sw_parameter_10 = "INSERT INTO sw_parameter VALUES('PTZ_IP', '192.168.0.64'),('PTZ_PORT', '8000'),('PTZ_ID', 'admin'),('PTZ_PW', 'hbrain0372!');"
        insert_sw_parameter_11 = "INSERT INTO sw_parameter VALUES('DB_IP', '127.0.0.1'),('DB_PORT', '1433'),('DB_ID', 'sa'),('DB_PW', 'hbrain0372!'),('DB_DB', 'hbrain_vds');"
        insert_sw_parameter_12 = "INSERT INTO sw_parameter VALUES('SOCKET_IP', NULL),('SOCKET_PORT', '30100');"
        insert_sw_parameter_13 = "INSERT INTO sw_parameter VALUES('congestion_criterion', '50'),('congestion_cycle', '30'), ('zone_criterion', '10');"

        insert_controlbox_status_1 = "INSERT INTO controlBox_Status VALUES('Long_Power_Fail', 0),('Short_Power_Fail', 0),('Default Parameter', 1);"
        insert_controlbox_status_2 = "INSERT INTO controlBox_Status VALUES('Front_Door_Status', 0),('Back_Door_Status', 0),('Fan_Status', 0),('Heater_Stauts', 0),('Image_Status', 0),('Reset_Status', 0);"
        insert_controlbox_status_3 = "INSERT INTO controlBox_Status VALUES('Temperature', 24),('Input_Voltage', 220),('Output_Voltage', 12);"
        # endregion

        if use_db:
            db_conn = pymssql.connect(server=host, port=port, user=user, password=password, database=db, charset='utf8', autocommit=True)
            cur_conn = db_conn.cursor()
            try:
                cur_conn.execute(create_obj_info)
            except Exception as e:
                print("err create_obj_info: ", e)

            try:
                cur_conn.execute(create_traffic_detail)
            except Exception as e:
                print("err create_traffic_detail: ", e)

            try:
                cur_conn.execute(create_traffic_info)
            except Exception as e:
                print("err create_traffic_info: ", e)

            try:
                cur_conn.execute(create_outbreak)
            except Exception as e:
                print("err create_outbreak: ", e)

            try:
                cur_conn.execute(create_parameter)
            except Exception as e:
                print("err create_parameter: ", e)

            try:
                cur_conn.execute(create_vds_version)
            except Exception as e:
                print("err create_vds_version: ", e)

            try:
                cur_conn.execute(create_sw_parameter)
            except Exception as e:
                print("err create_sw_parameter: ", e)

            try:
                cur_conn.execute(create_controlBox_status)
            except Exception as e:
                print("err create_controlBox_status: ", e)

            try:
                cur_conn.execute(create_log_communication)
            except Exception as e:
                print("err create_log_communication: ", e)

            try:
                cur_conn.execute(insert_traffic_info)
            except Exception as e:
                print("err insert_traffic_info: ", e)

            try:
                cur_conn.execute(insert_parameter)
            except Exception as e:
                print("err insert_parameter: ", e)

            try:
                cur_conn.execute(insert_vds_version)
            except Exception as e:
                print("err insert_vds_version: ", e)

            try:
                cur_conn.execute(insert_sw_parameter_1)
            except Exception as e:
                print("err insert_sw_parameter_1: ", e)

            try:
                cur_conn.execute(insert_sw_parameter_2)
            except Exception as e:
                print("err insert_sw_parameter_2: ", e)

            try:
                cur_conn.execute(insert_sw_parameter_3)
            except Exception as e:
                print("err insert_sw_parameter_3: ", e)

            try:
                cur_conn.execute(insert_sw_parameter_4)
            except Exception as e:
                print("err insert_sw_parameter_4: ", e)

            try:
                cur_conn.execute(insert_sw_parameter_5)
            except Exception as e:
                print("err insert_sw_parameter_5: ", e)

            try:
                cur_conn.execute(insert_sw_parameter_6)
            except Exception as e:
                print("err insert_sw_parameter_6: ", e)

            try:
                cur_conn.execute(insert_sw_parameter_7)
            except Exception as e:
                print("err insert_sw_parameter_7: ", e)

            try:
                cur_conn.execute(insert_sw_parameter_8)
            except Exception as e:
                print("err insert_sw_parameter_8: ", e)

            try:
                cur_conn.execute(insert_sw_parameter_9)
            except Exception as e:
                print("err insert_sw_parameter_9: ", e)

            try:
                cur_conn.execute(insert_sw_parameter_10)
            except Exception as e:
                print("err insert_sw_parameter_10: ", e)

            try:
                cur_conn.execute(insert_sw_parameter_11)
            except Exception as e:
                print("err insert_sw_parameter_11: ", e)

            try:
                cur_conn.execute(insert_sw_parameter_12)
            except Exception as e:
                print("err insert_sw_parameter_12: ", e)

            try:
                cur_conn.execute(insert_sw_parameter_13)
            except Exception as e:
                print("err insert_sw_parameter_13: ", e)

            try:
                cur_conn.execute(insert_controlbox_status_1)
            except Exception as e:
                print("err insert_controlbox_status_1: ", e)

            try:
                cur_conn.execute(insert_controlbox_status_2)
            except Exception as e:
                print("err insert_controlbox_status_2: ", e)

            try:
                cur_conn.execute(insert_controlbox_status_3)
            except Exception as e:
                print("err insert_controlbox_status_3: ", e)
            db_conn.close()

    # DB 연결 체크 함수
    def db_connection_check(self, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        try:
            db_connect = pymssql.connect(server=host, port=port, user=user, password=password, database=db,
                                         charset=charset)
            cur = db_connect.cursor()
            sql = 'use ' + db
            cur.execute(sql)

            db_connect.close()
            return True
        except Exception as e:
            print("err db_connection_check : ", e)
            return False

    # region get data
    # socket ip & port
    def get_socket_info(self, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        socket_info = []
        try:
            db_connect = pymssql.connect(server=host, port=port, user=user, password=password, database=db, charset=charset)
            cur = db_connect.cursor()

            sql = "select value from sw_parameter where param='SOCKET_IP'"
            cur.execute(sql)
            result = cur.fetchone()
            if result[0] is None:
                socket_info.append(None)
            else:
                socket_info.append(result[0].replace(" ", ""))

            sql = "select value from sw_parameter where param='SOCKET_PORT'"
            cur.execute(sql)
            result = cur.fetchone()
            socket_info.append(int(result[0]))

            db_connect.close()
        except Exception as e:
            print("err get_socket_info : ", e)

        return socket_info

    # 지정체 관련 값
    def get_congestion_info(self, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        value_list = [50, 10, 30]
        try:
            db_connect = pymssql.connect(server=host, port=port, user=user, password=password, database=db, charset=charset)
            cur = db_connect.cursor()

            sql = "select value from sw_parameter where param='congestion_criterion'"
            cur.execute(sql)
            result = cur.fetchone()
            value_list[0] = (int(result[0]))

            sql = "select value from sw_parameter where param='zone_criterion'"
            cur.execute(sql)
            result = cur.fetchone()
            value_list[1] = (int(result[0]))

            sql = "select value from sw_parameter where param='congestion_cycle'"
            cur.execute(sql)
            result = cur.fetchone()
            value_list[2] = (int(result[0]))

            db_connect.close()
        except Exception as e:
            print("err get_socket_info : ", e)

        return value_list

    # 버전
    def get_version_num(self, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        version_list = []
        try:
            db_connect = pymssql.connect(server=host, port=port, user=user, password=password, database=db,
                                         charset=charset)
            cur = db_connect.cursor()
            sql = 'SELECT time FROM vds_version'
            cur.execute(sql)

            result = []
            for i in cur:
                result.append(i[0])
            result.sort(reverse=True)

            sql = "SELECT * FROM vds_version WHERE time='" + str(result[0]) + "';"
            cur.execute(sql)
            for i in cur:
                version_list.append(i)

            db_connect.close()
        except Exception as e:
            print("err get_version_num : ", e)

        return version_list

    # 교통량 데이터
    def get_traffic_data(self, cycle=30, sync_time=None, lane=6, host=None, port=None, user=None, password=None,
                         db=None, charset='utf8'):
        traffic_data = []

        try:
            if sync_time is None:
                print('nack')
            else:
                temp = time.localtime(sync_time - cycle)
                data_start = time.strftime("%Y-%m-%d %H:%M:%S", temp)

                # 교통량 및 속도
                Tspeed_data = self.calc.Tspeed_data(data_start, lane, host, port, user, password, db, charset)

                # 점유율
                occu = self.get_occupancy_interval_data(lane, host, port, user, password, db, charset)
                share_data = self.calc.share_data(occu, data_start, cycle, lane, host, port, user, password, db,
                                                  charset)

                # 상하행
                lane_way = self.calc.lane_way(lane)

                # 전송 데이터 종합
                if lane >= 1:
                    for i in range(lane):
                        traffic_temp = [Tspeed_data[0][i], Tspeed_data[1][i], share_data[i], lane_way[i]]
                        traffic_data.append(traffic_temp)

        except Exception as e:
            print("err get_traffic_data : ", e)

        return traffic_data

    # 개별 차량 데이터
    def get_individual_traffic_data(self, cycle=30, sync_time=None, lane=6, host=None, port=None, user=None,
                                    password=None, db=None, charset='utf8'):
        individual_traffic_data = []

        try:
            if sync_time is None:
                print('nack')
            else:
                temp = time.localtime(sync_time - cycle)
                data_start = time.strftime("%Y-%m-%d %H:%M:%S", temp)

                # 개별 차량 데이터
                individual_traffic_data = self.calc.Icar_data(data_start, lane, host, port, user, password, db, charset)

        except Exception as e:
            print("err get_individual_traffic_data : ", e)

        return individual_traffic_data

    # 차선별 누적 교통량 데이터
    def get_ntraffic_data(self, lane=6, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        ntraffic_data = []

        try:
            db_connect = pymssql.connect(server=host, port=port, user=user, password=password, database=db,
                                         charset=charset,
                                         autocommit=True)
            cur = db_connect.cursor()
            # 차선 오름차순으로 데이터 select
            sql = "SELECT * FROM traffic_info order by Lane asc"
            cur.execute(sql)
            result = cur.fetchall()
            for i in range(lane):
                ntraffic_data.append(result[i][1])

            # 초기화 부분
            # mysql
            # sql = "update traffic_info set nTraffic=0, totalVelocity=0 where Lane;"
            # mssql
            sql = "update traffic_info set nTraffic=0, totalVelocity=0"
            cur.execute(sql)
            db_connect.commit()
            db_connect.close()
        except Exception as e:
            print("err: ", e)

        return ntraffic_data

    # 카테고리(속도) 기준 차선별 교통량
    def get_speed_data(self, sync_time=None, lane=6, cnum=[], host=None, port=None, user=None, password=None, db=None,
                       charset='utf8'):
        speed_data = []

        try:
            speed_data = self.calc.Cspeed_data(sync_time, cnum, lane, host, port, user, password, db, charset)
            # print(speed_data)
        except Exception as e:
            print("err get_ntraffic_data : ", e)

        return speed_data

    # 함체 정보 데이터
    def get_controllerBox_state_data(self, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        controllerBox_state_list = []
        try:
            db_connect = pymssql.connect(server=host, port=port, user=user, password=password, database=db,
                                         charset=charset)
            cur = db_connect.cursor()
            sql = "SELECT * FROM controllerbox_state;"
            cur.execute(sql)
            result = cur.fetchall()
            for i in range(1, len(result[0])):
                controllerBox_state_list.append(result[0][i])

            db_connect.close()
        except Exception as e:
            print("err get_controllerBox_state_data : ", e)

        return controllerBox_state_list

    # 지정체 데이터
    def get_congestion_data(self, congestion=50, cycle=30, zone=10, sync_time=None, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        congestion_list = []
        try:
            if sync_time is None:
                print('nack')
            else:
                temp = time.localtime(sync_time - cycle)
                data_start = time.strftime("%Y-%m-%d %H:%M:%S", temp)
                zone_data = self.calc.congestion_data(zone=zone, data_start=data_start, host=host, port=port, user=user, password=password, db=db, charset=charset)
                # zone_data = self.calc.congestion_data(zone=zone, data_start='2022-10-06 10:00:00', host=host, port=port, user=user, password=password, db=db, charset=charset)
                if zone_data:
                    for i, lane_data in enumerate(zone_data):
                        for j, a_velocity in enumerate(lane_data):
                            if a_velocity < congestion and a_velocity != 0:
                                # i+1 = 차선. j = 구역
                                congestion_list.append([i+1, j])
                else:
                    print("nack")

                # print("차선별 데이터/ ", zone_data)
                # print("지정체 데이터/ ", congestion_list)
        except Exception as e:
            print("err get_congestion_data : ", e)

        return congestion_list

    # 돌발 상황 정보
    def get_outbreak(self, lane=6, zone_num=None, last_time=None, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        outbreak = []
        try:
            db_connect = pymssql.connect(server=host, port=port, user=user, password=password, database=db,
                                         charset=charset,
                                         autocommit=True)
            cur = db_connect.cursor()

            # region 차선 간격 = lane_point
            sql = "SELECT value From sw_parameter WHERE param LIKE '%lanePoint' order by param asc;"
            cur.execute(sql)
            result = cur.fetchall()
            lane_point = []
            for data in result:
                lane_point.append(float(data[0]))
            # endregion

            sql = "SELECT * FROM outbreak "
            if last_time is None:
                temp = datetime.now() - timedelta(seconds=10) # 마지막 시간이 없으면 현재 시간보다 10초 전 데이터
                now_time = temp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                # print("start : ", now_time)
                sql += "WHERE time>='" + now_time + "' order by time desc"
            else:
                # 테이블 마지막으로 읽은 시간으로부터의 데이터
                data_start = last_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                # print("start : ", data_start)
                sql += "WHERE time>='" + data_start + "' order by time desc"

            # print(sql)
            cur.execute(sql)
            result = cur.fetchall()

            # print(result)
            # 상/하행
            if lane > 0:
                lane_half = lane / 2

                if result:
                    for data in result:
                        # out = [time, lane, class, distance, 상하행]
                        out = []
                        out.append(data[0]) # time
                        if data[3] is not None:
                            out.append(data[3]) # lane
                        else:
                            out.append(1)
                        out.append(data[2]) # class
                        out.append(data[6]) # distance
                        if data[3] is not None:
                            if data[3] <= lane_half:
                                out.append(0)
                            elif lane_half < data[3] <= lane:
                                out.append(1)
                        else:
                            out.append(0)
                        outbreak.append(out)
                    # for i in range(lane):
                    #     for j in range(len(result)):
                    #         if result[j][1] == (i + 1):
                    #             out = []
                    #             out.append(result[j][0]) # time
                    #             if result[j][3] is None:
                    #                 out.append(1)
                    #             else:
                    #                 out.append(result[j][3]) # lane
                    #             out.append(result[j][2]) # class
                    #             out.append(result[j][6]) # distance
                    #             if result[j][3] is None:
                    #                 if result[j][3] <= lane_half:
                    #                     out.append(0)
                    #                 elif lane_half < result[j][3] <= lane:
                    #                     out.append(1)
                    #             else:  # 값 오류
                    #                 out.append(0)
                    #                 continue
                    #             outbreak.append(out)

                # print("돌발 건수: ", len(outbreak))
                # 초기화 부분, 추후 활성화
                # mysql
                # sql = "truncate outbreak"
                # mssql
                # sql = "truncate table outbreak;"
                # cur.execute(sql)
                # db_connect.commit()
            db_connect.close()
        except Exception as e:
            print("err get_outbreak : ", e)
        return outbreak
    def get_location_data(self, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        result = []
        try:
            db_connect = pymssql.connect(server=host, port=port, user=user, password=password, database=db, charset=charset, autocommit=True)
            cur = db_connect.cursor()

            # 경도
            sql_2 = "SELECT value FROM sw_parameter WHERE param='longitude'"
            cur.execute(sql_2)
            temp = cur.fetchall()
            result.append(str(temp[0][0])[:10])

            # 위도
            sql_1 = "SELECT value FROM sw_parameter WHERE param='latitude'"
            cur.execute(sql_1)
            temp = cur.fetchall()
            result.append(str(temp[0][0])[:10])


            db_connect.close()
        except Exception as e:
            print("error get_location_data : ", e)
        return result

    def get_parameter_data(self, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        lane_num = None
        collect_cycle = None
        category_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        use_ntraffic = None
        use_category_speed = None
        use_unexpected = None
        parameter_list = []

        try:
            db_connect = pymssql.connect(server=host, port=port, user=user, password=password, database=db,
                                         charset=charset,
                                         autocommit=True)
            cur = db_connect.cursor()
            sql = "SELECT * FROM parameter"
            cur.execute(sql)
            result = cur.fetchall()

            for i in range(len(result)):
                if result[i][0] == 1:
                    if (result[i][1] == 0) and result[i][2]:
                        tenp = result[i][2]
                        for i in range(0, 8):
                            if (tenp >> i) & 0x01 == 0x01:
                                lane_num = 8 - i

                    if (result[i][1] == 1) and result[i][2]:
                        tenp = result[i][2]
                        for i in range(0, 8):
                            if (tenp >> i) & 0x01 == 0x01:
                                lane_num = (8 - i) + 8

                elif result[i][0] == 3:
                    collect_cycle = result[i][2]
                elif result[i][0] == 5:
                    category_num[result[i][1]] = result[i][2]
                elif result[i][0] == 7:
                    use_ntraffic = result[i][2]
                elif result[i][0] == 9:
                    use_category_speed = result[i][2]
                elif result[i][0] == 19:
                    use_unexpected = result[i][2]

            db_connect.close()
            parameter_list.append(lane_num)
            parameter_list.append(collect_cycle)
            parameter_list.append(category_num)
            parameter_list.append(use_ntraffic)
            parameter_list.append(use_category_speed)
            parameter_list.append(use_unexpected)
        except Exception as e:
            print("err get_parameter_data : ", e)
        return parameter_list

    def get_occupancy_interval_data(self, lane=6, host=None, port=None, user=None, password=None, db=None,
                                    charset='utf8'):
        occupanvcy_interval_list = []
        try:
            db_connect = pymssql.connect(server=host, port=port, user=user, password=password, database=db,
                                         charset=charset, autocommit=True)
            cur = db_connect.cursor()

            temp_min = []
            temp_max = []
            # min 값 입력
            sql = "SELECT * FROM sw_parameter WHERE param LIKE '%occupancy_min' order by param asc;"
            cur.execute(sql)
            result = cur.fetchall()
            for i in range(lane):
                # result[1] => parameter value
                temp_min.append(int((result[i][1])))
            occupanvcy_interval_list.append(temp_min)

            # max 값 입력
            sql = "SELECT * FROM sw_parameter WHERE param LIKE '%occupancy_max' order by param asc;"
            cur.execute(sql)
            result = cur.fetchall()
            for i in range(lane):
                # result[1] => parameter value
                temp_max.append(int((result[i][1])))
            occupanvcy_interval_list.append(temp_max)

            db_connect.close()
        except Exception as e:
            print("err get_occupancy_interval_data : ", e)
        return occupanvcy_interval_list

    # endregion

    # region set data
    # socket ip & port
    def set_socket_info(self, socket_info=[], host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        try:
            if socket_info == '':
                print("parameter in none")
            else:
                db_connect = pymssql.connect(server=host, port=port, user=user, password=password, database=db,
                                         charset=charset, autocommit=True)
                cur = db_connect.cursor()
                # socket_info = [ip, socket]
                sql_1 = "UPDATE sw_parameter set value='" + str(socket_info[0]) + "' WHERE param='SOCKET_IP'"
                sql_2 = "UPDATE sw_parameter set value='" + str(socket_info[1]) + "' WHERE param='SOCKET_PORT'"

                cur.execute(sql_1)
                cur.execute(sql_2)

                db_connect.close()
        except Exception as e:
            print("error set_socket_info : ", e)

    def set_congestion_info(self, change_list=[], host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        try:
            if change_list == '':
                print("parameter in none")
            else:
                db_connect = pymssql.connect(server=host, port=port, user=user, password=password, database=db,
                                         charset=charset, autocommit=True)
                cur = db_connect.cursor()
                # socket_info = [congestion, zone]
                sql_1 = "UPDATE sw_parameter set value='" + str(change_list[0]) + "' WHERE param='congestion_criterion'"
                sql_2 = "UPDATE sw_parameter set value='" + str(change_list[1]) + "' WHERE param='zone_criterion'"
                sql_3 = "UPDATE sw_parameter set value='" + str(change_list[2]) + "' WHERE param='congestion_cycle'"

                cur.execute(sql_1)
                cur.execute(sql_2)
                cur.execute(sql_3)

                db_connect.close()
        except Exception as e:
            print("error set_congestion_info : ", e)

    def insert_outbreak(self, congestion_list=[], input_time=None, zone=None, zone_num=None, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        # congestion_list = 지정체 구역 = [차선 (1부터), 구역 (0부터)]
        # input_time = 지정체 발생 시간
        # zone = 구역 간격
        # zone_num = 차선별 구역 수
        try:
            if congestion_list == '' or zone is None or input_time is None or zone_num is None:
                print("parameter in none")
            else:
                db_connect = pymssql.connect(server=host, port=port, user=user, password=password, database=db,
                                         charset=charset, autocommit=True)
                cur = db_connect.cursor()

                sql = "SELECT value From sw_parameter WHERE param LIKE '%lanePoint' order by param asc;"
                cur.execute(sql)
                result = cur.fetchall()
                lane_point = []
                for data in result:
                    lane_point.append(float(data[0]))

                # outbreak_time = time.strftime("%Y-%m-%d %H:%M:%S.%f", time.localtime(input_time))[:-3]
                outbreak_time = input_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                for i in range(len(congestion_list)):
                    # zone = congestion_list[i][0]
                    # DistLat
                    # distlat = 0
                    # if (congestion_list[i][0]-1) > 0:
                    #     for j in range(congestion_list[i][0]-1):
                    #         distlat += lane_point[j]
                    # total_distlat = round(distlat + lane_point[congestion_list[i][0]-1]/2, 1)
                    # DistLong
                    total_distlong = round(zone * congestion_list[i][1] + zone/2, 1)
                    sql = "INSERT INTO outbreak VALUES('" + outbreak_time + "', " + str(i) + ", 4, " + str(congestion_list[i][0]) + \
                          ", NULL, " + str(total_distlong) + ", " + str(total_distlong) + ");"
                    # print(sql)
                    cur.execute(sql)

                db_connect.close()
        except Exception as e:
            print("error insert_outbreak : ", e)

    # S/W 파라미터 저장
    def set_paramete_data(self, parameter_list=[], host=None, port=None, user=None, password=None, db=None,
                          charset='utf8'):
        try:
            if parameter_list == '':
                print("parameter in none")
            else:
                lane = 1 << (16 - parameter_list[0])
                lane_1 = lane >> 8
                lane_2 = lane & 0xFF
                list = [lane_1, lane_2]
                for i in range(1, len(parameter_list)):
                    list.append(parameter_list[i])
                print("list: ", list)
                db_connect = pymssql.connect(server=host, port=port, user=user, password=password, database=db,
                                             charset=charset, autocommit=True)
                cur = db_connect.cursor()
                sql = "SELECT Param, Nbyte from parameter ORDER BY Param asc"
                cur.execute(sql)
                index_list = []
                for i in cur:
                    index_list.append((i[0], i[1]))
                index = 0
                for i in range(len(list)):
                    if type(list[i]) == type([]):
                        for j in range(len(list[i])):
                            sql = "UPDATE parameter set Data=" + str(list[i][j]) + " WHERE Param=" + str(
                                index_list[index][0]) + " AND Nbyte=" + str(index_list[index][1]) + ";"
                            index += 1
                            cur.execute(sql)
                    else:
                        sql = "UPDATE parameter set Data=" + str(list[i]) + " WHERE Param=" + str(
                            index_list[index][0]) + " AND Nbyte=" + str(index_list[index][1]) + ";"
                        index += 1
                        cur.execute(sql)

                db_connect.close()
        except Exception as e:
            print("err set_paramete_data : ", e)

    # endregion

    # region save
    def save_Log_data(self, msg_list=[], host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        try:
            if msg_list == '':
                print("parameter in none")
            else:
                db_connect = pymssql.connect(server=host, port=port, user=user, password=password, database=db,
                                             charset=charset, autocommit=True)
                cur = db_connect.cursor()
                sql = ''

                if len(msg_list) == 4:
                    sql = "INSERT INTO Log_communication values('" + msg_list[0] + "', '" + msg_list[1] + "', '" + \
                          msg_list[2] + "', '" + msg_list[3] + "');"
                elif len(msg_list) == 3:
                    sql = "INSERT INTO Log_communication values('" + msg_list[0] + "', '" + msg_list[1] + "', '" + \
                          msg_list[2] + "', '');"
                elif len(msg_list) == 2:
                    sql = "INSERT INTO Log_communication values('" + msg_list[0] + "', '" + msg_list[1] + "', '', '');"

                cur.execute(sql)
                db_connect.close()
        except Exception as e:
            print("err save_Log_data : ", e)
    # endregion
