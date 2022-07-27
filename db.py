import pymysql
from datetime import datetime, timedelta
import time
import math

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

    def get_traffic_data(self, cycle=30, host='183.99.41.239', port=23306, user='root', password='hbrain0372!', db='vds', charset='utf8'):
        traffic_data = []
        """
        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
            cur = db_connect.cursor()
            now_time = time.time()
            temp = now_time - cycle
            # data_start =
            time_list = []
            sql = 'SELECT time FROM obj_info'
            cur.execute(sql)

            for i in cur:
                if i[0] > data_start:
                    time_list.append(i[0])

            # time_list.sort(reverse=True)
            #
            for i in range(len(time_list)):
                sql = "SELECT * FROM vds_version WHERE time='" + time_list[i] + "';"
                cur.execute(sql)
                for data in cur:
                    traffic_temp.append()
            # cur.execute(sql)
            # for i in cur:
            #     version_list.append(i)

            db_connect.close()
        except Exception as e:
            print("err: ", e)
"""
        return traffic_data

    def get_individual_traffic_data(self, cycle=30, sync_time=None, lane=2, host='183.99.41.239', port=23306, user='root', password='hbrain0372!',
                       db='vds', charset='utf8'):
        individual_traffic_data = []

        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
            cur = db_connect.cursor()
            sync_time = time.time()
            temp = time.localtime(sync_time - cycle)
            #data_start = time.strftime("%Y-%m-%d %H:%M:%S", temp)
            realtime = "2022-07-25 20:17:27"
            data_start = "2022-07-25 20:16:57"
            data_count = datetime.strptime(data_start, '%Y-%m-%d %H:%M:%S')
            sql = "SELECT * FROM obj_info where time >= '" + data_start + "' order by ID asc, time asc"
            print(sql)
            cur.execute(sql)

            result = cur.fetchall()

            count = [0]
            limit_len = 40
            for i in range(1, len(result)):
                # print(result[i])
                if (abs(result[i][3]-result[i-1][3]) >= self.distlong_diff) or (abs(result[i][1]-result[i-1][1]) > 0):
                    count.append(i)
            count.append(len(result))
            print(count)
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
                print(cardata)

            db_connect.close()
        except Exception as e:
            print("err: ", e)

        print(individual_traffic_data)
        return individual_traffic_data



'''
    def get_speed_data(self, back=30,lane=2,host='183.99.41.239', port=23306, user='root', password='hbrain0372!', db='vds', charset='utf8'):
        speed_data = []

        try:
            db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
            cur = db_connect.cursor()
            #now_time = time.time()
            #temp = now_time - back
            #print(temp)

            timenow = datetime(2022, 7, 25, 20, 17, 27)  # 추후 datetime.now() 로 변경
            if back == 30:
                timepast = timenow + timedelta(seconds=-30)  # 추후 -30으로 값 변경 필요
            else:
                timepast = back  # 현재시간 -30초 임 back 값이 있으면 back 값을 시간으로 변경

            # if (back == timenow):
            # timepast = timenow + timedelta(seconds=-5) #현재 시간 기준 적용시 사용할 것
            # else:
            # timepast = back


            sql = "SELECT * FROM obj_info where time >= '" +str(timepast)+ "' order by ID asc, time asc"
            print(sql)

            cur.execute(sql)

            result = cur.fetchall()
            #result = cur.fetchmany(size = 200)
            #print(result[0][0])
            #for record in result:
            #    print(record)

            count = []
            limit_len = 40
            for i in range(1, len(result)):
                # print(result[i])
                if (result[i][3] <= limit_len) and (result[i-1][3] > limit_len):
                    count.append(i)

            print(count)


            for con in count:
                for i in range(lane):
                    if ((result[con][12]%lane) == i):
                           print(i)



            """
            for i in range(1, len(count)):
                sum = 0
                for j in range(count[i-1],count[i]):
                    sum += result[j][4]
                ans = sum/(count[i]-count[i-1])
                print(ans)

            
            data_start =
            time_list = []
            sql = 'SELECT time FROM obj_info'
            cur.execute(sql)

            for i in cur:
                if i[0] > data_start:
                    time_list.append(i[0])

            # time_list.sort(reverse=True)
            #
            for i in range(len(time_list)):
                sql = "SELECT * FROM vds_version WHERE time='" + time_list[i] + "';"
                cur.execute(sql)

            """

            db_connect.close()
        except Exception as e:
            print("err: ", e)

        return speed_data '''