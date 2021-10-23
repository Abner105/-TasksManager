import datetime

from flask import Flask,make_response,request
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
        {'title':'项目1-任务1','date':n,'condition':'todo','pid':1,'sort':2},
        {'title':'项目1-任务2','date':n,'condition':'todo','pid':1,'sort':1},
        {'title':'项目1-任务3','date':n,'condition':'done','pid':1,'sort':-1},
        {'title':'项目1-任务4','date':n,'condition':'done','pid':1,'sort':-2},
        {'title': '项目2-任务1', 'date': n, 'condition': 'todo', 'pid': 2,'sort':2},
        {'title': '项目2-任务2', 'date': n, 'condition': 'todo', 'pid': 2,'sort':1},
        {'title': '项目2-任务3', 'date': n, 'condition': 'done', 'pid': 2,'sort':-1},
        {'title': '项目3-任务1', 'date': n, 'condition': 'done', 'pid': 3,'sort':-1},
    ]
    for t in tasks:
        task = Tasks(title=t['title'],date=t['date'],condition=t['condition'],pid=t['pid'],sort=t['sort'])
        db.session.add(task)
    db.session.commit()
    click.echo('Done')


# 获取所有项目
@app.route('/getprojects',methods=['POST'])
def getprojects():
    ps = Projects.query.all()
    projects = []
    if ps:
        for p in ps:
            r = {'id':p.id,'name':p.name}
            projects.append(r)
    # print(projects)
    res = make_response(json.dumps(projects))
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.status = '200'
    return res


# 添加项目
@app.route('/addproject',methods=['POST','OPTIONS'])
def addproject():
    data = request.json
    if data:
        project = Projects(name=data['name'])
        db.session.add(project)
        db.session.flush()
        pid = project.id
        print(pid)
        db.session.commit()
        res = make_response(json.dumps([{'id':pid}]))
    else:
        res = make_response(json.dumps([{'msg':'请稍等'}]))
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers["Access-Control-Allow-Headers"] = "x-requested-with,Content-Type"
    res.status = '200'
    return res


# 删除项目
@app.route('/delproject',methods=['POST','OPTIONS'])
def delproject():
    data = request.json
    if data:
        # 删除项目表的项目
        project = Projects.query.get(data['id'])
        db.session.delete(project)
        # 删除任务表中该项目的任务
        tasks = Tasks.query.filter_by(pid=data['id']).all()
        for task in tasks:
            db.session.delete(task)
        db.session.commit()
    res = make_response(json.dumps([{'msg':'成功删除项目'}]))
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers["Access-Control-Allow-Headers"] = "x-requested-with,Content-Type"
    res.status = '200'
    return res


# 修改项目
@app.route('/alterproject',methods=['POST','OPTIONS'])
def alterproject():
    data = request.json
    if data:
        project = Projects.query.get(data['id'])
        project.name = data['name']
        db.session.commit()
    res = make_response(json.dumps([{'msg':'修改项目成功'}]))
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers["Access-Control-Allow-Headers"] = "x-requested-with,Content-Type"
    res.status = '200'
    return res


# 获取任务列表
@app.route('/gettasks',methods=['POST','OPTIONS'])
def gettasks():
    data = request.json
    # print(data)
    tasks = []
    if data:
        ts = Tasks.query.filter_by(pid=data['id']).order_by(Tasks.sort.desc()).all()
        for t in ts:
            # 将数据库中的时间切割为年月日的格式
            d = datetime.datetime.strftime(t.date, "%Y-%m-%d")
            r = {'id':t.id,'title':t.title,'date':d,'condition':t.condition,'pid':t.pid}
            tasks.append(r)
    # print(tasks)
    res = make_response(json.dumps(tasks))
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers["Access-Control-Allow-Headers"] = "x-requested-with,Content-Type"
    res.status = '200'
    return res


# 添加任务
@app.route('/addtask',methods=['POST','OPTIONS'])
def addtask():
    data = request.json
    if data:
        n = datetime.datetime.now()
        newsort = 0
        max = Tasks.query.filter_by(pid=data['pid']).order_by(Tasks.sort.desc()).first()
        if max:
            newsort = max.sort + 1
        task = Tasks(title=data['title'],date=n,condition='todo',pid=data['pid'],sort=newsort)
        db.session.add(task)
        db.session.commit()
    res = make_response(json.dumps([{'msg':'添加任务成功'}]))
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers["Access-Control-Allow-Headers"] = "x-requested-with,Content-Type"
    res.status = '200'
    return res


# 完成任务
@app.route('/done',methods=['POST','OPTIONS'])
def done():
    data = request.json
    if data:
        newsort = Tasks.query.filter_by(pid=data['pid']).order_by(Tasks.sort).first().sort - 1
        task = Tasks.query.get(data['id'])
        task.condition = 'done'
        task.sort = newsort
        db.session.commit()
    res = make_response(json.dumps([{'msg':'成功完成任务'}]))
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers["Access-Control-Allow-Headers"] = "x-requested-with,Content-Type"
    res.status = '200'
    return res


# 删除任务
@app.route('/deltask',methods=['POST','OPTIONS'])
def deltask():
    data = request.json
    if data:
        task = Tasks.query.get(data['id'])
        db.session.delete(task)
        db.session.commit()
    res = make_response(json.dumps([{'msg':'成功删除任务'}]))
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers["Access-Control-Allow-Headers"] = "x-requested-with,Content-Type"
    res.status = '200'
    return res


# 置顶任务
@app.route('/toptask',methods=['POST','OPTIONS'])
def toptask():
    data = request.json
    if data:
        newsort = Tasks.query.filter_by(pid=data['pid']).order_by(Tasks.sort.desc()).first().sort + 1
        task = Tasks.query.get(data['id'])
        task.sort = newsort
        db.session.commit()
    res = make_response(json.dumps([{'msg':'置顶任务成功'}]))
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers["Access-Control-Allow-Headers"] = "x-requested-with,Content-Type"
    res.status = '200'
    return res


# 修改任务
@app.route('/altertask',methods=['POST','OPTIONS'])
def altertask():
    data = request.json
    if data:
        task = Tasks.query.get(data['id'])
        task.title = data['title']
        db.session.commit()
    res = make_response(json.dumps([{'msg':'修改任务成功'}]))
    res.headers['Content-Type'] = 'application/json; charset=utf-8'
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers["Access-Control-Allow-Headers"] = "x-requested-with,Content-Type"
    res.status = '200'
    return res


if __name__ == '__main__':
    app.run()
