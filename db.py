import pymysql
from datetime import datetime, timedelta
import time
import math
import datetime

class DB_function:
    def __init__(self):
        super().__init__()
        self.distlong_diff = 20

    def test(self):
        print(":sdfaasfd")

    def get_version_num(self, host='183.99.41.239', port=23306, user='root', password='hbrain0372!', db='vds', charset='utf8'):
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

            sql = "SELECT * FROM vds_version WHERE time='" + result[0] + "';"
            cur.execute(sql)
            for i in cur:
                version_list.append(i)

            db_connect.close()
        except Exception as e:
            print("err: ", e)

        return version_list

    # 교통량 데이터
    def get_traffic_data(self, cycle=30, sync_time=None, lane=2, host='183.99.41.239', port=23306, user='root', password='hbrain0372!', db='vds', charset='utf8'):
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

                traffic_temp = [temp_1[0], round(temp_1[1] / num_1)]
                traffic_data.append(traffic_temp)
                traffic_temp = [temp_2[0], round(temp_2[1] / num_2)]
                traffic_data.append(traffic_temp)

                db_connect.close()
        except Exception as e:
            print("err: ", e)

        return traffic_data

    # 개별 차량 데이터
    def get_individual_traffic_data(self, cycle=30, sync_time=None, lane=2, host='183.99.41.239', port=23306, user='root', password='hbrain0372!', db='vds', charset='utf8'):
        individual_traffic_data = []

        try:
            if sync_time is None:
                print('nack')
            else:
                db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
                cur = db_connect.cursor()
                temp = time.localtime(sync_time - cycle)
                data_start = time.strftime("%Y-%m-%d %H:%M:%S", temp)
                data_count = datetime.strptime(data_start, '%Y-%m-%d %H:%M:%S')
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

                for i in range(1,len(count)):
                    cardata = []
                    carspeed = 0
                    carlane = 0
                    carcont = 0
                    for j in range(count[i-1], count[i]):
                        carcont += 1
                        carspeed += result[j][4]
                        if (result[j][12]%lane) == 0:
                            carlane += lane
                        else:
                            carlane += (result[j][12]%lane)

                    cardata.append(round(carlane/carcont))
                    cardata.append((result[count[i-1]][0]-data_count).seconds)
                    cardata.append(carspeed/carcont)
                    individual_traffic_data.append(cardata)

                db_connect.close()
        except Exception as e:
            print("err: ", e)

        return individual_traffic_data

    def get_ntraffic_data(self, lane=2, host='183.99.41.239', port=23306, user='root', password='hbrain0372!', db='vds', charset='utf8'):
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

    def get_speed_data(self, lane=2, cnum=[],  host='183.99.41.239', port=23306, user='root', password='hbrain0372!', db='vds', charset='utf8'):
        speed_data = []

        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset, autocommit=True)
            cur = db_connect.cursor()

            for i in range(lane):
                sql = "SELECT * FROM cumulative_velocity where Lane=" +str(i+1)+ " order by ID asc"

                cur.execute(sql)
                result = cur.fetchall()
                if result != '':
                    lane_speed = [0,0,0,0,0,0,0,0,0,0,0,0]
                    for res in result:
                        for i in reversed(range(len(cnum))):
                            if res[2] >= cnum[i]:
                                lane_speed[i] += 1
                                break

                speed_data.append(lane_speed)

            #sql = "truncate cumulative_velocity" #초기화 부분, 추후 활성화
            #cur.execute(sql)
            db_connect.close()
        except Exception as e:
            print("err: ", e)

        return speed_data

    # S/W 파라미터 저장
    def set_paramete_data(self, parameter_list=[], host='183.99.41.239', port=23306, user='root', password='hbrain0372!', db='vds', charset='utf8'):
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
                print("index: ", index_list)
                index = 0
                for i in range(len(list)):
                    if type(list[i]) == type([]):
                        for j in range(len(list[i])):
                            sql = "UPDATE parameter set Data=" + str(list[i][j]) + " WHERE Param=" + str(index_list[index][0]) + " AND Nbyte=" + str(index_list[index][1]) + ";"
                            index += 1
                            print(sql)
                            cur.execute(sql)
                    else:
                        sql = "UPDATE parameter set Data=" + str(list[i]) + " WHERE Param=" + str(index_list[index][0]) + " AND Nbyte=" + str(index_list[index][1]) + ";"
                        index += 1
                        print(sql)
                        cur.execute(sql)

                db_connect.close()
        except Exception as e:
            print("err: ", e)


    def get_image_link(self, request_time=None, direction=None, host='183.99.41.239', port=23306, user='root', password='hbrain0372!', db='vds', charset='utf8'):
        image_link = []

        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset, autocommit=True)
            cur = db_connect.cursor()
            request_time = datetime.datetime.now() #추후 삭제 요망
            direction = 0 #추후 삭제 요망
            request_time = request_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            sql_1 = "insert into image value('" +str(request_time)+ "', " +str(direction)+ ", '')"
            cur.execute(sql_1)
            sql_2 = "SELECT * FROM image order by time desc"

            while True:
                cur.execute(sql_2)
                result = cur.fetchall()
                if result[0][0].strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] == request_time:
                    if result[0][2] != '':
                       image_link.append(str(result[0][1]))
                       image_link.append(result[0][2])
                       break

            db_connect.close()
        except Exception as e:
            print("err: ", e)

        print(image_link)
        return image_link

