import pymysql

class MyDB:

    def __init__(self, host='localhost', username='root', password='210421', database='PTA'):
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.cur = None
        self.con = None
        # connect to mysql
        try:
            self.con = pymysql.connect(host=self.host, user=self.username, password=self.password,
                                       database=self.database, charset='utf8mb4')
            self.cur = self.con.cursor()
        except:
            print("DataBase connect error,please check the db config.")

    def close(self):
        self.con.close()

    def create_table(self, sql_str):
        try:
            self.cur.execute(sql_str)
        except Exception as e:
            print(e)

    def savedata(self, item, table):
        fields = ','.join(item.keys())
        values = ','.join(['%s'] * len(item))
        sql = f'INSERT INTO {table}({fields}) VALUES ({values})'
        try:
            self.cur.execute(sql, tuple(item.values()))
            self.con.commit()
        except:
            print('Failed')
            self.con.rollback()

