import gitlab

# 参考：https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html
# https://gitlab.zhito.com/api/v4/projects REST Url 

url = "https://gitlab.zhito.com"
token = "7c5ohyqs1pzL6873cxjd"
gl = gitlab.Gitlab(url=url, private_token=token)

# 列出所有项目，使用namespace搜索
projects = gl.projects.list(all=True, simple=True, search_namespaces=True, search="wangshiyuan/vehicle-resource")
for project in projects:
    print("Project: ", project.name)
    # 获取分支
    for branch in project.branches.list():
        print("\tBranch: ", branch.name)
    # print(project, "\n\n")
# 获取标签
print("\tTag: ", projects[0].tags.list()[0].name)

# 获取单个项目， 参数：project_name_with_namespace, 
project = gl.projects.get("wangshiyuan/vehicle-resource")
print("single project:\n", project, "\n")
