# coding=utf8
# 订单相关
from flask import Blueprint, request, jsonify
from Model import Module, Load, Order, User
from sqlalchemy import func, and_, or_, not_, text, asc, desc
from sqlalchemy.orm import aliased
from app.Model import Process_state
from common.utils import generateEntries
from common.sms import sendMessage
from enum import Enum
import re, datetime
from exts import db
session = db.session

# 操作类型，根据类型发送不同的通知消息
class OptType(Enum):
    order=1 #预订
    approve=2 #审批
    cancel=3 #取消
    start=4 #开始
    stop=5 #结束
    delete=6 #删除


order = Blueprint("order", __name__)

def searchOrder(id="", name="", driver="", subscriber="", orderField="", orderSeq="", stateFilter="", pageNo=1, pageSize=10):
    try:
        # 表别名，便于多次join同一个表
        S = aliased(User)
        T = aliased(User)
        U = aliased(User)

        total = 0
        if id == "":
            # 查询总数据量
            query = session.query(func.count(Order.id)
            ).join(
                Module,
                Order.module == Module.id,
                isouter = True
            ).join(
                Load,
                Order.load == Load.id,
                isouter = True
            ).join(
                S,
                Order.subscriber == S.id,
                isouter = True
            ).join(
                T,
                Order.approver == T.id,
                isouter = True
            ).join(
                Process_state,
                Order.state == Process_state.state,
                isouter = True
            )
            if subscriber != "":
                query = query.filter(
                    and_(
                        or_(
                            Order.vehicleNo.like("%{}%".format(name)),
                            Load.name.like("{}%".format(name)),
                            Order.project.like("{}%".format(name)),
                            Module.name.like("%{}%".format(name)),
                            Order.starttime.like("{}%".format(name)),
                            Order.endtime.like("{}%".format(name)),
                            Order.address.like("{}%".format(name)),
                            Process_state.name.like("%{}%".format(name)),
                            S.name.like("%{}%".format(name)),
                            T.name.like("%{}%".format(name))
                        ),
                        Order.subscriber == subscriber
                    ))
            else:
                query = query.filter(
                    or_(
                        Order.vehicleNo.like("%{}%".format(name)),
                        Load.name.like("{}%".format(name)),
                        Order.project.like("{}%".format(name)),
                        Module.name.like("%{}%".format(name)),
                        Order.starttime.like("{}%".format(name)),
                        Order.endtime.like("{}%".format(name)),
                        Order.address.like("{}%".format(name)),
                        Process_state.name.like("%{}%".format(name)),
                        S.name.like("%{}%".format(name)),
                        T.name.like("%{}%".format(name))
                    )
                )
            
            total = query.scalar()
            session.close()
            if total == 0:
                return jsonify({"code": 0, "data": [], "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})

        # 查询分页数据
        query = session.query(
            Order.id, S.username.label("subscriber"), S.name.label("subscriberName"), S.telephone.label("subscriberPhone"), 
            Order.project, Module.name.label("module"), Order.vehicleNo, Order.subscribeNote, 
            func.date_format(Order.starttime, '%Y-%m-%d %H:%i').label("startTime"),
            func.date_format(Order.endtime, '%Y-%m-%d %H:%i').label("endTime"),
            Order.address, Order.purpose, Order.route, Load.name.label("load"),
            func.date_format(func.date_add(Order.createtime, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i').label("createTime"),
            func.date_format(func.date_add(Order.updatetime, text("INTERVAL 8 Hour")), '%Y-%m-%d %H:%i').label("updateTime"),
            T.name.label("approver"), U.name.label("driver"), U.telephone.label("driverPhone"), Order.state, Process_state.name.label("stateName"),
            Order.comment, Order.desc
        ).join(
            Module,
            Order.module == Module.id,
            isouter = True
        ).join(
            Load,
            Order.load == Load.id,
            isouter = True
        ).join(
            S,
            Order.subscriber == S.id,
            isouter = True
        ).join(
            T,
            Order.approver == T.id,
            isouter = True
        ).join(
            U,
            Order.driver == U.id,
            isouter = True
        ).join(
            Process_state,
            Order.state == Process_state.state,
            isouter = True
        )
        if id != "":
            # 1.有id参数时不需要排序及分页
            result = query.filter(Order.id == id).all()
            session.close()
            data = generateEntries(["id", "subscriber", "subscriberName", "subscriberPhone", "project", "module", "vehicleNo", "subscribeNote","startTime", 
                "endTime", "address", "purpose", "route", "load", "createTime", "updateTime", "approver", "driver", "driverPhone", "state", "stateName", "comment", "desc"], result)
            return jsonify({"code": 0, "data": data, "msg": "成功"})
        else:
            # 2.有司机参数时，会有状态过滤及排序字段，不需要分页
            if driver != "":
                if stateFilter != "":
                    query = query.filter(and_(Order.driver == driver, Order.state == stateFilter))
                else:
                    query = query.filter(Order.driver == driver)
                if orderField == "state":
                    query = query.order_by(Order.state.desc())
                else:
                    query = query.order_by(Order.createtime.desc())
            else:
                # 3.其他情况默认时间排序，需要分页              
                if subscriber != "":
                    # 3.1查询个人申请的订单
                    query = query.filter(
                        and_(
                            or_(
                                Order.vehicleNo.like("%{}%".format(name)),
                                Load.name.like("{}%".format(name)),
                                Order.project.like("{}%".format(name)),
                                Module.name.like("%{}%".format(name)),
                                Order.starttime.like("{}%".format(name)),
                                Order.endtime.like("{}%".format(name)),
                                Order.address.like("{}%".format(name)),
                                Process_state.name.like("%{}%".format(name)),
                                S.name.like("%{}%".format(name)),
                                T.name.like("%{}%".format(name))
                            ),
                            Order.subscriber == subscriber
                        ))
                else:
                    # 3.2查询所有订单
                    query = query.filter(
                        or_(
                            Order.vehicleNo.like("%{}%".format(name)),
                            Load.name.like("{}%".format(name)),
                            Order.project.like("{}%".format(name)),
                            Module.name.like("%{}%".format(name)),
                            Order.starttime.like("{}%".format(name)),
                            Order.endtime.like("{}%".format(name)),
                            Order.address.like("{}%".format(name)),
                            Process_state.name.like("%{}%".format(name)),
                            S.name.like("%{}%".format(name)),
                            T.name.like("%{}%".format(name))
                        )
                    )
                # 设置排序
                if orderField != "" and orderSeq != "":
                    if orderSeq == "ascend":
                        query = query.order_by(asc(orderField))
                    else:
                        query = query.order_by(desc(orderField))
                else:
                    # 默认时间字段降序
                    query = query.order_by(Order.createtime.desc())
                # 执行查询
                query = query.limit(pageSize).offset((pageNo - 1) * pageSize)

            result = query.all()
            session.close()
            data = generateEntries(["id", "subscriber", "subscriberName", "subscriberPhone", "project", "module", "vehicleNo", "subscribeNote","startTime", 
                "endTime", "address", "purpose", "route", "load", "createTime", "updateTime", "approver", "driver", "driverPhone", "state", "stateName", "comment", "desc"], result)
            return jsonify({"code": 0, "data": data, "pagination": {"total": total, "current": pageNo, "pageSize": pageSize}, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 查询订单
@order.route('/list', methods=["GET"])
def searchAll():
    try:
        id = request.args.get("id", "")
        name = request.args.get("name", "")
        subscriber = request.args.get("subscriber", "")
        driver = request.args.get("driver", "")
        orderField = request.args.get("order", "")
        orderSeq = request.args.get("seq", "")
        stateFilter = request.args.get("state", "")
        pageNo = int(request.args.get("pageNo", 1))
        pageSize = int(request.args.get("pageSize", 10))
        return searchOrder(id=id, name=name, driver=driver, subscriber=subscriber, orderField=orderField, orderSeq=orderSeq, stateFilter=stateFilter, pageNo=pageNo, pageSize=pageSize)
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 查询一辆车的所有预订信息，只查询未处理--0,已通过--1,进行中--3的订单
@order.route('/summary', methods=["GET"])
def summary():
    try:
        vehicleId = request.args.get("vehicleId")
        result = session.query(Order.id, Order.vehicleNo,
            func.date_format(Order.starttime, '%Y-%m-%d %H:%i').label("startTime"),
            func.date_format(Order.endtime, '%Y-%m-%d %H:%i').label("endTime"),
            User.name, User.telephone,
            Module.name.label("module")
        ).join(
            User,
            Order.subscriber == User.id,
            isouter = True
        ).join(
            Module,
            Order.module == Module.id,
            isouter = True
        ).filter(and_(
            Order.vehicleId == vehicleId,
            Order.state.in_((0, 1, 3))
        )).order_by(Order.starttime).all()
        session.close()
        data = generateEntries(["id", "vehicleNo", "startTime", "endTime", "name", "telephone", "module"], result)
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 查询一辆车的当日的预订信息，只查询未处理--0,已通过--1,进行中--3的订单
@order.route('/present', methods=["GET"])
def orderPresent():
    try:
        vehicleId = request.args.get("vehicleId")
        result = session.query(Order.id, Order.vehicleNo, 
            func.date_format(Order.starttime, '%Y-%m-%d %H:%i').label("startTime"),
            func.date_format(Order.endtime, '%Y-%m-%d %H:%i').label("endTime"),
            func.concat(func.date_format(Order.starttime, '%m-%d %H:%i'), ' - ', func.date_format(Order.endtime, '%m-%d %H:%i')).label("useTime"),
            User.name, User.username, User.telephone, Order.state, Process_state.name.label("stateName"),
            Module.name.label("module")
        ).join(
            User,
            Order.subscriber == User.id,
            isouter = True
        ).join(
            Module,
            Order.module == Module.id,
            isouter = True
        ).join(
            Process_state,
            Order.state == Process_state.state,
            isouter = True 
        ).filter(and_(
            Order.vehicleId == vehicleId,
            Order.state.in_((0, 1, 3)),
            not_(
                or_(
                    Order.endtime < func.concat(func.date_format(func.date_add(func.now(), text("INTERVAL 8 Hour")), '%Y-%m-%d'), " 00:00:00"),
                    Order.starttime > func.concat(func.date_format(func.date_add(func.now(), text("INTERVAL 8 Hour")), '%Y-%m-%d'), " 23:59:59")
                )
            )
        )).order_by(Order.starttime).all()
        session.close()
        data = generateEntries(["id", "vehicleNo", "startTime", "endTime", "useTime", "name", "username", "telephone", "state", "stateName", "module"], result)
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 预订车辆
@order.route('/add', methods=["POST"])
def add():
    try:
        subscriber = request.json.get("subscriber")
        subscribeNote = request.json.get("subscribeNote")
        module = request.json.get("module")
        vehicleId = request.json.get("vehicleId")
        vehicleNo = request.json.get("vehicleNo")
        project = request.json.get("vehicleProject")
        starttime = request.json.get("starttime")
        endtime = request.json.get("endtime")
        address = request.json.get("address")
        purpose = request.json.get("purpose")
        route = request.json.get("route")
        load = request.json.get("load")

        # 检查时间是否冲突
        total = session.query(func.count(Order.id)).filter(
            and_(
                Order.vehicleId == vehicleId,
                Order.state.in_((0, 1, 3)),
                not_(or_(Order.starttime >= endtime, Order.endtime <= starttime))
            )
        ).scalar()
        session.close()
        if total > 0:
            return jsonify({"code": 1, "msg": "您选择的用车时间与已有订单冲突，请选择其他时间!"})

        # 添加订单
        data = Order(subscriber=subscriber, subscribeNote=subscribeNote, module=module, vehicleId=vehicleId, vehicleNo=vehicleNo,
        project=project, starttime=starttime, endtime=endtime, address=address, purpose=purpose, route=route, load=load)
        session.add(data)
        session.flush()
        id = data.id
        session.commit()
        session.close()
        generate_message(id, OptType.order)
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})
    
# 审批订单
@order.route('/update', methods=["POST"])
def update():
    try:
        id = request.json.get("id")
        approver = request.json.get("approver")
        state = request.json.get("state")
        driver = request.json.get("driver", "")
        comment = request.json.get("comment", "")
        session.query(Order).filter(Order.id == id).update({
            "approver": approver,
            "state": int(state),
            "driver": driver,
            "comment": comment
        })
        session.commit()
        session.close()
        generate_message(id, OptType.approve)
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 取消订单
@order.route('/cancel', methods=["POST"])
def cancel():
    try:
        id = request.json.get("id")
        session.query(Order).filter(Order.id == id).update({"state": 5})
        session.commit()
        session.close()
        generate_message(id, OptType.cancel)
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 开始订单
@order.route('/start', methods=["POST"])
def start():
    try:
        id = request.json.get("id")
        session.query(Order).filter(Order.id == id).update({"state": 3})
        session.commit()
        session.close()
        generate_message(id, OptType.start)
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 结束订单
@order.route('/stop', methods=["POST"])
def stop():
    try:
        id = request.json.get("id")
        session.query(Order).filter(Order.id == id).update({"state": 4})
        session.commit()
        session.close()
        generate_message(id, OptType.stop)
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 删除订单
@order.route('/delete', methods=["POST", "DELETE"])
def delete():
    try:
        id = request.json.get("id")
        session.query(Order).filter(Order.id == id).delete()
        session.commit()
        session.close()
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})


# 短信状态回调
@order.route('/sms/callback', methods=["POST"])
def callback():
    try:
        mobile = request.json[0].get("mobile")
        user_receive_time = request.json[0].get("user_receive_time")
        report_status = request.json[0].get("report_status")
        errmsg = request.json[0].get("errmsg")
        description = request.json[0].get("description")
        sid = request.json[0].get("sid")
        print("\n短信下发状态：\n当前时间：{}, 手机号：{}, 接收时间：{}, 状态：{}, 错误消息：{}, 描述：{}, SID：{}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), mobile, user_receive_time, report_status, errmsg, description, sid), flush=True)
        return jsonify({"code": 0, "msg": "成功"})
    except Exception as e:
        print("短信下发状态错误：", str(e), flush=True)
        return jsonify({"code": 1, "msg": str(e)})

# 短信通知
def generate_message(orderId, type):
    try:
        orderInfo = getOrderInfo(orderId)
        if type == OptType.order:
            # 预订后通知所有的管理员需要审批订单
            phones = getAllAdminPhones()
            sendMessage(TemplateId="1680924", TemplateParamSet=[orderInfo["subscriber"], orderInfo["vehicleNo"], orderInfo["startTime"][5:], orderInfo["endTime"][5:]], PhoneNumberSet=phones, orderId=orderId)
        elif type == OptType.approve:
            # 通过审批通知订单预订人及关联的司机
            if orderInfo["state"] == 1:
                sendMessage(TemplateId="1680926", TemplateParamSet=[orderInfo["vehicleNo"], orderInfo["startTime"][5:], orderInfo["endTime"][5:], orderInfo["driver"]], PhoneNumberSet=[orderInfo["subscriberPhone"]], orderId=orderId)
                # 通知司机
                sendMessage(TemplateId="1680911", TemplateParamSet=[orderInfo["subscriber"], orderInfo["vehicleNo"], orderInfo["startTime"][5:], orderInfo["endTime"][5:], orderInfo["address"]], PhoneNumberSet=[orderInfo["driverPhone"]], orderId=orderId)
            # 被驳回通知预订人
            elif orderInfo["state"] == 2:
                sendMessage(TemplateId="1680929", TemplateParamSet=[orderInfo["vehicleNo"], orderInfo["startTime"][5:], orderInfo["endTime"][5:], orderInfo["approver"]], PhoneNumberSet=[orderInfo["subscriberPhone"]], orderId=orderId)
        elif type == OptType.cancel:
            # 取消订单，通知预订人及关联的司机（如果有司机）
            PhoneNumberSet = [orderInfo["subscriberPhone"]]
            if orderInfo["driverPhone"] is not None:
                PhoneNumberSet = [orderInfo["subscriberPhone"], orderInfo["driverPhone"]]
            sendMessage(TemplateId="1680917", TemplateParamSet=[orderInfo["subscriber"], orderInfo["vehicleNo"], orderInfo["startTime"][5:], orderInfo["endTime"][5:], orderInfo["address"]], PhoneNumberSet=PhoneNumberSet, orderId=orderId)
        elif type == OptType.start:
            # 开始订单，通知订单预订人
            sendMessage(TemplateId="1680936", TemplateParamSet=[orderInfo["vehicleNo"], orderInfo["startTime"][5:], orderInfo["endTime"][5:]], PhoneNumberSet=[orderInfo["subscriberPhone"]], orderId=orderId)
        elif type == OptType.stop:
            # 结束订单，通知订单预订人
            sendMessage(TemplateId="1680941", TemplateParamSet=[orderInfo["vehicleNo"], orderInfo["startTime"][5:], orderInfo["endTime"][5:]], PhoneNumberSet=[orderInfo["subscriberPhone"]], orderId=orderId)
    except Exception as e:
        print('生成短信消息出错：', str(e), flush=True)

def getOrderInfo(orderId):
    try:
        # 查询关联的预订人/司机及审批人的名称电话
        # 表别名，便于多次join同一个表
        S = aliased(User)
        T = aliased(User)
        U = aliased(User)
        result = session.query(
            Order.vehicleNo, Order.address, Order.purpose, Order.route, Order.state, Load.name.label("load"),
            func.date_format(Order.starttime, '%Y-%m-%d %H:%i').label("startTime"),
            func.date_format(Order.endtime, '%Y-%m-%d %H:%i').label("endTime"),
            S.name.label("subscriber"), func.concat('+86', S.telephone).label("subscriberPhone"),            
            T.name.label("approver"), func.concat('+86', T.telephone).label("approverPhone"),
            U.name.label("driver"), func.concat('+86', U.telephone).label("driverPhone")
        ).join(
            Load,
            Order.load == Load.id,
            isouter = True
        ).join(
            S,
            Order.subscriber == S.id,
            isouter = True
        ).join(
            T,
            Order.approver == T.id,
            isouter = True
        ).join(
            U,
            Order.driver == U.id,
            isouter = True
        ).filter(Order.id == orderId).all()
        session.close()
        
        orderInfo = {}
        if len(result):
            order = result[0]
            orderInfo = {
                "vehicleNo": order.vehicleNo,
                "address": order.address,
                "purpose": order.purpose,
                "route": order.route,
                "load": order.load,
                "startTime": order.startTime,
                "endTime": order.endTime,
                "state": order.state,
                "subscriber": order.subscriber,
                "subscriberPhone": order.subscriberPhone,
                "approver": order.approver,
                "approverPhone": order.approverPhone,
                "driver": order.driver,
                "driverPhone": order.driverPhone
            }
        return orderInfo
    except Exception as e:
        session.rollback()
        print('An exception occurred', str(e), flush=True)

def getAllAdminPhones():
    try:
        result = session.query(func.concat('+86', User.telephone)).filter(User.role == 1).all()
        phones = []
        pattern = '^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-79])|(?:5[0-35-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9[1589]))\d{8}$'
        for item in result:
            res = re.match(pattern, item[0])
            if res is not None:
                phones.append(item[0])
        return list(set(phones))
    except Exception as e:
        session.rollback()
        print('An exception occurred', str(e), flush=True)
