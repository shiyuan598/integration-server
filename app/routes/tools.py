# coding=utf8
# 工具接口，gitlab/jenkins/artifactory/confluence
from flask import Blueprint, request, jsonify
from common.gitlab_tool import getAllBranches, getAllTags, getBranchesTagsOfMultiProjects
from common.jenkins_tool import build
from common.artifactory_tool import getAllFiles, getUri
from Model import Api_process, App_process
from sqlalchemy import func, text, and_, or_, asc, desc
from exts import db
session = db.session

tools = Blueprint("tools", __name__)

# 拉取gitlab分支
@tools.route('/gitlab/branch', methods=["GET"])
def branch():
    try:
        project = request.args.get("project_name_with_namespace", "")
        data = getAllBranches(project)
        return jsonify({"code": 0, "data": {"branch": data}, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 拉取gitlab的Tag
@tools.route('/gitlab/tag', methods=["GET"])
def tag():
    try:
        project = request.args.get("project_name_with_namespace", "")
        data = getAllTags(project)
        return jsonify({"code": 0, "data": {"tag": data}, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 拉取gitlab多个项目的分支和Tag
@tools.route('/gitlab/multiple/branch_tag', methods=["GET"])
def branch_tag():
    try:
        projects = request.args.getlist("projects")
        data = getBranchesTagsOfMultiProjects(projects[0].split(","))
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 触发jenkins构建
@tools.route('/jenkins/build_job', methods=["POST"])
def build_job():
    try:
        process_type = int(request.json.get("process_type", 0))
        process_id = int(request.json.get("process_id", 0))
        job = request.json.get("job", "integration_test4")
        parameters = request.json.get("parameters")
        data = build(job, parameters)
        # 更新集成流程中的build_number, build_queue
        if process_type == 0:
            session.query(Api_process).filter(Api_process.id == process_id).update({           
                "build_number": data["build_number"],
                "build_queue": data["build_queue"],
                "state": 2 # 进行中
            })
            session.commit()
            session.close()
        else:
            if process_type == 1:
                session.query(App_process).filter(App_process.id == process_id).update({           
                    "build_number": data["build_number"],
                    "build_queue": data["build_queue"],
                    "state": 2 # 进行中
                })
                session.commit()
                session.close()
        
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 1, "msg": str(e)})

# 查询artifactory目录下的文件
@tools.route('/artifacts/files', methods=["GET"])
def artifacts_files():
    try:
        path = request.args.get("path", "GSL2/test/x86/1.0.0")
        data = getAllFiles(path)

        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})

# 查询artifactory目录下的文件
@tools.route('/artifacts/uri', methods=["GET"])
def artifacts_uri():
    try:
        path = request.args.get("path", "GSL2/test/x86/1.0.0")
        data = getUri(path)

        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})
