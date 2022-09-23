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

        self.distlong_diff = 30

    # DB 연결 체크 함수
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
                # print
                print("lane: ", lane)
                print("sync_time: ", sync_time)
                print("cycle: ", cycle)

                db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
                cur = db_connect.cursor()
                temp = time.localtime(sync_time - cycle)
                data_start = time.strftime("%Y-%m-%d %H:%M:%S", temp)
                # data_start = '2022-08-29 20:05:41.350'

                sql = "SELECT * FROM obj_info WHERE time >='" + data_start + "' ORDER BY ID asc, time asc;"
                cur.execute(sql)
                result = cur.fetchall()
                #print(result)
                temp = []
                num = []
                for i in range(lane):
                    temp.append([1, 0])
                    num.append(0)
                for i in range(0, len(result)-1):
                    for j in range(lane):
                        if result[i][14] % lane == j:
                            num[j] += 1
                            if result[i][1] != result[i + 1][1]:
                                temp[j][0] += 1
                                temp[j][1] += result[i][6]
                            elif abs(result[i + 1][3] - result[i][3]) < self.distlong_diff:
                                temp[j][1] += result[i][6]
                            else:
                                temp[j][0] += 1
                                temp[j][1] += result[i][6]

                # 점유율
                sql = "SELECT * FROM obj_info WHERE time >='" + data_start + "' and (DistLong BETWEEN '30' AND '33') ORDER BY ID asc, time desc;"

                cur.execute(sql)
                result = cur.fetchall()
                ttime = [0]
                timegap = []
                timeoc = []
                coun = []
                for i in range(lane):
                    timegap.append(0)
                    timeoc.append(0)
                    coun.append(0)

                for i in range(0, len(result)-1):
                    if result[i][1] != result[i + 1][1] or abs(result[i][3] - result[i + 1][3]) > 2:
                        ttime.append(i)
                        ttime.append((i+1))
                ttime.append((len(result)-1))

                for i in range(0, len(ttime), 2):
                    for j in range(lane):
                        if result[ttime[i]][14] % lane == j:
                            timegap[j] += ((result[ttime[i]][0] - result[ttime[i+1]][0]).microseconds/1000000) /cycle
                            coun[j] += 1
                            #print(timegap[j])

                for j in range(lane):
                    if coun[j] != 0:
                        timeoc[j] = timegap[j] * 100 /coun[j]
                        #print(timeoc[j])
                    else:
                        timeoc[j] = 0

                if lane > 0 and lane != 1:
                    lane_half = lane / 2
                    for j in range(1, lane):
                        # 상/하행
                        if j <= lane_half:
                            laneway = 0
                        else:
                            laneway = 1
                        if num[j] != 0:
                            traffic_temp = [temp[j][0], round(temp[j][1] / num[j]), round(timeoc[j]), laneway]
                            traffic_data.append(traffic_temp)
                        else:
                            traffic_temp = [temp[j][0], 0, round(timeoc[j]), laneway]
                            traffic_data.append(traffic_temp)

                if num[0] != 0:
                    laneway = 1
                    traffic_temp = [temp[0][0], round(temp[0][1] / num[0]), round(timeoc[0]), laneway]
                    traffic_data.append(traffic_temp)
                else:
                    laneway = 1
                    traffic_temp = [temp[0][0], 0, round(timeoc[0]), laneway]
                    traffic_data.append(traffic_temp)

                #print(traffic_data)
                db_connect.close()
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
                # print
                print("lane: ", lane)
                print("sync_time: ", sync_time)
                print("cycle: ", cycle)

                db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
                cur = db_connect.cursor()
                temp = time.localtime(sync_time - cycle)
                data_start = time.strftime("%Y-%m-%d %H:%M:%S", temp)
                data_count = datetime.datetime.strptime(data_start, '%Y-%m-%d %H:%M:%S')
                sql = "SELECT * FROM obj_info where time >= '" + data_start + "' order by ID asc, time asc"
                cur.execute(sql)

                result = cur.fetchall()

                count = [0]
                limit_len = 40
                for i in range(1, len(result)):
                    # print(result[i])
                    if (abs(result[i][3]-result[i-1][3]) >= self.distlong_diff) or (abs(result[i][1]-result[i-1][1]) > 0):
                        count.append(i)
                count.append(len(result))
                #print(len(result))

                for i in range(1, len(count)):
                    cardata = []
                    carspeed = 0
                    carway = 0
                    carlane = 0
                    carcont = 0
                    carid = 0
                    for j in range(count[i - 1], count[i]):
                        carcont += 1
                        carspeed += result[j][6]
                        carway += result[j][5]
                        carid += result[j][11]
                        if (result[j][14] % lane) == 0:
                            carlane += lane
                        else:
                            carlane += (result[j][14] % lane)
                    if carcont != 0:
                        cardata.append(round(carlane / carcont))
                        cardata.append((result[count[i - 1]][0] - data_count).seconds)
                        cardata.append(int(carspeed / carcont))
                        if (int(carway)/carcont) >= 0:
                            cardata.append(0)
                        else:
                            cardata.append(1)
                        cardata.append(round(carid / carcont))
                        individual_traffic_data.append(cardata)

                db_connect.close()
        except Exception as e:
            print("err get_individual_traffic_data : ", e)

        return individual_traffic_data

    # 차선별 누적 교통량 데이터
    def get_ntraffic_data(self, lane=6, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        ntraffic_data = []

        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset, autocommit=True)
            cur = db_connect.cursor()

            # 차선 오름차순으로 데이터 select
            sql = "SELECT * FROM cumulative_traffic order by Lane asc"
            cur.execute(sql)
            result = cur.fetchall()
            for i in range(lane):
                ntraffic_data.append(result[i][1])

            # 초기화 부분
            sql = "update cumulative_traffic set nTraffic=0"
            cur.execute(sql)

            db_connect.close()
        except Exception as e:
            print("err: ", e)

        return ntraffic_data

    # 카테고리(속도) 기준 차선별 교통량
    def get_speed_data(self, lane=6, cnum=[],  host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        speed_data = []

        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset, autocommit=True)
            cur = db_connect.cursor()

            for i in range(lane):
                sql = "SELECT * FROM cumulative_velocity where Zone=" +str(i+1)+ " order by ID asc"

                cur.execute(sql)
                result = cur.fetchall()

                lane_speed = [0,0,0,0,0,0,0,0,0,0,0,0]
                for res in result:
                    for i in reversed(range(len(cnum))):
                        if res[2] >= cnum[i]:
                            lane_speed[i] += 1
                            break

                speed_data.append(lane_speed)

            sql = "truncate cumulative_velocity" #초기화 부분, 추후 활성화
            cur.execute(sql)
            db_connect.close()
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

