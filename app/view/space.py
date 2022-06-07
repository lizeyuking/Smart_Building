import pymysql as mysql
from flask import jsonify, Blueprint, request
import datetime
import time

space = Blueprint('space', __name__)

@space.route("/FloorUsage",methods=['POST'])
def get_UseFrequency():
    mysql_conn = mysql.connect(host='1.119.44.200', user='root', password='cuc@building', db='fakedata', charset='utf8',
                               cursorclass=mysql.cursors.DictCursor)  # 设置数据库返回结果为字典类型
    mysql_cursor = mysql_conn.cursor()  # 生成一个游标，开启游标功能，就是不会把数据全部返回，而是一条一条返回，便于处理

    total_size = [800,800,800,800,800,800,800,800,800,800,800,800,800,800,800,800]
    #floor_num = [40,50,96,58,38,53,34,26,35,36,31,30,29,26,25,19]  #每层大概人数
    avg = []
    # date = '2020-11-10'
    dateJson = request.get_json()['date']
    for i in range(0,16):
        max_num=0
        print("floor:", i)
        for j in range(0,24):
            sql = "select count(id) as cnt from facerecords where Floor_id='%s' and TO_DAYS(entryTime) = TO_DAYS('%s') and ( (HOUR(entryTime) >= '%s' and HOUR(entryTime) <= '%s') or (HOUR(leaveTime) >= '%s' and HOUR(leaveTime) <= '%s') )" % (
            i+1,dateJson, j,j+1,j,j+1)
            mysql_cursor.execute(sql)
            result = mysql_cursor.fetchall()
            max_num=max(max_num,result[0]['cnt'])
            print("result:",result)
            print("max_num:", max_num)
        avg.append(int(total_size[i]/max_num))

    Dict = {'today':total_size,
             'avg':avg
           }
    #print(Dict)
    return jsonify(Dict)




