import os
import git

def clone_and_get_branches(repoUrl):
    # 提取项目名
    repo_name = repoUrl.split(':')[-1].split('.git')[0]

    # 临时目录来克隆存储库，以项目名命名的子目录
    temp_clone_path = f'./temp/{repo_name}'

    # 检查存储库是否已经存在于临时目录中
    if not os.path.exists(temp_clone_path):
        # 存储库不存在，因此克隆它
        repo = git.Repo.clone_from(repoUrl, temp_clone_path)
    else:
        # 存储库已经存在，不需要再次克隆
        repo = git.Repo(temp_clone_path)
        # 执行git pull以拉取远程更新
        repo.remotes.origin.pull()

    # 获取远程分支列表
    remote_branches = repo.remote().refs

    # 提取分支名称（去除"origin/"前缀）
    branches = [branch.name.split('/', 1)[1] for branch in remote_branches if branch.name.startswith('origin/')]

     # 获取远程标签列表
    remote_tags = repo.tags
    # 提取标签名称
    tags = [tag.name for tag in remote_tags]

    # 返回分支和标签信息
    return {
        "branch": branches,
        "tag": tags
    }

# 使用示例
repoUrl = 'git@gitlab.zhito.com:wangshiyuan/vehicle-resource-server.git'
# repoUrl = 'git@gitlab.zhito.com:wangshiyuan/integration-front.git'
result = clone_and_get_branches(repoUrl)

# 打印远程分支名称
for branch in result["branch"]:
    print(branch)

for tag in result["tag"]:
    print(tag)




# import git, os

# # 远程Git存储库的URL
# remote_repo_url = 'git@gitlab.zhito.com:wangshiyuan/vehicle-resource-server.git'

# # 临时目录来克隆存储库
# temp_clone_path = './temp'

# # 检查存储库是否已经存在于临时目录中
# if not os.path.exists(temp_clone_path):
#     # 存储库不存在，因此克隆它
#     repo = git.Repo.clone_from(remote_repo_url, temp_clone_path)
# else:
#     # 存储库已经存在，不需要再次克隆
#     repo = git.Repo(temp_clone_path)
#     # 执行git pull以拉取远程更新
#     repo.remotes.origin.pull()

# # 获取远程分支列表
# remote_branches = repo.remote().refs

# # 提取分支名称（去除"origin/"前缀）
# branch_names = [branch.name.split('/', 1)[1] for branch in remote_branches if branch.name.startswith('origin/')]

# # 打印远程分支名称
# for branch_name in branch_names:
#     print(branch_name)
