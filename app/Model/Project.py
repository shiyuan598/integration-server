from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.orm import class_mapper
from exts import db

# 项目
class Project(db.Model):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="名称", unique=True)
    platform = Column(String(50), nullable=False, comment="平台")
    job_name = Column(Text, nullable=False, comment="jenkins构建任务的名称")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    create_time = Column(DateTime, server_default=func.now(), nullable=False)
    owner = Column(Integer, nullable=False, comment="负责人")
    desc = Column(String(100), comment="描述")

    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) for col in class_mapper(obj.__class__).mapped_table.c) 
