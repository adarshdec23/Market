import pymysql.cursors
from config import db

connection = pymysql.connect(
    host=db.host,
    user=db.username,
    password=db.password,
    db=db.database
)
try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM stockData"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
finally:
    connection.close()