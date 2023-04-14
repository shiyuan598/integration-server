# coding=utf8
# 待办
import json
from flask import Blueprint, request, jsonify
from Model import Todo, Project, App_process, User
from sqlalchemy import func, text, and_, or_, asc, desc, case
from sqlalchemy.orm import aliased
from common.utils import generateEntries
from exts import db
session = db.session

todo = Blueprint("todo", __name__)

# 待办列表
@todo.route('/list', methods=["GET"])
def search():
    try:
        # 接收参数
        pageNo = int(request.args.get("pageNo", 1))
        pageSize = int(request.args.get("pageSize", 10))
        orderField = request.args.get("order", "")
        orderSeq = request.args.get("seq", "")
        filter = request.args.get("state", 0)
        user_id = int(request.args.get("user_id"))
        # 查询总数据量
        query = session.query(func.count(Todo.id)).filter(or_(Todo.creator == user_id, Todo.handler == user_id))
        if filter != "":
            query = query.filter(Todo.state == int(filter))
        
        total = query.scalar()
        session.close()
        if total == 0:
            return jsonify({"code": 0, "data": [], "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})

        # 表别名，便于多次join同一个表
        S = aliased(User)
        T = aliased(User)
        # 查询分页数据
        query = session.query(Todo.id, Todo.type, Todo.process_id, Todo.project, Project.name.label("project_name"), Todo.build_type,
            Todo.version, Todo.module_name, Todo.creator, S.name.label("creator_name"), Todo.handler, T.name.label("handler_name"), Todo.desc,
            func.date_format(func.date_add(Todo.create_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
            func.date_format(func.date_add(Todo.update_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
            case(
                (Todo.type == 0, "接口集成"),
                (Todo.type == 1, "应用集成")
            ).label("type_name")
        ).join(
            Project,
            Todo.project == Project.id,
            isouter=True
        ).join(
            S,
            Todo.creator == S.id,
            isouter = True
        ).join(
            T,
            Todo.handler == T.id,
            isouter = True
        )
        query = query.filter(or_(Todo.creator == user_id, Todo.handler == user_id))
        if filter != "": # 查询历史待办
            query = query.filter(Todo.state == int(filter))

        # 设置排序
        if orderField != "" and orderSeq != "":
            if orderSeq == "ascend":
                query = query.order_by(asc(orderField))
            else:
                query = query.order_by(desc(orderField))
        
        result = query.limit(pageSize).offset((pageNo - 1) * pageSize).all()
        session.close()
        data = generateEntries(["id", "type", "process_id", "project", "project_name", "build_type", "version", "module_name", 
        "creator", "creator_name", "handler", "handler_name", "desc", "create_time", "update_time", "type_name"], result)
        return jsonify({"code": 0, "data": data, "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 创建待办消息, 类型：0-接口集成，1-应用集成
def create_todo(type, process_id, project, build_type, version, creator, desc, modulesStr):
    try:
      modules = json.loads(modulesStr)
      # 删除之前的待办消息
      session.query(Todo).filter(Todo.process_id == process_id).delete()
      session.commit()
      session.close()
      for key, value in modules.items():
        # base模块不需要创建待办, 填写过version的不需要创建待办
        if value["type"] != 0 and value["version"] == "":
            data = Todo(type=type, process_id=process_id, project=project, build_type=build_type, version=version, creator=creator, desc=desc,
                module_name=key, handler=value["owner"])
            session.add(data)
            session.commit()
            session.close()
    except Exception as e:
        session.rollback()
        print('An exception occurred at create_todo', str(e), flush=True)

# 处理待办消息
@todo.route('/handle', methods=["POST"])
# 类型：0-接口集成，1-应用集成
def handle_todo():
    try:
        type = request.json.get("type")
        id = request.json.get("id")
        process_id = request.json.get("process_id")
        module_name = request.json.get("module_name")
        version = request.json.get("version")
        release_note = request.json.get("release_note")
        # 1.更新 *应用* 集成流程的模块信息及状态
        if type == 1:
            update_app_process_module(process_id, module_name, version, release_note)
        # 2.更新待办消息的状态
        session.query(Todo).filter(Todo.id == id).update({"state": 1})
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        print('An exception occurred at create_todo', str(e), flush=True)

# 更新应用集成的模块
def update_app_process_module(id, module_name, version, release_note):
    try:
        result = session.query(App_process.modules).filter(App_process.id == id).all()
        modules = json.loads(result[0].modules)
        print("\n\n modules:", modules, "\n\n", type(modules))
        modules[module_name]["version"] = version
        modules[module_name]["release_note"] = release_note
        print("\n\n modules:", json.dumps(modules, indent=4), "\n\n", type(modules))
        keys = modules.keys()
        state = 1
        # 所有模块信息填写完整后状态为已就绪
        for key in keys:
            if modules[key]["version"] is "":
                state = 0
        session.query(App_process).filter(App_process.id == id).update({           
            "modules": json.dumps(modules, indent=4),
            "state": state
        })
        session.commit()
        session.close()
        return True
    except Exception as e:
        session.rollback()
        return False