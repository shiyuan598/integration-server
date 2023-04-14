# coding=utf8
# 项目管理
from flask import Blueprint, request, jsonify
from Model import Project, Module, User
from sqlalchemy import func, text, and_, or_, asc, desc, case
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
        query = session.query(Project.id, Project.name, Project.platform, Project.job_name, Project.artifacts_path, Project.owner, User.name.label("owner_name"), Project.desc,
        func.date_format(func.date_add(Project.create_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
        func.date_format(func.date_add(Project.update_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i')
        ).join(
            User,
            User.id == Project.owner,
            isouter=True
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
        data = generateEntries(["id", "name", "platform", "job_name", "artifacts_path", "owner", "owner_name", "desc", "create_time", "update_time"], result)
        return jsonify({"code": 0, "data": data, "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 所有项目(不分页)
@project.route('/list_all', methods=["GET"])
def search_all():
    try:
        # 查询所有数据
        query = session.query(Project.id, Project.name, Project.platform, Project.job_name, Project.artifacts_path, Project.owner)
        result = query.all()
        session.close()
        data = generateEntries(["id", "name", "platform", "job_name", "artifacts_path", "owner"], result)
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
        query = session.query(Module.id, Module.name, Module.git, Module.owner, User.name.label("owner_name"), Module.desc,
        Module.type, case(
                (Module.type == 0, "Base"),
                (Module.type == 1, "接口"),
                (Module.type == 2, "应用")
        ).label("type_name"),
        func.date_format(func.date_add(Module.create_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
        func.date_format(func.date_add(Module.update_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i')
        ).join(
            User,
            User.id == Module.owner,
            isouter=True
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
        data = generateEntries(["id", "name", "git", "owner", "owner_name", "desc", "type", "type_name", "create_time", "update_time"], result)
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
        types = request.args.getlist("type")
        # 查询所有数据
        query = session.query(Module.id, Module.name, Module.type, Module.git, Module.owner, User.name.label("owner_name")
        ).join(
            User,
            User.id == Module.owner,
            isouter=True
        ).filter(Module.project == project_id)
        if len(types) > 0:
            types = tuple(types[0].split(","))
            query = query.filter(Module.type.in_(types))
        result = query.all()
        session.close()
        data = generateEntries(["id", "name", "type", "git", "owner", "owner_name"], result)
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 某项目下同一类型的所有模块(不分页)
@project.route('/<int:project_id>/module_type_all/<int:type>', methods=["GET"])
def modules_all_type(project_id, type=0):
    try:
        # 接收参数
        project_id = request.view_args['project_id']
        # 查询所有数据
        query = session.query(Module.id, Module.name, Module.git, Module.owner).filter(and_(Module.project == project_id, Module.type == type))
        result = query.all()
        session.close()
        data = generateEntries(["id", "name", "git", "owner"], result)
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})
