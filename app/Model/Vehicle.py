from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, BIGINT, Float, func
from sqlalchemy.orm import class_mapper
from exts import db

# 车辆
class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vehicleNo = Column(String(50), nullable=False)
    project = Column(String(50), nullable=False, comment="所属项目")
    place = Column(String(100), comment="地点")
    state = Column(Integer, nullable=False, server_default="1",
                   comment="状态  0:不可用;1:可用")
    createtime = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    version = Column(Text, comment="版本信息")
    timestamp = Column(BIGINT, comment="版本更新时间")
    lon = Column(Float, comment="经度")
    lat = Column(Float, comment="纬度")
    desc = Column(String(100), comment="描述")
    
    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) for col in class_mapper(obj.__class__).mapped_table.c)
