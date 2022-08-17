import pymysql
from datetime import datetime, timedelta
import time
import math
import datetime

class DB_function:
    def __init__(self):
        super().__init__()
        self.distlong_diff = 20

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
            print("err: ", e)

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
            print("err: ", e)

        return version_list

    # 교통량 데이터
    def get_traffic_data(self, cycle=30, sync_time=None, lane=2, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        traffic_data = []

        try:
            if sync_time is None:
                print('nack')
            else:
                db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
                cur = db_connect.cursor()
                temp = time.localtime(sync_time - cycle)
                data_start = time.strftime("%Y-%m-%d %H:%M:%S", temp)
                # data_start = '2022-07-25 20:17:00'

                sql = "SELECT * FROM obj_info WHERE time >='" + data_start + "' ORDER BY ID asc, time asc;"
                cur.execute(sql)
                result = cur.fetchall()
                # print(result)
                temp_1 = [0, 0]
                temp_2 = [0, 0]
                num_1 = 0
                num_2 = 0
                for i in range(0, len(result)-1):
                    if result[i][12] % lane == 1:
                        num_1 += 1
                        if result[i][1] != result[i+1][1]:
                            temp_1[0] += 1
                            temp_1[1] += result[i][4]
                        elif abs(result[i+1][3] - result[i][3]) < self.distlong_diff:
                            temp_1[1] += result[i][4]
                        else:
                            temp_1[0] += 1
                            temp_1[1] += result[i][4]
                    elif result[i][12] % lane == 0:
                        num_2 += 1
                        if result[i][1] != result[i + 1][1]:
                            temp_2[0] += 1
                            temp_2[1] += result[i][4]
                        elif abs(result[i + 1][3] - result[i][3]) < self.distlong_diff:
                            temp_2[1] += result[i][4]
                        else:
                            temp_2[0] += 1
                            temp_2[1] += result[i][4]
                    if (i+1) == (len(result)-1):
                        if result[i+1][12] % lane == 1:
                            num_1 += 1
                        if result[i+1][12] % lane == 0:
                            num_2 += 1
                if num_1 != 0:
                    traffic_temp = [temp_1[0], round(temp_1[1] / num_1)]
                    traffic_data.append(traffic_temp)
                if num_2 != 0:
                    traffic_temp = [temp_2[0], round(temp_2[1] / num_2)]
                    traffic_data.append(traffic_temp)

                db_connect.close()
        except Exception as e:
            print("err: ", e)

        return traffic_data

    # 개별 차량 데이터
    def get_individual_traffic_data(self, cycle=30, sync_time=None, lane=2, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        individual_traffic_data = []

        try:
            if sync_time is None:
                print('nack')
            else:
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
                    carlane = 0
                    carcont = 0
                    carid = 0
                    for j in range(count[i - 1], count[i]):
                        carcont += 1
                        carspeed += result[j][4]
                        carid += result[j][9]
                        if (result[j][12] % lane) == 0:
                            carlane += lane
                        else:
                            carlane += (result[j][12] % lane)
                    if carcont != 0:
                        cardata.append(round(carlane / carcont))
                        cardata.append((result[count[i - 1]][0] - data_count).seconds)
                        cardata.append(int(carspeed / carcont))
                        cardata.append(round(carid / carcont))
                        individual_traffic_data.append(cardata)

                db_connect.close()
        except Exception as e:
            print("err: ", e)

        return individual_traffic_data

    # 차선별 누적 교통량 데이터
    def get_ntraffic_data(self, lane=2, host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        ntraffic_data = []

        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset, autocommit=True)
            cur = db_connect.cursor()
            sql = "SELECT * FROM cumulative_traffic order by Lane asc"
            cur.execute(sql)
            result = cur.fetchall()
            for i in range(lane):
                ntraffic_data.append(result[i][1])
            sql = "update cumulative_traffic set nTraffic=0" #초기화 부분
            cur.execute(sql)

            db_connect.close()
        except Exception as e:
            print("err: ", e)

        return ntraffic_data

    # 카테고리(속도) 기준 차선별 교통량
    def get_speed_data(self, lane=2, cnum=[],  host=None, port=None, user=None, password=None, db=None, charset='utf8'):
        speed_data = []

        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset, autocommit=True)
            cur = db_connect.cursor()

            for i in range(lane):
                sql = "SELECT * FROM cumulative_velocity where Lane=" +str(i+1)+ " order by ID asc"

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
            print("err: ", e)

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
            print("err: ", e)

        return controllerBox_state_list

        # 돌발 상황 정보

    def get_outbreak(self, lane=2, host=None, port=None, user=None, password=None, db=None,
                     charset='utf8'):
        outbreak = []

        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset,
                                         autocommit=True)
            cur = db_connect.cursor()
            sql = "SELECT * FROM outbreak order by time desc"
            cur.execute(sql)
            result = cur.fetchall()

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
                            outbreak.append(out)

                sql = "truncate outbreak" #초기화 부분, 추후 활성화
                cur.execute(sql)
            db_connect.close()
        except Exception as e:
            print("err: ", e)
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
            print("err: ", e)
        return parameter_list

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
            print("err: ", e)


    # endregion

