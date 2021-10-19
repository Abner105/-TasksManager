import datetime

from flask import Flask,make_response
from flask_sqlalchemy import SQLAlchemy
import os,json,click
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
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
    title = db.Column(db.String(80))
    date = db.Column(db.DateTime)
    condition = db.Column(db.String(10)) # 任务的状态
    pid = db.Column(db.Integer) # 项目表的id
    sort = db.Column(db.Integer)  # 记录用户的排序

# 创建初始化数据
@app.cli.command()
def forge():
    # 先删除之前的记录,再创建数据库表
    db.drop_all()
    db.create_all()
    # 向项目表中插入数据
    projects=[
        {'name':'项目1'},
        {'name':'项目2'},
        {'name':'项目3'},
    ]
    for p in projects:
        project = Projects(name=p['name'])
        db.session.add(project)
    # 向任务表中插入数据
    n = datetime.datetime.now()
    tasks=[
        {'title':'逛公园','date':n,'condition':'todo','pid':1,'sort':1},
        {'title':'完成游戏','date':n,'condition':'todo','pid':1,'sort':2},
        {'title':'吃饭','date':n,'condition':'done','pid':1,'sort':3},
        {'title':'上王者','date':n,'condition':'done','pid':1,'sort':4},
        {'title': '撸猫', 'date': n, 'condition': 'todo', 'pid': 2,'sort':5},
        {'title': '看电视剧', 'date': n, 'condition': 'todo', 'pid': 2,'sort':6},
        {'title': '逛街', 'date': n, 'condition': 'done', 'pid': 2,'sort':7},
        {'title': '去XX景区', 'date': n, 'condition': 'done', 'pid': 3,'sort':8},
    ]
    for t in tasks:
        task = Tasks(title=t['title'],date=t['date'],condition=t['condition'],pid=t['pid'],sort=t['sort'])
        db.session.add(task)
    db.session.commit()
    click.echo('Done')


@app.route('/gettasks',methods=['GET','POST'])
def gettasks():
    tasks = []
    ts = Tasks.query.filter_by(pid=2).all()
    for t in ts:
        d = datetime.datetime.strftime(t.date, "%Y-%m-%d")
        r = {'id':t.id,'title':t.title,'date':d,'condition':t.condition,'pid':t.pid}
        tasks.append(r)
    print(tasks)
    res = make_response(json.dumps(tasks))
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.status = '200'
    return res

@app.route('/getprojects')
def getprojects():
    ps = Projects.query.all()
    projects = []
    for p in ps:
        r = {'id':p.id,'name':p.name}
        projects.append(r)
    print(projects)
    res = make_response(json.dumps(projects))
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.status = '200'
    return res
#
if __name__ == '__main__':
    app.run()
