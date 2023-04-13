import json
from atlassian import Confluence

url = "https://confluence.zhito.com:8090"
username = "wangshiyuan"
password = "zhito26@#"
space="ITD"
parent_page_id=56111727

confluence = Confluence(url=url, username=username, password=password)


# 创建页面
def create_page(title, data, space="ITD", parent_page_id=56111727):
    try:
        config = {
            "project": "GSL4_X86",
            "version": "1.1",
            "build_type": "Debug",
            "base": {
                "message_group": {
                    "url": "git@gitlab.zhito.com:ai/message_group.git",
                    "version": "feature/zhito_l4_cicd"
                },
                "common": {
                    "url": "git@gitlab.zhito.com:ai/zhito_common.git",
                    "version": "feature/zhito_l4_cicd"
                },
                "map": {
                    "url": "git@gitlab.zhito.com:ai/map_module.git",
                    "version": "feature/zhito_l4_cicd"
                },
                "zlam_common": {
                    "url": "git@gitlab.zhito.com:zlam/zlam_common.git",
                    "version": "feature/zhito_l4_cicd"
                },
                "perception_common": {
                    "url": "git@gitlab.zhito.com:ai/perception_common.git",
                    "version": "feature/zhito_l4_cicd"
                }
            },
            "modules": {
                "drivers": {
                    "url": "git@gitlab.zhito.com:drivers/drivers.git",
                    "version": "feature/zhito_l4_cicd"
                }
            }
        }

        title = "page6"
        pre = '<p class="auto-cursor-target"><br /></p><ac:structured-macro ac:name="code" ac:schema-version="1" ac:macro-id="06dba324-f02c-4410-8fa5-190d5d7f8bcd"><ac:plain-text-body><![CDATA['
        suf = '}]]></ac:plain-text-body></ac:structured-macro><p><br /></p>'
        content = pre + json.dumps(config, indent=4) + suf

        new_page = confluence.create_page(space=space,
                                          title=title,
                                          body=content,
                                          parent_id=parent_page_id)
        print("\n\nnew_page:", new_page)
        return url + new_page["_links"]["webui"]
    except Exception as e:
        print('An exception occurred in create_page', str(e), flush=True)
