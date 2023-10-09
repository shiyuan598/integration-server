# coding=utf8
import os
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from exts import db
from flask_sqlalchemy import record_queries
import time
from routes.blueprint import registerRoute
from routes.user import check_token
from apscheduler.schedulers.background import BackgroundScheduler
from common.jenkins_tool import schedule_task
from common.redis_tool import redis as redis_conn
from flask_migrate import Migrate
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

app = Flask(__name__)
app.config.from_object('config.setting')
# 全局允许跨域
CORS(app, supports_credentials=True)

db.init_app(app)

# 数据迁移
migrate = Migrate(app, db)

# 注册路由
registerRoute(app)

# 创建所有的表，需要放在路由后面
with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return 'Hello World!'

# 不需要校验的接口
NOT_CHECK_URL = [
    "/", "/api/user/login", "/api/user/register", "/api/user/list/all", "/api/app_process/log",
    "/api/user/check/noexist", "/api/user/check/correct", "/api/user/resetpwd"
]
ALLOW_METHOD = ["GET", "POST", "DELETE", "PUT"]


@app.before_request
def auth_check():
    if request.method in ALLOW_METHOD and request.path not in NOT_CHECK_URL:
        Authorization = request.headers.get('Authorization')
        if Authorization != '' or Authorization != None:
            #如果当前登录态没有过期则什么都不做，否则拦截
            if check_token(Authorization) != True:
                return jsonify({'msg': '无效状态'}), 401
            pass
        else:
            return jsonify({'msg': '无效状态'}), 401
    else:
        pass


@app.after_request
def after_request(response):
    for query in record_queries.get_recorded_queries():
        if query.duration > app.config["FLASKY_DB_QUERY_TIMEOUT"]:
            startTime = time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime(int(query.start_time)))
            print("\t", ('\n时间: {}\n时长: {}\nSQL: {}\n参数: {}').format(
                startTime, query.duration, query.statement, str(query.parameters)[0:150]), flush=True)
    if (response.status_code != 200):
        print(("\n响应出错：\ntime:{}\nstatus:{}\ndata:{}").format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), response.status_code, response.data.decode("utf-8")), flush=True)
    return response


@app.teardown_request
def teardown_request(e):
    db.session.remove()

# 定时任务, 更新流程的状态
def run_schedule_task():
    with app.app_context():
        schedule_task()

def init_scheduler():
    print(f"\n\n初始化定时任务\n", flush=True)
    scheduler = BackgroundScheduler(max_instances=10)
    scheduler.add_job(run_schedule_task, "interval", seconds=60)
    scheduler.start()

# 获取分布式锁
def acquire_lock():
    return redis_conn.set(lock_key, os.getpid(), nx=True, ex=60)

# 定义文件路径和锁文件路径
file_path = 'schedule_task.file'
lock_key = 'schedule_task_lock'

# 释放分布式锁
def release_lock():
    redis_conn.delete(lock_key)

# 尝试获取分布式锁
if acquire_lock():
    try:
        # 检查任务文件是否存在，如果不存在则执行任务
        if not os.path.exists(file_path):
            print(f"\n 任务文件不存在, 初始化定时任务！", flush=True)
            # 执行定时任务
            init_scheduler()
            # 创建任务文件
            with open(file_path, 'w') as task_file:
                task_file.write(str(os.getpid()))
        else:
            print(f"\n 任务文件已存在, 不再进行定时任务初始化！", flush=True)
    finally:
        # 释放分布式锁
        release_lock()
else:
    print("Another process is already running the task.", flush=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9021, debug=False)
