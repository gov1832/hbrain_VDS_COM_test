import pymysql

class DB_function:
    def __init__(self):
        super().__init__()

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