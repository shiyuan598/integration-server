import json
from atlassian import Confluence

url = "https://confluence.zhito.com:8090"
username = "wangshiyuan"
password = "zhito26@#"
space="ITD"
parent_page_id=56111727
parent_page_id_app=56114852
parent_page_id_api=56114855

confluence = Confluence(url=url, username=username, password=password)


# 创建页面
def create_page(title, content="", space="ITD", parent_page_id=56111727):
    try:   
        new_page = confluence.create_page(space=space,
                                          title=title,
                                          body=content,
                                          parent_id=parent_page_id)
        return {"id": new_page["id"], "url": url + new_page["_links"]["webui"]}
    except Exception as e:
        print('An exception occurred in create_page', str(e), flush=True)

# 根据title获取page_id,如果没有就创建
def query_or_create_page_by_title(title, parent_page_id, space="ITD"):
    page = confluence.get_page_by_title(space=space,
                                    title=title,
                                    expand='body.storage')
    if page is None:
        return create_page(title=title, space=space, parent_page_id=parent_page_id)["id"]

    return page["id"]

# 获取项目级的页面id
def get_page_by_title(title, type="App_process"):
    if type == "App_process":
        return query_or_create_page_by_title(title=title, space=space, parent_page_id=parent_page_id_app)
    if type == "Api_process":
        return query_or_create_page_by_title(title=title, space=space, parent_page_id=parent_page_id_api)


# confluence集成平台构建日志
# 触发条件：系统级别的构建会生成日志
# 触发时间：查询到结果时触发写入confluence

# 目录结构（命名规范）：
# 一级目录：应用集成 / 接口集成
# 二级目录：项目名称【应用/集成】，注：增加标签避免confluence同一空间下title重复的问题
# 三级目录：版本号【日期】【应用/集成】，如：V0.1.1【2023-04-19】【应用】
# 内容模板：
# 项目：GSL4_X86

# 版本号：v0.1.1

# 集成类型：接口集成

# 描述：xxxx

# 创建人：admin

# 时间：2023-04-19 14:29

# 结果：成功 / 失败

# Jenkins: https://jenkins.zhito.com/job/integration_test4/72/

# Artifacts: https://artifactory.zhito.com/ui/native/GSL4/cicd/X86/

# 模块配置信息：{project: "GSL4_X86", version: "V1.2.1", modules: { ... }}
