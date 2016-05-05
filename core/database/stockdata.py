from config import database as dbconfig
import pymysql.cursors


class StockData:

    def __init__(self):
        self.con = pymysql.connect(
            host=dbconfig.host,
            user=dbconfig.username,
            password=dbconfig.password,
            db=dbconfig.database
        )
        self.fromDate = ""
        self.toDate = ""
        self.symbol = None
        self.selectFields = ""

    def sfrom(self, fdate):
        self.fromDate = fdate

    def sto(self, tdate):
        self.toDate = tdate

    def ssymbol(self, symbol):
        self.symbol = symbol

    def get_sdata(self, symbol):
        with self.con.cursor() as cursor:
            sql = '''
                    SELECT s.sopen, s.high, s.low, s.sclose, s.quantity, TRUNCATE(s.turnover*100000/s.quantity, 2) AS average
                    FROM stockData s, companies c
                    WHERE c.symbol = %s
                    AND c.id = s.companyId
                    AND DATE(sdate) BETWEEN %s AND %s
                    ORDER BY sdate ASC
                    '''
            cursor.execute(sql, (symbol, self.fromDate, self.toDate))
            results = cursor.fetchall()
            return results

    def getallofcompany(self, symbol=None):
        with self.con.cursor() as cursor:
            sql = '''
                    SELECT s.sopen, s.high, s.low, s.sclose, s.quantity, TRUNCATE(s.turnover*100000/s.quantity, 2) AS average
                    FROM stockData s, companies c
                    WHERE c.symbol = %s
                    AND c.id = s.companyId
                    ORDER BY sdate ASC
                    '''
            cursor.execute(sql, (symbol, self.fromDate, self.toDate))
            results = cursor.fetchall()
            return results

    def get_all_companies(self):
        with self.con.cursor() as cursor:
            sql = '''
                    SELECT *
                    FROM  companies c
                    ORDER BY id ASC
                    '''
            cursor.execute(sql)
            results = cursor.fetchall()
            return results

    def get_last_n(self, symbol, n):
        with self.con.cursor() as cursor:
            sql = '''
                    SELECT *
                    FROM stockData s, companies c
                    WHERE c.symbol = %s
                    AND c.id = s.companyId
                    ORDER BY sdate DESC
                    LIMIT %s
                    '''
            cursor.execute(sql, (symbol, n))
            results = cursor.fetchall()
            return results
