FROM ubuntu:18.04

#  RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list

RUN apt-get update -y && \ 
apt-get install -y python3-pip python3-dev vim net-tools

WORKDIR /app

COPY app /app

# 安装 Python 依赖
RUN pip3 install -r /app/requirements.txt --index https://pypi.tuna.tsinghua.edu.cn/simple

# 执行 Flask 数据库迁移
RUN python3.10 -m flask db upgrade

# 启动 Gunicorn 服务器
CMD ["./start_gunicorn.sh"]
