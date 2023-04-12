from sqlalchemy import Column, Integer, String, DateTime, Text, func, UniqueConstraint
from sqlalchemy.orm import class_mapper
from exts import db

# 应用集成流程
class App_process(db.Model):
    __tablename__ = 'app_process'
    id = Column(Integer, primary_key=True, autoincrement=True)
    project = Column(Integer, nullable=False, comment="项目")
    build_type = Column(String(50), nullable=False, comment="构建类型")
    version = Column(String(50), nullable=False, comment="版本号")
    api_version = Column(String(50), comment="接口版本号")
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    create_time = Column(DateTime, server_default=func.now(), nullable=False)
    creator = Column(Integer, nullable=False, comment="创建者")
    type = Column(Integer, nullable=False, server_default="1", comment="类型：0-系统集成，1-开发集成")
    modules = Column(Text, nullable=False, comment="模块信息")
    job_name = Column(Text, nullable=False, comment="jenkins构建任务的名称")
    build_queue = Column(Integer, comment="jenkins构建任务的queue_id")
    build_number = Column(Integer, comment="jenkins构建任务的序号")
    jenkins_url = Column(String(100), comment="jenkins构建的url")
    artifactory_url = Column(String(100), comment="artifactory的url")
    state = Column(Integer, nullable=False, server_default="0", comment="0：准备中、1：已就绪、2：进行中、3：成功、 4：失败、5：已取消")
    desc = Column(String(100), comment="描述")
    __table_args__ = (UniqueConstraint('version', 'creator', 'project', name='uq_version_creator_project'),) # 同一个用户在同一个项目下创建的版本号不能重复

    def as_dict(obj):
        return dict((col.name, getattr(obj, col.name)) for col in class_mapper(obj.__class__).mapped_table.c)
