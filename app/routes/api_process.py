# coding=utf8
# 接口集成
from flask import Blueprint, request, jsonify
from Model import Api_process
from sqlalchemy import func, text, and_, or_, asc, desc
from common.utils import generateEntries
from exts import db
session = db.session

api_process = Blueprint("api_process", __name__)

# 查询最新的8条公告
@api_process.route('/list', methods=["GET"])
def search():
    try:
        # 接收参数
        pageNo = int(request.args.get("pageNo", 1))
        pageSize = int(request.args.get("pageSize", 10))
        name = request.args.get("name", "")
        orderField = request.args.get("order", "")
        orderSeq = request.args.get("seq", "")
        # 查询总数据量
        total = session.query(func.count(Api_process.id)).filter(or_(
            Api_process.project.like("%{}%".format(name)),
            Api_process.version.like("%{}%".format(name)),
            Api_process.release_note.like("%{}%".format(name))
        )).scalar()
        session.close()
        if total == 0:
            return jsonify({"code": 0, "data": [], "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})

        # 查询分页数据
        query = session.query(Api_process.id, Api_process.project, Api_process.build_type, Api_process.version, Api_process.release_note, 
        Api_process.creator, Api_process.modules, Api_process.state,
        func.date_format(func.date_add(Api_process.create_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
        func.date_format(func.date_add(Api_process.update_time, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i'),
        ).filter(or_(
            Api_process.project.like("%{}%".format(name)),
            Api_process.version.like("%{}%".format(name)),
            Api_process.release_note.like("%{}%".format(name))
        ))

        # 设置排序
        if orderField != "" and orderSeq != "":
            if orderSeq == "ascend":
                query = query.order_by(asc(orderField))
            else:
                query = query.order_by(desc(orderField))
        
        result = query.limit(pageSize).offset((pageNo - 1) * pageSize).all()
        session.close()
        data = generateEntries(["id", "project", "build_type", "version", "release_note", "creator", "modules", "state", "create_time", "update_time"], result)
        return jsonify({"code": 0, "data": data, "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# # 添加公告
# @notice.route('/add', methods=["POST"])
# def add():
#     try:
#         title = request.json.get("title")
#         content = request.json.get("content")
#         expire = request.json.get("expire")
#         data = Notice(title=title, content=content, expire=expire)
#         session.add(data)
#         session.commit()
#         session.close()
#         return jsonify({"code": 0, "msg": "成功"})
#     except Exception as e:
#         session.rollback()
#         return jsonify({"code": 1, "msg": str(e)})

# # 删除公告
# @notice.route('/delete', methods=["POST", "DELETE"])
# def delete():
#     try:
#         id = request.json.get("id")      
#         session.query(Notice).filter(Notice.id == id).update({
#             "isDel": 1
#         })  
#         session.commit()
#         session.close()
#         return jsonify({"code": 0, "msg": "成功"})
#     except Exception as e:
#         session.rollback()
#         return jsonify({"code": 1, "msg": str(e)})