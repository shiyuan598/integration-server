from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.orm import class_mapper
from exts import db

# 订单
class Api_process(db.Model):
    __tablename__ = 'api_process'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project = Column(String(50), nullable=False, comment="项目")
    build_type = Column(String(50), nullable=False, comment="构建类型")
    version = Column(String(50), nullable=False, comment="版本号")
    release_note = Column(String(50), nullable=False, comment="release note")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    create_time = Column(DateTime, server_default=func.now(), nullable=False)
    creator = Column(String(50), nullable=False, comment="创建者")
    modules = Column(Text, nullable=False, comment="模块信息")
    state = Column(Integer, nullable=False, server_default="0", comment="0：准备中、1：已就绪、2：进行中、3：成功、 4：失败、5：已取消")
    desc = Column(String(100), comment="描述")

    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) for col in class_mapper(obj.__class__).mapped_table.c) 
