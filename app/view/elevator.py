import pymysql as mysql
from flask import jsonify, Blueprint, request
import datetime
import time

elevator = Blueprint('elevator', __name__)

@elevator.route("/UseFrequency",methods=['POST'])
def get_UseFrequency():

    mysql_conn = mysql.connect(host='1.119.44.200', user='root', password='cuc@building', db='fakedata',charset='utf8',
                               cursorclass=mysql.cursors.DictCursor)  #设置数据库返回结果为字典类型
    mysql_cursor = mysql_conn.cursor()   #生成一个游标，开启游标功能，就是不会把数据全部返回，而是一条一条返回，便于处理

    # sql="select * from elevator where (TO_DAYS(entryTime)= TO_DAYS(NOW()) and entryTime between time('8:00:00') and time(now()) order by entryTime;"
    # sql="select count(id) as cnt from elevator where entryTime between '2020-11-30 22:21:34' and '2020-11-30 22:21:35'"
    # sql = "select * from elevator where TO_DAYS(entryTime) = TO_DAYS(NOW())"

    today = []
    # date = '2020-11-10'
    dateJson = request.get_json()['date']
    print("电梯"+dateJson)
    for i in range(0,24):
        sql="select count(id) as cnt from elevator where TO_DAYS(entryTime) = TO_DAYS('%s') and HOUR(entryTime) >= '%s' and HOUR(entryTime) <= '%s'"%(dateJson,i,i+1)
        # sql="select count(id) as cnt from elevator where TO_DAYS(entryTime) = TO_DAYS(NOW())"
        mysql_cursor.execute(sql)
        result = mysql_cursor.fetchall()
        #print(result)
        today.append(result[0]['cnt'])#注意result结果的格式
    # for i in range(0,6):
    #     sql="select count(id) as cnt from elevator where TO_DAYS(entryTime) = TO_DAYS(NOW()) and HOUR(entryTime) >= '%s' and HOUR(entryTime) <= '%s'"%(i,i+1)
    #     # sql="select count(id) as cnt from elevator where TO_DAYS(entryTime) = TO_DAYS(NOW())"
    #     mysql_cursor.execute(sql)
    #     result = mysql_cursor.fetchall()
    #     #print(result)
    #     today.append(result[0]['cnt']) #注意result结果的格式

    date_str1='2020-10-01 00:00:00'
    starttime = datetime.datetime.strptime(date_str1,'%Y-%m-%d %H:%M:%S')
    #date_str2 = time.strftime("%Y-%m-%d 00:00:00", time.localtime())  #获取当前日期
    date_str2 = dateJson+' 00:00:00'
    localtime = datetime.datetime.strptime(date_str2,'%Y-%m-%d %H:%M:%S')   #转换成struct tuple(datetime.datetime)格式
    # print(starttime)
    # print(localtime)
    days_num=(localtime-starttime).days
    print(days_num)

    avg = []
    for i in range(0,24):
        sql="select count(id) as cnt from elevator where HOUR(entryTime) >= '%s' and HOUR(entryTime) <= '%s'"%(i,i+1)
        # sql="select count(id) as cnt from elevator where TO_DAYS(entryTime) = TO_DAYS(NOW())"
        mysql_cursor.execute(sql)
        result = mysql_cursor.fetchall()
        #print(result)
        avg.append( int( result[0]['cnt'] / days_num ))

    Dict={'today':today,
          'avg':avg
    }

    # Dict = {'today':[1,5,6,5,6,4,4,6,9,9,2,8,6,3,4,5,1,8,6,3,1,5,6,7],
    #          'avg':[1,5,8,6,3,9,4,7,8,6,4,9,1,6,8,6,2,9,9,9,5,6,8,6]
    #        }
    #print(Dict)
    return jsonify(Dict)






