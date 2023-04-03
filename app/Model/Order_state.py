from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import class_mapper
from exts import db

# 订单状态
class Order_state(db.Model):
    __tablename__ = 'order_state'
    id = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(Integer, nullable=False)
    name = Column(String(50))
    desc = Column(String(50))

    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) for col in class_mapper(obj.__class__).mapped_table.c)
