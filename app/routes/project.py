# coding=utf8
# 项目管理
from flask import Blueprint, request, jsonify
from Model import Project, Module
from sqlalchemy import func, text, and_, or_, asc, desc
from common.utils import generateEntries
from exts import db
session = db.session

project = Blueprint("project", __name__)

# 项目列表
@project.route('/list', methods=["GET"])
def search():
    try:
        # 接收参数
        pageNo = int(request.args.get("pageNo", 1))
        pageSize = int(request.args.get("pageSize", 10))
        name = request.args.get("name", "")
        orderField = request.args.get("order", "")
        orderSeq = request.args.get("seq", "")
        # 查询总数据量
        total = session.query(func.count(Project.id)).filter(or_(
            Project.name.like("%{}%".format(name)),
            Project.platform.like("%{}%".format(name))
        )).scalar()
        session.close()
        if total == 0:
            return jsonify({"code": 0, "data": [], "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})

        # 查询分页数据
        query = session.query(Project.id, Project.name, Project.platform, Project.job_name, Project.owner, Project.desc,
        func.date_format(func.date_add(Project.create_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
        func.date_format(func.date_add(Project.update_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
        ).filter(or_(
            Project.name.like("%{}%".format(name)),
            Project.platform.like("%{}%".format(name))
        ))

        # 设置排序
        if orderField != "" and orderSeq != "":
            if orderSeq == "ascend":
                query = query.order_by(asc(orderField))
            else:
                query = query.order_by(desc(orderField))
        
        result = query.limit(pageSize).offset((pageNo - 1) * pageSize).all()
        session.close()
        data = generateEntries(["id", "name", "platform", "job_name", "owner", "desc", "create_time", "update_time"], result)
        return jsonify({"code": 0, "data": data, "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 某项目下的所有模块(不分页)
@project.route('/list_all', methods=["GET"])
def search_all():
    try:
        # 查询所有数据
        query = session.query(Project.id, Project.name, Project.platform, Project.job_name)
        result = query.all()
        session.close()
        data = generateEntries(["id", "name", "platform", "job_name"], result)
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 某项目下的模块列表
@project.route('/<int:project_id>/module', methods=["GET"])
def modules(project_id):
    try:
        # 接收参数
        project_id = request.view_args['project_id']
        pageNo = int(request.args.get("pageNo", 1))
        pageSize = int(request.args.get("pageSize", 10))
        name = request.args.get("name", "")
        orderField = request.args.get("order", "")
        orderSeq = request.args.get("seq", "")
        # 查询总数据量
        total = session.query(func.count(Module.id)).filter(or_(
            Module.name.like("%{}%".format(name))
        )).filter(Module.project == project_id).scalar()
        session.close()
        if total == 0:
            return jsonify({"code": 0, "data": [], "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})

        # 查询分页数据
        query = session.query(Module.id, Module.name, Module.git, Module.owner, Module.desc,
        func.date_format(func.date_add(Module.create_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
        func.date_format(func.date_add(Module.update_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
        ).filter(or_(
            Module.name.like("%{}%".format(name))
        )).filter(Module.project == project_id)

        # 设置排序
        if orderField != "" and orderSeq != "":
            if orderSeq == "ascend":
                query = query.order_by(asc(orderField))
            else:
                query = query.order_by(desc(orderField))
        
        result = query.limit(pageSize).offset((pageNo - 1) * pageSize).all()
        session.close()
        data = generateEntries(["id", "name", "git", "owner", "desc", "create_time", "update_time"], result)
        return jsonify({"code": 0, "data": data, "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})


# 某项目下的所有模块(不分页)
@project.route('/<int:project_id>/module_all', methods=["GET"])
def modules_all(project_id):
    try:
        # 接收参数
        project_id = request.view_args['project_id']
        # 查询所有数据
        query = session.query(Module.id, Module.name, Module.git).filter(Module.project == project_id)
        result = query.all()
        session.close()
        data = generateEntries(["id", "name", "git"], result)
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})
