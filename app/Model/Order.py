from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import class_mapper
from exts import db

# 订单
class Order(db.Model):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    subscriber = Column(String(50), nullable=False, comment="预订人")
    subscribeNote = Column(String(100), comment="预订备注")
    module = Column(String(50), nullable=False, comment="所属模块")
    vehicleId = Column(Integer, nullable=False)
    vehicleNo = Column(String(50), nullable=False)
    project = Column(String(50), nullable=False, comment="所属项目")
    starttime = Column(DateTime, nullable=False, comment="预订的开始使用时间")
    endtime = Column(DateTime, nullable=False, comment="预订的结束使用时间")
    address = Column(String(100), nullable=False, comment="使用地点")
    purpose = Column(String(100), nullable=False, comment="约车目的")
    route = Column(String(100), nullable=False, comment="测试路线")
    load = Column(String(100), nullable=False, comment="带挂")
    updatetime = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    createtime = Column(DateTime, server_default=func.now(), nullable=False)    
    approver = Column(String(50), comment="审批人")
    driver = Column(String(50), comment="司机")
    state = Column(Integer, nullable=False, server_default="0", comment="0：未处理、1：已通过、2：已驳回、3：进行中、4：已结束、5：已取消")
    comment = Column(String(100), comment="审批意见")
    desc = Column(String(100), comment="描述")

    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) for col in class_mapper(obj.__class__).mapped_table.c) 
