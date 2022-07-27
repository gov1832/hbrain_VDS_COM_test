import pymysql
from datetime import datetime
import time
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

    def get_traffic_data(self, cycle=30, sync_time=None, lane=2, host='183.99.41.239', port=23306, user='root', password='hbrain0372!', db='vds', charset='utf8'):
        traffic_data = []

        try:
            if sync_time == 0:
                print('nack')
            else:
                db_connect = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
                cur = db_connect.cursor()
                # temp = time.localtime(sync_time - cycle)
                # data_start = time.strftime("%Y-%m-%d %H:%M:%S", temp)
                data_start = '2022-07-25 20:17:00'
                traffic_temp = []
                sql = "SELECT distinct Zone FROM obj_info ORDER BY Zone asc;"
                cur.execute(sql)
                zone_list = []
                for i in cur:
                    zone_list.append(i[0])
                print(zone_list)

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

                temp_1[1] / num_1
                traffic_temp.append(temp_1)
                traffic_data.append(temp_2)

                # time_list.sort(reverse=True)
                # for i in range(len(time_list)):
                #     sql = "SELECT * FROM obj_info WHERE time='" + time_list[i][:23] + "';"
                #     cur.execute(sql)
                #     for data in cur:
                #         traffic_temp.append(data)
                print(traffic_temp)


                db_connect.close()
        except Exception as e:
            print("err: ", e)

        return traffic_data
