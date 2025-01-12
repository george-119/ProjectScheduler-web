import pymysql
class connection:
    def __init__(self):
        self.con = pymysql.connect(host='localhost', user='root', password='', db='complete_my_project', port=3306)
        self.cu = self.con.cursor()
    def insert(self,q):
        self.cu.execute(q)
        self.con.commit()
        return self.cu.lastrowid

    def select(self, q):
        self.cu.execute(q)
        return self.cu.fetchall()

    def selectOne(self, q):
        self.cu.execute(q)
        return self.cu.fetchone()

    def update(self, q):
        self.cu.execute(q)
        self.con.commit()
        return self.cu.rowcount

    def delete(self, q):
        self.cu.execute(q)
        self.con.commit()
        return self.cu.rowcount
