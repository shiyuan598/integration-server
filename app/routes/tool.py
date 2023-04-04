# coding=utf8
# 工具接口，gitlab/jenkins/artifactory/confluence
from flask import Blueprint, request, jsonify
from common.gitlab_tool import getAllBranches, getAllTags, getBranchesTagsOfMultiProjects, getBranchesTagsOfMultiProjects2
from common.jenkins_tool import build, get_build_info

from Model import Api_process, App_process
from sqlalchemy import func, text, and_, or_, asc, desc
from exts import db
session = db.session

tool = Blueprint("tool", __name__)

# 拉取gitlab分支
@tool.route('/gitlab/branch', methods=["GET"])
def branch():
    try:
        project = request.args.get("project_name_with_namespace", "")
        data = getAllBranches(project)
        return jsonify({"code": 0, "data": {"branch": data}, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 拉取gitlab的Tag
@tool.route('/gitlab/tag', methods=["GET"])
def tag():
    try:
        project = request.args.get("project_name_with_namespace", "")
        data = getAllTags(project)
        return jsonify({"code": 0, "data": {"tag": data}, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 拉取gitlab多个项目的分支和Tag
@tool.route('/gitlab/multiple/branch_tag', methods=["GET"])
def branch_tag():
    try:
        projects = request.args.getlist("projects")
        data = getBranchesTagsOfMultiProjects(projects[0].split(","))
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 拉取gitlab多个项目的分支和Tag，一次性查询所有项目，再逐个比对，效率低
@tool.route('/gitlab/multiple/branch_tag2', methods=["GET"])
def branch_tag2():
    try:
        projects = request.args.getlist("projects")
        data = getBranchesTagsOfMultiProjects2(projects[0].split(","))
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 触发jenkins构建
@tool.route('/jenkins/build_job', methods=["GET", "POST"])
def build_job():
    try:
        # process_type = request.json.get("process_type", "0")
        # process_id = request.json.get("process_id", "0")
        # job = request.json.get("job", "integration_test4")
        # parameters = request.json.get("parameter", {"username": "yhifif", "date": "2023-04-20"})
        # data = build(job, parameters)
        data = build("integration_test4", {"username": "yhifif", "date": "2023-04-20"})
        # 更新集成流程中的build_number, build_queue
        # if process_type == "0":
        #     session.query(Api_process).filter(Api_process.id == process_id).update({           
        #         "build_number": data["build_number"],
        #         "build_queue": data["build_queue"],
        #         "state": 2 # 进行中
        #     })
        # else:
        #     if process_type == "1":
        #         session.query(App_process).filter(App_process.id == process_id).update({           
        #             "build_number": data["build_number"],
        #             "build_queue": data["build_queue"],
        #             "state": 2 # 进行中
        #         })
        # session.commit()
        # session.close()
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        # session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 查询jenkins构建任务的状态
@tool.route('/jenkins/build_info', methods=["GET", "POST"])
def build_info():
    try:
        # process_type = request.json.get("process_type", "0")
        # process_id = request.json.get("process_id", "0")
        # job = request.json.get("job", "integration_test4")
        # build_number = request.json.get("build_number", "26")
        # build_queue = request.json.get("build_queue", "18052")
        # data = get_build_info(job, build_number, build_queue)
        data = get_build_info("integration_test4", 37, 18091)

        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

#  办法：
#  1.build前假定该次build_number = nextBuildNumber, 记录queueId
#  2.查询build_info前, 先查询lastbuildNumber, 
#    2.1 lastBuildNumber < build_number, 直接返回, 认为build进行中, 需要等一会再查询
#    2.2 lastBuildNumber >= build_number时, 查询buildInfo
#    2.3 比较buildInfo.queueId和记录的queueId
#    2.4 如果相等,返回buildInfo
#    2.5 如果不相等, build_number = build_number + 1, 重复执行步骤2
#  tips:build之后不能立即查询到build_number,等待时间不确定
