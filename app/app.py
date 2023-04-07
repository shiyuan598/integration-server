# coding=utf8

import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from exts import db
from flask_sqlalchemy import get_debug_queries, SQLAlchemy
import time
from routes.blueprint import registerRoute
# from routes.user import check_token

app = Flask(__name__)
app.config.from_object('config.setting')
db.init_app(app)

# 全局允许跨域
CORS(app, supports_credentials=True)

# 注册路由
registerRoute(app)

# 创建所有的表，需要放在路由后面
db.create_all(app=app)


@app.route('/')
def hello():
    return 'Hello World!'


NOT_CHECK_URL = [
    "/", "/api/user/login", "/api/user/register",
    "/api/user/check/noexist", "/api/user/check/correct", "/api/user/resetpwd"
]
ALLOW_METHOD = ["GET", "POST", "DELETE", "PUT"]


# @app.before_request
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
    for query in get_debug_queries():
        if query.duration > app.config["FLASKY_DB_QUERY_TIMEOUT"]:
            startTime = time.strftime("%Y-%m-%d %H:%M:%S",
                                      time.localtime(int(query.start_time)))
            print("\t", ('\n时间: {}\n时长: {}\nSQL: {}\n参数: {}').format(
                startTime, query.duration, query.statement, str(query.parameters)[0:150]), flush=True)
    if (response.status_code is not 200):
        print(("\n响应出错：\ntime:{}\nstatus:{}\ndata:{}").format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), response.status_code, response.data.decode("utf-8")), flush=True)
    return response


@app.teardown_request
def teardown_request(e):
    db.session.remove()


if __name__ == '__main__':
    app.run(host="172.16.12.84", port=9002, debug=False)
