# coding=utf8
# 加油相关
from flask import Blueprint, request, jsonify
from Model import Notice
from sqlalchemy import func, text, and_
from common.utils import generateEntries
from exts import db
session = db.session

notice = Blueprint("notice", __name__)

# 查询最新的8条公告
@notice.route('/list', methods=["GET"])
def search():
    try:
        result = session.query(
            Notice.id, Notice.title, Notice.content,
            func.date_format(func.date_add(Notice.createtime, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i').label("createTime")
        ).filter(
            and_(Notice.isDel == 0, Notice.expire > func.date_add(func.now(), text("INTERVAL 8 Hour")))
        ).order_by(Notice.createtime.desc()).limit(8).all()
        session.close()        
        data = generateEntries(["id", "title", "content", "createTime"], result)
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 添加公告
@notice.route('/add', methods=["POST"])
def add():
    try:
        title = request.json.get("title")
        content = request.json.get("content")
        expire = request.json.get("expire")
        data = Notice(title=title, content=content, expire=expire)
        session.add(data)
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 删除公告
@notice.route('/delete', methods=["POST", "DELETE"])
def delete():
    try:
        id = request.json.get("id")      
        session.query(Notice).filter(Notice.id == id).update({
            "isDel": 1
        })  
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})