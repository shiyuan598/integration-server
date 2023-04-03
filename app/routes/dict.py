# coding=utf8
# 字典
from flask import Blueprint, request, jsonify
from Model import Project, Module, Load
from common.utils import generateEntries
from exts import db
session = db.session

dict = Blueprint("dict", __name__)

# 查询所属项目
@dict.route('/project', methods=["GET"])
def project():
    try:
        result = session.query(Project.id, Project.name, Project.desc).all()
        session.close()
        data = generateEntries(["id", "name", "desc"], result)
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 查询所属模块
@dict.route('/module', methods=["GET"])
def module():
    try:
        pid = request.args.get("pid", 0)
        result = session.query(Module.id, Module.name, Module.desc).filter(
            Module.pid == pid).all()
        session.close()
        data = generateEntries(["id", "name", "desc"], result)
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 查询车辆带挂
@dict.route('/load', methods=["GET"])
def load():
    try:
        result = session.query(Load.id, Load.name, Load.desc).all()
        session.close()
        data = generateEntries(["id", "name", "desc"], result)
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})
