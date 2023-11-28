import gitlab
from config.setting import GITLAB

# 参考：https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html
# https://gitlab.zhito.com/api/v4/projects REST Url 

url, token = GITLAB["url"], GITLAB["token"]
gl = gitlab.Gitlab(url=url, private_token=token)

# 查询一个项目的所有分支
def getAllBranches(repoUrl):
    try:
        project_name_with_namespace = repoUrl.split(':')[-1].split('.git')[0]
        # 参数：project_name_with_namespace, 
        project = gl.projects.get(project_name_with_namespace)
        # 获取分支
        branches = []
        for branch in project.branches.list(all=True):
            branches.append(branch.name)
        return branches
    except Exception as e:
        print('An exception occurred in gitlab getAllBranches', str(e), flush=True)
        return []

# 查询一个项目的所有Tag
def getAllTags(repoUrl):
    try:
        project_name_with_namespace = repoUrl.split(':')[-1].split('.git')[0]
        # 参数：project_name_with_namespace, 
        project = gl.projects.get(project_name_with_namespace)
        # 获取tag
        tags = []
        for tag in project.tags.list(all=True):
            tags.append(tag.name)
        return tags
    except Exception as e:
        print('An exception occurred in gitlab getAllTags', str(e), flush=True)
        return []

# 一次查询多个项目的所有分支和tag
def multiGetBranchesTags(repoUrls):
    try:
        result = {}
        # 逐个项目查询
        for repoUrl in repoUrls:
            project_name_with_namespace = repoUrl.split(':')[-1].split('.git')[0]
            project = gl.projects.get(project_name_with_namespace)
            # 获取分支
            branches = []

            for branch in project.branches.list(all=True):
                branches.append(branch.name)
            # 获取tag
            tags = []
            for tag in project.tags.list(all=True):
                tags.append(tag.name)
            result[repoUrl] = {
                "branch": branches,
                "tag": tags
            }
        return result
    except Exception as e:
        print('An exception occurred in gitlab multiGetBranchesTags', str(e), flush=True)
        return {"branches": [], "tags": []}

# 查询特定分支的commitId
def getCommitId(project_name_with_namespace, branch_name):
    try:
        commit = ""

        # 获取需要查询的项目
        project = gl.projects.get(project_name_with_namespace)
        
        try:
            # 获取指定分支
            branch = project.branches.get(branch_name)
            commit = branch.commit["id"]
        except gitlab.exceptions.GitlabGetError as e:
            # 分支不存在，就尝试从tag中查找
            if e.response_code == 404:
                tag = project.tags.get(branch_name)
                commit = tag.commit["id"]
        return commit
    except Exception as e:
        print('An exception occurred in gitlab getCommitId', str(e), flush=True)
        return ""