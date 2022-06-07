import pymysql as mysql
from flask import jsonify, Blueprint, request
import math
import datetime
import time

meetingRoom = Blueprint('meetingRoom', __name__)

room_num = 42 #会议室总个数

#房间利用率路由
@meetingRoom.route("/room",methods=['POST'])
def get_UseFrequency_room():
    mysql_conn = mysql.connect(host='1.119.44.200', user='root', password='cuc@building', db='fakedata', charset='utf8',
                               cursorclass=mysql.cursors.DictCursor)  # 设置数据库返回结果为字典类型
    mysql_cursor = mysql_conn.cursor()  # 生成一个游标，开启游标功能，就是不会把数据全部返回，而是一条一条返回，便于处理

    room_useNow = []
    room_UseFrequency = []

    # date = '2020-11-10'
    dateJson = request.get_json()['date']
    for i in range(0,24):
        sql="select count(location) as cnt from confer_room_reserv where TO_DAYS(start_time) = TO_DAYS('%s') and ( (HOUR(start_time) >= '%s' and HOUR(start_time) <= '%s') or (HOUR(end_time) >= '%s' and HOUR(end_time) <= '%s') )"%(dateJson,i,i+1,i,i+1)
        mysql_cursor.execute(sql)
        result = mysql_cursor.fetchall()
        #print(result)
        temp=result[0]['cnt']
        room_useNow.append(temp)
        room_UseFrequency.append(round(temp/room_num,2)*100)

    Dict = {'bar': room_useNow,
            'line': room_UseFrequency
            }
    # print(Dict)
    return jsonify(Dict)

#时间利用率路由
@meetingRoom.route("/time",methods=['POST'])
def get_UseFrequency_time():
    mysql_conn = mysql.connect(host='1.119.44.200', user='root', password='cuc@building', db='fakedata', charset='utf8',
                               cursorclass=mysql.cursors.DictCursor)  # 设置数据库返回结果为字典类型
    mysql_cursor = mysql_conn.cursor()

    dateJson = request.get_json()['date']
    print(dateJson)

    #floor_num=[0,0,3,3,3,3,3,3,3,3,3,3,3,3,3]   #每层有多少会议室
    #floor_str=["一","二","三","四","五","六","七","八","九","十","十一","十二","十三","十四","十五","十六"] #对应汉字
    sql = "select sum(TIMESTAMPDIFF(HOUR,start_time,end_time)) as cnt from confer_room_reserv where TO_DAYS(start_time) = TO_DAYS('%s') " % (
        dateJson)

    #sql = "select * from confer_room_reserv where location like'%十六层%'AND location not like '%十%'"

    mysql_cursor.execute(sql)
    result = mysql_cursor.fetchall()
    # print(result)
    temp = float(round(result[0]['cnt']/room_num,2))
    res1=temp
    res2=round(temp-0.1,2)
    Dict = {'rate': [res1, res2]
            }
    return jsonify(Dict)

#使用状态路由
@meetingRoom.route("/useStatus", methods=['POST'])
def get_UseFrequency_useStatus():
    mysql_conn = mysql.connect(host='1.119.44.200', user='root', password='cuc@building', db='fakedata', charset='utf8',
                               cursorclass=mysql.cursors.DictCursor)  # 设置数据库返回结果为字典类型
    mysql_cursor = mysql_conn.cursor()
    dateJson = request.get_json()['date']
    print(dateJson)
    sql = "select * from confer_room_reserv where TO_DAYS(start_time) = TO_DAYS('%s') and end_time>NOW()" % (
    dateJson)
    mysql_cursor.execute(sql)
    result = mysql_cursor.fetchall()
    print(result)

    Dict = []
    for i in range(0,len(result)):
        if result[0]['start_time']>datetime.datetime.now():
            status_str='空闲'
        else:
            status_str='使用中'
        each_str={'status_date':dateJson,'status_name':result[0]['location'],'status_theme':result[0]['theme'],'status_status':status_str,'status_start':result[0]['start_time'],'status_end':result[0]['end_time']}
        Dict.append(each_str)
    # Dict=[{status_date: '2020-11-06', status_name: '十五层C会议室', status_theme: '国家传播创新研究', status_status: '空闲', status_start: '2020-11-09 00:38:57', status_end: '2020-11-09 02:38:57'},
    #       {status_date: '2020-11-06', status_name: '十五层C会议室', status_theme: '国家传播创新研究', status_status: '空闲', status_start: '2020-11-09 00:38:57', status_end: '2020-11-09 02:38:57'}
    # ]
    return jsonify(Dict)