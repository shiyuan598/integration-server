# coding=utf8
# 工具接口，gitlab/jenkins/artifactory/confluence
from flask import Blueprint, request, jsonify
from common.gitlab_tool import getAllBranches, getAllTags, getBranchesTagsOfMultiProjects, getBranchesTagsOfMultiProjects2
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

@tool.route('/gitlab/multiple/branch_tag2', methods=["GET"])
def branch_tag2():
    try:
        projects = request.args.getlist("projects")
        data = getBranchesTagsOfMultiProjects2(projects[0].split(","))
        return jsonify({"code": 0, "data": data, "msg": "成功"})
    except Exception as e:
        return jsonify({"code": 1, "msg": str(e)})