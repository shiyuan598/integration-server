import gitlab
import time

# 参考：https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html
# https://gitlab.zhito.com/api/v4/projects REST Url 

url = "https://gitlab.zhito.com"
token = "7c5ohyqs1pzL6873cxjd"
gl = gitlab.Gitlab(url=url, private_token=token)

# 查询一个项目的所有分支
def getAllBranches(project_name_with_namespace):
    try:
        # 参数：project_name_with_namespace, 
        project = gl.projects.get(project_name_with_namespace)
        # 获取分支
        branches = []
        for branch in project.branches.list():
            branches.append(branch.name)
        return branches
    except Exception as e:
      print('An exception occurred in gitlab getAllBranches', str(e))
    
# 查询一个项目的所有Tag
def getAllTags(project_name_with_namespace):
    try:
        # 参数：project_name_with_namespace, 
        project = gl.projects.get(project_name_with_namespace)
        # 获取tag
        tags = []
        for tag in project.tags.list():
            tags.append(tag.name)
        return tags
    except Exception as e:
      print('An exception occurred in gitlab getAllTags', str(e))
    

# 一次查询多个项目的所有分支和tag
def getBranchesTagsOfMultiProjects2(project_names):
    try:
        start = time.clock()
        # 先列出所有项目
        projects = gl.projects.list(all=True, simple=True, search_namespaces=True)
        result = {}
        # 再逐个项目查看是否匹配
        for project in projects:
            name_with_namespace = project.name_with_namespace.replace(" ", "").lower()
            if name_with_namespace in project_names:
                # 获取分支
                branches = []
                for branch in project.branches.list():
                    branches.append(branch.name)
                # 获取tag
                tags = []
                for tag in project.tags.list():
                    tags.append(tag.name)
                result[project.name] = {
                    "branch": branches,
                    "tag": tags
                }
        end = time.clock()
        runTime = end - start
        print("\n method 1 run time:", runTime)
        return result
    except Exception as e:
      print('An exception occurred in gitlab getBranchesTagsOfMultiProjects', str(e))


# 一次查询多个项目的所有分支和tag
def getBranchesTagsOfMultiProjects(project_names):
    try:
        start = time.clock()
        result = {}
        # 逐个项目查询
        for project_name_with_namespace in project_names:
            project = gl.projects.get(project_name_with_namespace)
            # 获取分支
            branches = []
            for branch in project.branches.list():
                branches.append(branch.name)
            # 获取tag
            tags = []
            for tag in project.tags.list():
                tags.append(tag.name)
            result[project.name] = {
                "branch": branches,
                "tag": tags
            }
        end = time.clock()
        runTime = end - start
        print("\n method 2 run time:", runTime)
        return result
    except Exception as e:
      print('An exception occurred in gitlab getBranchesTagsOfMultiProjects', str(e))
