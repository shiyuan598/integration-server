import git, os

# 查询一个项目的所有分支
def getAllBranches(repoUrl):
    try:
        result = get_branches_tags(repoUrl)
        return result["branch"]
    except Exception as e:
        print('An exception occurred in gitlab getAllBranches', str(e), flush=True)
        return []
    
# 查询一个项目的所有Tag
def getAllTags(repoUrl):
    try:
        result = get_branches_tags(repoUrl)
        return result["tag"]
    except Exception as e:
        print('An exception occurred in gitlab getAllTags', str(e), flush=True)
        return []

# 一次查询多个项目的所有分支和tag
def multiGetBranchesTags(repo_urls):
    try:
        result = {}
        # 逐个项目查询
        for repo_url in repo_urls:
            result[repo_url] = get_branches_tags(repo_url)
        return result
    except Exception as e:
        print('An exception occurred in gitlab multiGetBranchesTags', str(e), flush=True)
        return {"branches": [], "tags": []}

def get_branches_tags(repoUrl):
    try:
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
    except Exception as e:
            print('An exception occurred in gitlab get_branches_tags', repoUrl, str(e), flush=True)
            return None