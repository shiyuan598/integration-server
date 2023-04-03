from pyartifactory import Artifactory

url = "https://artifactory.zhito.com/artifactory"
username = "wangshiyuan"
api_key = "AKCp8nzqQaRKVZGfYHimkQh9FK3FHq2mkaaRtgJZhjaeYL71aUXU3RTJbFBjNTT9CqNoMTdru"

art = Artifactory(url=url, auth=(username, api_key), api_version=1)

# print(art)
# repo = art.repositories.get_repo("GSL2")
# print(repo)
arts = art.artifacts.list("GSL2/test/x86/1.0.0")
print(arts, type(arts), arts.uri, arts.files)
for file in arts.files:
    print("file uri:", file.uri)
# users=art.groups.list()

# repo = repositories.get("GSL2")
# print(repo)


