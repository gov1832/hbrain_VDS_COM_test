import pymysql
from datetime import datetime, timedelta
import time
import math
import datetime

from calc import CALC_function

class DB_function:
    def __init__(self):
        super().__init__()
        self.calc = CALC_function()

    def db_connection_check(self, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
            cur = db_connect.cursor()
            sql = 'use ' + db
            cur.execute(sql)

            db_connect.close()
            return True
        except Exception as e:
            return False
            print("err db_connection_check : ", e)

    # region get data
    # 버전
    def get_version_num(self, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        version_list = []
        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
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
    def get_traffic_data(self, cycle=30, sync_time=None, lane=6, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
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
                share_data = self.calc.share_data(occu, data_start,cycle,lane, host, port, user, password, db, charset)

                #상하행
                lane_way = self.calc.lane_way(lane)

                #전송 데이터 종합
                if lane >= 1:
                    for i in range(lane):
                        traffic_temp = [ Tspeed_data[0][i], Tspeed_data[1][i], share_data[i], lane_way[i]]
                        traffic_data.append(traffic_temp)

        except Exception as e:
            print("err get_traffic_data : ", e)

        return traffic_data

    # 개별 차량 데이터
    def get_individual_traffic_data(self, cycle=30, sync_time=None, lane=6, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        individual_traffic_data = []

        try:
            if sync_time is None:
                print('nack')
            else:
                temp = time.localtime(sync_time - cycle)
                data_start = time.strftime("%Y-%m-%d %H:%M:%S", temp)

                #개별 차량 데이터
                individual_traffic_data = self.calc.Icar_data(data_start, lane, host, port, user, password, db, charset)

        except Exception as e:
            print("err get_individual_traffic_data : ", e)

        return individual_traffic_data

    # 차선별 누적 교통량 데이터
    def get_ntraffic_data(self, lane=6, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        ntraffic_data = []

        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset,
                                         autocommit=True)
            cur = db_connect.cursor()
            sql = "SELECT * FROM traffic_info order by Lane asc"
            cur.execute(sql)
            result = cur.fetchall()
            for i in range(lane):
                ntraffic_data.append(result[i][1])
            sql = "update traffic_info set nTraffic=0 set totalVelocity=0"  # 초기화 부분
            cur.execute(sql)
            db_connect.commit()
            db_connect.close()
        except Exception as e:
            print("err: ", e)

        return ntraffic_data

    # 카테고리(속도) 기준 차선별 교통량
    def get_speed_data(self, sync_time=None, lane=6, cnum=[],  host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        speed_data = []

        try:
            speed_data = self.calc.Cspeed_data(sync_time, cnum, lane, host, port, user, password, db, charset)
            print(speed_data)
        except Exception as e:
            print("err get_ntraffic_data : ", e)

        return speed_data

    # 함체 정보 데이터
    def get_controllerBox_state_data(self,  host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        controllerBox_state_list = []
        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
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

        # 돌발 상황 정보

    def get_outbreak(self, lane=6, host=None, port=None, user=None, password=None, db=None,
                     charset='utf8'):
        outbreak = []

        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset,
                                         autocommit=True)
            cur = db_connect.cursor()
            sql = "SELECT * FROM outbreak order by time desc"
            cur.execute(sql)
            result = cur.fetchall()

            # 상/하행
            if lane > 0:
                lane_half = lane / 2

                if result:
                    for i in range(lane):
                        for j in range(len(result)):
                            if result[j][1] == (i + 1):
                                out = []
                                out.append(result[j][0])
                                out.append(result[j][1])
                                out.append(result[j][2])
                                out.append(result[j][3])
                                out.append(result[j][4])
                                out.append(result[j][5])
                                if result[j][1] <= lane_half:
                                    out.append(0)
                                elif lane_half < result[j][1] <= lane:
                                    out.append(1)
                                else: # 값 오류
                                    continue
                                    # out.append(2)
                                outbreak.append(out)

                # 초기화 부분, 추후 활성화
                sql = "truncate outbreak"
                cur.execute(sql)
                db_connect.commit()
            db_connect.close()
        except Exception as e:
            print("err get_outbreak : ", e)
        return outbreak

    def get_parameter_data(self, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        lane_num = None
        collect_cycle = None
        category_num = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        use_ntraffic = None
        use_category_speed = None
        use_unexpected = None
        parameter_list = []

        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset,
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

    def get_occupancy_interval_data(self, lane=6, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        occupanvcy_interval_list = []
        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset, autocommit=True)
            cur = db_connect.cursor()

            temp_min = []
            temp_max = []
            # min 값 입력
            for i in range(lane):
                sql = "SELECT * FROM sw_parameter WHERE param LIKE '%occupancy_min' order by param asc;"
                cur.execute(sql)
                result = cur.fetchall()
                # result[1] => parameter value
                temp_min.append(int((result[i][1])))
            occupanvcy_interval_list.append(temp_min)

            # max 값 입력
            for i in range(lane):
                sql = "SELECT * FROM sw_parameter WHERE param LIKE '%occupancy_max' order by param asc;"
                cur.execute(sql)
                result = cur.fetchall()
                # result[1] => parameter value
                temp_max.append(int((result[i][1])))
            occupanvcy_interval_list.append(temp_max)

            db_connect.close()
        except Exception as e:
            print("err get_occupancy_interval_data : ", e)
        return occupanvcy_interval_list

    # endregion

    # region set data
    # S/W 파라미터 저장
    def set_paramete_data(self, parameter_list=[], host=None, port=None, user=None, password=None, db=None, charset='utf8'):
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
                db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset, autocommit=True)
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
                            sql = "UPDATE parameter set Data=" + str(list[i][j]) + " WHERE Param=" + str(index_list[index][0]) + " AND Nbyte=" + str(index_list[index][1]) + ";"
                            index += 1
                            cur.execute(sql)
                    else:
                        sql = "UPDATE parameter set Data=" + str(list[i]) + " WHERE Param=" + str(index_list[index][0]) + " AND Nbyte=" + str(index_list[index][1]) + ";"
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
                db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset, autocommit=True)
                cur = db_connect.cursor()
                sql = ''

                if len(msg_list) == 4:
                    sql = "INSERT INTO Log_communication value('" + msg_list[0] + "', '" + msg_list[1] + "', '" + msg_list[2] + "', '" + msg_list[3] + "');"
                elif len(msg_list) == 3:
                    sql = "INSERT INTO Log_communication value('" + msg_list[0] + "', '" + msg_list[1] + "', '" + msg_list[2] + "', '');"
                elif len(msg_list) == 2:
                    sql = "INSERT INTO Log_communication value('" + msg_list[0] + "', '" + msg_list[1] + "', '', '');"

                cur.execute(sql)
                db_connect.close()
        except Exception as e:
            print("err save_Log_data : ", e)
    # endregion

