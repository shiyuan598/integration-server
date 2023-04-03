#### 说明
软件集成平台后端服务
##### 开发
1.安装依赖
```bash
pip3 install -r requirements.txt --index https://pypi.tuna.tsinghua.edu.cn/simple
```
设置镜像源：--index https://pypi.tuna.tsinghua.edu.cn/simple
安装短信SDK：
pip3 install -i https://mirrors.tencent.com/pypi/simple/ --upgrade tencentcloud-sdk-python tencentcloud-sdk-python-sms

参考：腾讯云短信服务SDK[地址(https://cloud.tencent.com/document/product/382)]
腾讯云账户管理[地址(https://console.cloud.tencent.com/smsv2)]

2.启动
```bash
python3 app.py
```

##### 文档
1.python-gitlab: https://python-gitlab.readthedocs.io/en/stable/gl_objects/branches.html
2.python-jenkins: https://python-jenkins.readthedocs.io/en/latest/api.html#jenkins.Jenkins.get_queue_item
3.confluence: https://docs.atlassian.com/ConfluenceServer/rest/7.8.1/#api/content-createContent


##### rest url
https://jira.zhito.com:8080/rest/api/2/issue/GSL3P-2986
https://confluence.zhito.com:8090/rest/api/space/JSZSZX
https://gitlab.zhito.com/api/v4/projects
https://artifactory.zhito.com/artifactory/api/repositories
https://jenkins.zhito.com/api/