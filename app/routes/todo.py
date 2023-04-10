# coding=utf8
# 待办
import json
from flask import Blueprint, request, jsonify
from Model import Todo
from sqlalchemy import func, text, and_, or_, asc, desc, case
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
        # 查询总数据量
        query = session.query(func.count(Todo.id))
        if filter != "":
            query = query.filter(Todo.state == int(filter))
        
        total = query.scalar()
        session.close()
        if total == 0:
            return jsonify({"code": 0, "data": [], "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})

        # 查询分页数据
        query = session.query(Todo.id, Todo.type, Todo.process_id, Todo.version, Todo.module, Todo.creator, Todo.handler, Todo.desc,
            func.date_format(func.date_add(Todo.create_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
            func.date_format(func.date_add(Todo.update_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'))
        if filter != "":
            query = query.filter(Todo.state == int(filter))

        # 设置排序
        if orderField != "" and orderSeq != "":
            if orderSeq == "ascend":
                query = query.order_by(asc(orderField))
            else:
                query = query.order_by(desc(orderField))
        
        result = query.limit(pageSize).offset((pageNo - 1) * pageSize).all()
        session.close()
        data = generateEntries(["id", "type", "process_id", "version", "module", "creator", "handler", "desc", "create_time", "update_time"], result)
        return jsonify({"code": 0, "data": data, "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})


def create_todo(type, process_id, version, creator, desc, modules):
    try:
      modules = json.loads(modules)
      # 删除之前的待办消息
      session.query(Todo).filter(Todo.process_id == process_id).delete()
      session.commit()
      session.close()
      for key, value in modules.items():
        # base模块不需要创建待办, 填写过version的不需要创建待办
        if value["type"] != 0 and value["version"] == "":
            data = Todo(type=type, process_id=process_id, version=version, creator=creator, desc=desc,
                module=key, handler=value["owner"])
            session.add(data)
            session.commit()
            session.close()
    except Exception as e:
        session.rollback()
        print('An exception occurred at create_todo', str(e), flush=True)
