from pyartifactory import Artifactory

url = "https://artifactory.zhito.com/artifactory"
username = "wangshiyuan"
api_key = "AKCp8nzqQaRKVZGfYHimkQh9FK3FHq2mkaaRtgJZhjaeYL71aUXU3RTJbFBjNTT9CqNoMTdru"

art = Artifactory(url=url, auth=(username, api_key), api_version=1)

# 查询一个目录下的所有文件
def getAllFiles(path):
    try:
        # 参数：path, 只查询当前目录下的文件，不进入深层目录
        arts = art.artifacts.list(path, recursive=False, list_folders=False)
        files = []
        for file in arts.files:
            files.append(file.uri)
        return files
    except Exception as e:
        print('An exception occurred in artifactory getAllFiles', str(e))
        
# 查询一个目录访问地址
def getUri(path):
    try:
        # 参数：path,
        arts = art.artifacts.info(path)
        return arts.uri
    except Exception as e:
        print('An exception occurred in artifactory getUri', str(e))