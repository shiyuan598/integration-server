# coding=utf8
# 应用集成
from flask import Blueprint, request, jsonify
from Model import App_process, Project, Process_state
from sqlalchemy import func, text, and_, or_, asc, desc
from common.utils import generateEntries
from common.jenkins_tool import update_build_state
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
        type = int(request.args.get("type", 1))
        user_id = int(request.args.get("user_id"))
        # 查询总数据量
        query = session.query(func.count(App_process.id)).filter(or_(
            App_process.project.like("%{}%".format(name)),
            App_process.version.like("%{}%".format(name)),
            App_process.api_version.like("%{}%".format(name))
        )).filter( # 查询系统级的集成流程或自己创建的流程
            or_(App_process.type == 1, App_process.creator == user_id)
        )            
        
        total = query.scalar()
        session.close()
        if total == 0:
            return jsonify({"code": 0, "data": [], "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})

        # 更新流程状态
        runningData = session.query(App_process.id, App_process.job_name, App_process.build_number, App_process.build_queue).filter(App_process.state == 2).all()
        session.close()
        update_build_state(runningData, "App_process")

        # 查询分页数据
        query = session.query(App_process.id, App_process.project, App_process.build_type, App_process.version, App_process.api_version,
        App_process.job_name, App_process.build_queue, App_process.build_number, App_process.jenkins_url, App_process.artifactory_url,
        App_process.creator, App_process.modules, App_process.state, Process_state.name.label("state_name"), App_process.desc, Project.name.label("project_name"),
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
        ).filter(or_(
            App_process.project.like("%{}%".format(name)),
            App_process.version.like("%{}%".format(name)),
            App_process.api_version.like("%{}%".format(name))
        )).filter( # 查询系统级的集成流程或自己创建的流程
            or_(App_process.type == 1, App_process.creator == user_id)
        )

        if type == 1:
            query = query.filter(App_process.type == type)
        
        # 设置排序
        if orderField != "" and orderSeq != "":
            if orderSeq == "ascend":
                query = query.order_by(asc(orderField))
            else:
                query = query.order_by(desc(orderField))
        
        result = query.limit(pageSize).offset((pageNo - 1) * pageSize).all()
        session.close()
        data = generateEntries(["id", "project", "build_type", "version", "api_version", "job_name", "build_queue", "build_number",
        "jenkins_url", "artifactory_url", "creator", "modules", "state", "state_name", "desc", "project_name", "create_time", "update_time"], result)
        return jsonify({"code": 0, "data": data, "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})
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
        state = int(request.json.get("state"))
        data = App_process(project=project, version=version, build_type=build_type, 
        job_name=job_name, modules=modules, creator=creator, type=type, state=state, desc=desc)
        session.add(data)
        session.flush()
        id = data.id
        session.commit()
        session.close()

        # 创建待办消息
        create_todo(type=1, process_id=id, version=version, creator=creator, desc=desc, modules=modules)
        
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
        if type == 1:
            create_todo(type=1, process_id=id, version=version, creator=creator, desc=desc, modules=modules)
            
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 更新应用集成中的模块配置
@app_process.route('/update_module', methods=["POST"])
def update_module():
    try:
        id = request.json.get("id")
        modules = request.json.get("modules")
        state = request.json.get("state")
        session.query(App_process).filter(App_process.id == id).update({           
            "modules": modules,
            "state": int(state) # 所有模块信息填写完整后状态为已就绪
        })
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})
