1.修改配置
config/setting.py 中数据库的配置
gun.conf 中IP端口配置

2.拷贝文件到服务器
sudo scp -r build/ zhito@172.16.18.223:/home/zhito/integration/server

3.启动命令
nohup gunicorn -c gunicorn.conf app:app > log_info.log 0<&1 2>&1 &