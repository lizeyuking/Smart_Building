import pymysql
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import json_util
from bson.json_util import dumps
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.view.elevator import elevator
from app.view.space import space
from app.view.meetingRoom import meetingRoom
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  #显示正常字符串而不是ASCII码值

app.register_blueprint(elevator, url_prefix='/smartBuilding/elevator')
app.register_blueprint(space, url_prefix='/smartBuilding/space')
app.register_blueprint(meetingRoom, url_prefix='/smartBuilding/meetingRoom')

pymysql.install_as_MySQLdb()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:cuc@building@1.119.44.200:3306/fakedata'
# 配置flask配置对象中键：SQLALCHEMY_COMMIT_TEARDOWN,设置为True,应用会自动在每次请求结束后提交数据库中变动
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False

db = SQLAlchemy(app)
# enable CORS
# CORS(app, resources={r'/*': {'origins': '*'}})  # 允许跨域
CORS(app, supports_credentials=True)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')  #host='0.0.0.0' 广播
