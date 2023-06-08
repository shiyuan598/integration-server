import json
from atlassian import Confluence

url = "https://confluence.zhito.com:8090"
username = "wangshiyuan"
password = "zhito26@#"
space = "ITD"
parent_page_id = 56111727
parent_page_id_app = 56114852
parent_page_id_api = 56114855

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
    try:
        page = confluence.get_page_by_title(space=space,
                                            title=title,
                                            expand='body.storage')
        if page is None:
            return create_page(title=title,
                               space=space,
                               parent_page_id=parent_page_id)["id"]

        return page["id"]
    except Exception as e:
        print('An exception occurred in query_or_create_page_by_title',
              str(e),
              flush=True)


# 获取或创建项目级的页面id
def get_or_create_page_by_title(title, type="App_process"):
    try:
        if type == "App_process":
            return query_or_create_page_by_title(
                title=title, space=space, parent_page_id=parent_page_id_app)
        if type == "Api_process":
            return query_or_create_page_by_title(
                title=title, space=space, parent_page_id=parent_page_id_api)
    except Exception as e:
        print('An exception occurred in get_or_create_page_by_title', str(e), flush=True)


# # 获取页面
# def get_page_by_title(title):
#     try:
#         return confluence.get_page_by_title(space=space, title=title, expand='body.storage')
#     except Exception as e:
#         print('An exception occurred in get_page_by_title', str(e), flush=True)

# 将测试结果链接追加到confluence页面中
def append_page_by_id(id, content):
    try:
        result = None
        if id is not None:
            result = confluence.append_page(page_id=id, append_body=content)

        return result
    except Exception as e:
        print('An exception occurred in append_page_by_id', str(e), flush=True)
