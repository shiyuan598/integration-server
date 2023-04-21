# coding=utf8
# 应用集成
from flask import Blueprint, request, jsonify
from Model import App_process, Project, Process_state, User
from sqlalchemy import func, text, and_, or_, asc, desc
from common.utils import generateEntries

from common.jenkins_tool import app_process_log

from .todo import create_todo
from exts import db
session = db.session

app_process = Blueprint("app_process", __name__)

# 应用集成流程列表
@app_process.route('/list', methods=["GET"])
def search():
    try:
        # 接收参数
        pageNo = int(request.args.get("pageNo", 1))
        pageSize = int(request.args.get("pageSize", 10))
        name = request.args.get("name", "")
        orderField = request.args.get("order", "")
        orderSeq = request.args.get("seq", "")
        user_id = int(request.args.get("user_id"))
        # 查询总数据量
        query = session.query(func.count(App_process.id)).filter(or_(
            App_process.project.like("%{}%".format(name)),
            App_process.version.like("%{}%".format(name)),
            App_process.api_version.like("%{}%".format(name))
        )).filter( # 查询系统级的集成流程或自己创建的流程
            or_(App_process.type == 0, App_process.creator == user_id)
        )            
        
        total = query.scalar()
        session.close()
        if total == 0:
            return jsonify({"code": 0, "data": [], "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})

        # 查询分页数据
        query = session.query(App_process.id, App_process.project, App_process.build_type, App_process.version, App_process.api_version,
        App_process.job_name, App_process.build_queue, App_process.build_number, App_process.jenkins_url, App_process.artifacts_url, App_process.confluence_url,
        App_process.creator, User.name.label("creator_name"), App_process.modules, App_process.state, Process_state.name.label("state_name"),
        App_process.type, App_process.desc, Project.name.label("project_name"),
        func.date_format(func.date_add(App_process.create_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
        func.date_format(func.date_add(App_process.update_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
        ).join(
            Project,
            App_process.project == Project.id,
            isouter=True
        ).join(
            Process_state,
            App_process.state == Process_state.state,
            isouter=True
        ).join(
            User,
            User.id == App_process.creator,
            isouter=True
        ).filter(or_(
            App_process.project.like("%{}%".format(name)),
            App_process.version.like("%{}%".format(name)),
            App_process.api_version.like("%{}%".format(name))
        )).filter( # 查询系统级的集成流程或自己创建的流程
            or_(App_process.type == 0, App_process.creator == user_id)
        )
        # 设置排序
        if orderField != "" and orderSeq != "":
            if orderSeq == "ascend":
                query = query.order_by(asc(orderField))
            else:
                query = query.order_by(desc(orderField))
        
        result = query.limit(pageSize).offset((pageNo - 1) * pageSize).all()
        session.close()
        data = generateEntries(["id", "project", "build_type", "version", "api_version", "job_name", "build_queue", "build_number", "jenkins_url",
        "artifacts_url", "confluence_url", "creator", "creator_name", "modules", "state", "state_name", "type", "desc", "project_name", "create_time", "update_time"], result)
        return jsonify({"code": 0, "data": data, "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 检查名称是否可用，不存在
@app_process.route("/version/noexist", methods=["GET"])
def checkExist():
    try:
        project = request.args.get("project")
        creator = request.args.get("creator")
        version = request.args.get("version")
        total = session.query(func.count(App_process.id)).filter(
            and_(
                App_process.project == project,
                App_process.creator == creator,
                App_process.version == version
                )
            ).scalar()
        session.close()
        return jsonify({"code": 0, "data": (total == 0), "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 创建应用集成
@app_process.route('/create', methods=["POST"])
def create():
    try:
        project = request.json.get("project")
        version = request.json.get("version")
        build_type = request.json.get("build_type")
        # api_version = request.json.get("api_version")
        desc = request.json.get("desc")
        job_name = request.json.get("job_name")
        modules = request.json.get("modules")
        creator = request.json.get("creator")
        type = request.json.get("type")
        artifacts_url = request.json.get("artifacts_url")
        state = int(request.json.get("state"))
        data = App_process(project=project, version=version, build_type=build_type, job_name=job_name, 
        modules=modules, creator=creator, type=type, artifacts_url=artifacts_url, state=state, desc=desc)
        session.add(data)
        session.flush()
        id = data.id
        session.commit()
        session.close()

        # 系统应用创建待办消息
        if type == 0:
            # 类型：0-接口集成，1-应用集成
            create_todo(type=1, process_id=id, project=project, build_type=build_type, version=version, creator=creator, desc=desc, modulesStr=modules)
        
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})


# 编辑应用集成
@app_process.route('/edit', methods=["POST"])
def edit():
    try:
        id = request.json.get("id")
        project = request.json.get("project")
        version = request.json.get("version")
        build_type = request.json.get("build_type")
        # api_version = request.json.get("api_version")
        desc = request.json.get("desc")
        job_name = request.json.get("job_name")
        modules = request.json.get("modules")
        creator = request.json.get("creator")
        type = request.json.get("type")
        state = int(request.json.get("state"))
        session.query(App_process).filter(App_process.id == id).update({
            "project": project,
            "version": version,
            "build_type": build_type,
            "desc": desc,
            "job_name": job_name,
            "modules": modules,
            "state": int(state)
        })
        session.commit()
        session.close()

        # 系统应用创建待办消息
        if type == 0:
            # 类型：0-接口集成，1-应用集成
            create_todo(type=1, process_id=id, project=project, build_type=build_type, version=version, creator=creator, desc=desc, modulesStr=modules)
            
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 更新应用集成中的模块配置
@app_process.route('/modules', methods=["GET"])
def modules():
    try:
        id = request.args.get("id")
        result = session.query(App_process.modules).filter(App_process.id == id).all()
        session.commit()
        session.close()
        if result[0] is not None:
            return jsonify({"code": 0, "data": {"modules": result[0][0]}, "msg": "成功"})
        else:
            return jsonify({"code": 0, "data": {"modules": ""}, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

@app_process.route('/log', methods=["GET"])
def log():
    try:
        id = request.args.get("id")
        app_process_log(id)
        
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})