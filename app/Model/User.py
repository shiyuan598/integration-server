from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import class_mapper
from exts import db

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="名称")
    username = Column(String(50), nullable=False, comment="登录名")
    password = Column(String(50), nullable=False, comment="密码")
    telephone = Column(String(50), nullable=False, comment="电话号码")
    role = Column(Integer, nullable=False, comment="1: 管理员, 2:司机,3:普通用户")
    token = Column(String(100), comment="")
    desc = Column(String(100), comment="")

    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) for col in class_mapper(obj.__class__).mapped_table.c)
