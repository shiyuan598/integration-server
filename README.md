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
开发环境
```bash
python3 app.py
```
生产环境使用gunicorn
```bash
nohup gunicorn -c gunicorn.conf app:app > log_info.log 0<&1 2>&1 &
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


#### 测试api
获取单个git项目的分支和tag
http://127.0.0.1:9002/api/gitlab/tag?project_name_with_namespace=ai/perception_camera

一次性获取多个git项目的分支和tag
http://127.0.0.1:9002/api/gitlab/multiple/branch_tag2?projects=ai/perception_camera,ai/planning_lattice

