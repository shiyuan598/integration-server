from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.orm import class_mapper
from exts import db

# 待办
class Todo(db.Model):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(Integer, nullable=False, server_default="1", comment="类型：0-接口集成，1-应用集成")
    process_id = Column(Integer, nullable=False, comment="流程Id")
    version = Column(String(50), nullable=False, comment="版本号")
    module = Column(String(50), nullable=False, comment="模块")
    creator = Column(String(50), nullable=False, comment="创建者")
    handler = Column(String(50), nullable=False, comment="处理者")
    desc = Column(String(100), comment="描述")
    state = Column(Integer, nullable=False, server_default="0", comment="状态：0-未处理，1-已处理")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    create_time = Column(DateTime, server_default=func.now(), nullable=False)
    
    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) for col in class_mapper(obj.__class__).mapped_table.c)
