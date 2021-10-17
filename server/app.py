from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(app.root_path,'taskmgr.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


# 创建表 -- 项目表
class Projects(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    # description = db.Column(db.String(100))

# 任务表
class Tasks(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60))
    date = db.Column(db.DateTime)
    condition = db.Column(db.String(10))
    pid = db.Column(db.Integer)

projects=[
    {'name':'项目1'},
    {'name':'项目2'},
    {'name':'项目3'},
],
tasks=[
    {'title':'逛公园','date':'10月13日','condition':'todo','pid':1},
    {'title':'完成游戏','date':'10月12日','condition':'todo','pid':1},
    {'title':'吃饭','date':'10月15日','condition':'done','pid':1},
    {'title':'上王者','date':'10月16日','condition':'done','pid':1},
    {'title': '撸猫', 'date': '10月13日', 'condition': 'todo', 'pid': 2},
    {'title': '看电视剧', 'date': '10月12日', 'condition': 'todo', 'pid': 2},
    {'title': '逛街', 'date': '10月15日', 'condition': 'done', 'pid': 2},
    {'title': '去XX景区', 'date': '10月16日', 'condition': 'done', 'pid': 3},
]

@app.route('/')
def hello():
    return tasks 

