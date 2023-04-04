from sqlalchemy import Column, Integer, String, DateTime, func, UniqueConstraint
from sqlalchemy.orm import class_mapper
from exts import db

# 订单
class Module(db.Model):
    __tablename__ = 'module'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project = Column(String(50), nullable=False, comment="项目")
    name = Column(String(50), nullable=False, comment="名称")
    git = Column(String(50), nullable=False, comment="git")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    create_time = Column(DateTime, server_default=func.now(), nullable=False)
    owner = Column(String(50), nullable=False, comment="负责人")
    desc = Column(String(100), comment="描述")
    __table_args__ = (UniqueConstraint('name', 'project', name='uq_name_project'),) # 同一个项目下的模块名不能重复

    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) for col in class_mapper(obj.__class__).mapped_table.c) 
