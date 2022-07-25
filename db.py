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


        except Exception as e:
            print("err: ", e)

        return version_list