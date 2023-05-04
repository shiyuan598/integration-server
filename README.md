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
腾讯云密钥管理[地址(https://console.cloud.tencent.com/cam/capi)]

2.启动
开发环境
```bash
python3 app.py
```
生产环境使用gunicorn
```bash
nohup gunicorn -c gunicorn.conf app:app > log_info.log 0<&1 2>&1 &
```

3.迁移
3.1安装
```
pip3 install flask-migrate --index https://pypi.tuna.tsinghua.edu.cn/simple
```
3.2初始化Migrate
from flask_migrate import Migrate
...
# 数据迁移
migrate = Migrate(app, db)

3.3初始化数据库
```bash
flask db init 
```
或 python -m flask db init


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

#### 测试数据：
```sql
INSERT INTO integration.module (project,name,git,owner,`desc`) VALUES
	 ('1','drivers','git@gitlab.zhito.com:drivers/drivers.git','1',NULL),
	 ('1','zloc','git@gitlab.zhito.com:zloc/zloc.git','2',NULL),
	 ('1','zmap','git@gitlab.zhito.com:zlam/zmap.git','3',NULL),
	 ('1','perception_camera_obs','git@gitlab.zhito.com:ai/perception_camera_obs.git','4',NULL),
	 ('1','perception_radar','git@gitlab.zhito.com:ai/perception_radar.git','5',NULL),
	 ('1','perception_lidar','git@gitlab.zhito.com:ai/perception_lidar.git','6',NULL),
	 ('1','perception_fusion','git@gitlab.zhito.com:ai/perception_fusion.git','7',NULL),
	 ('1','perception_camera','git@gitlab.zhito.com:ai/perception_camera.git','8',NULL),
	 ('1','prediction','git@gitlab.zhito.com:prediction/prediction.git','9',NULL),
	 ('1','routing','git@gitlab.zhito.com:routing/routing.git','10',NULL);
	
INSERT INTO integration.module (project,name,git,owner,`desc`) VALUES
	 ('1','control','git@gitlab.zhito.com:control/control.git','11',NULL);
```