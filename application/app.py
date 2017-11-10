import json
import os
import pymysql.cursors
import requests
from flask import Flask


PORT = 8080
BASE_CONSUL_URL = 'http://consul:8500'
DB_SERVICE_NAME = os.environ.get('DB_SERVICE_NAME','mysql')
TABLE_NAME = 'tbl_msg'

def get_config():
        url = BASE_CONSUL_URL + '/v1/catalog/service/' + DB_SERVICE_NAME 
        response = requests.get(url)
        result = json.loads(response.content.decode('utf-8'))
        r = result[0] 
        return r

data = get_config()

if data is not None:
        DB_HOST = str(data["ServiceAddress"])
        DB_PORT = int(data["ServicePort"])
        MYSQL_USER = os.environ.get('MYSQL_USER',"root")
        MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE',"mysqldb")
        MYSQL_ROOT_PASSWORD = os.environ.get('MYSQL_ROOT_PASSWORD',"root")


# database connection create 
connection = pymysql.connect(host=DB_HOST,
                             user=MYSQL_USER,
                             password=MYSQL_ROOT_PASSWORD,
                             port=DB_PORT,
                             db=MYSQL_DATABASE,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)



def tbl_create():
        cursor = connection.cursor()
        create_tbl = '''CREATE TABLE IF NOT EXISTS `{}` (
                        `id` int(11) NOT NULL AUTO_INCREMENT,
                        `msg` varchar(255) COLLATE utf8_bin NOT NULL,
                        PRIMARY KEY (`id`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
                        AUTO_INCREMENT=1;'''.format(TABLE_NAME)
        cursor.execute(create_tbl)
        cursor.close()

def insert_data():
        cursor = connection.cursor()
        sql =  "INSERT INTO `{}` (`msg`) VALUES (%s)".format(TABLE_NAME)
        cursor.execute(sql, ('Hello, world'))
        connection.commit()
        cursor.close()

def get_msg():
        with connection.cursor() as cursor:
                sql = "SELECT `msg` FROM `{}` WHERE `id`=%s".format(TABLE_NAME)
                cursor.execute(sql, ('1'))
                result = cursor.fetchone()
                result = str(result['msg'])
                cursor.close()
        return result


def checkTableExists(dbconnection):
        cursor = dbconnection.cursor()
        stmt = "SHOW TABLES LIKE '{}'".format(TABLE_NAME)
        cursor.execute(stmt)
        exist = cursor.fetchone()
        cursor.close()
        if exist:             
                return True
        else:
                return False

# check if table exists
if not checkTableExists(connection):
        tbl_create()
        insert_data()

app = Flask(__name__)
@app.route('/')
def home():
	res = get_msg()
	return res


app.run(host="0.0.0.0", port=PORT)

