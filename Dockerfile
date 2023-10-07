FROM dp-harbor.zhito.com/vehicle/integration-server:20230915

# 安装 Git
RUN apt-get update && apt-get install -y git

WORKDIR /app

COPY app /app/server

WORKDIR /app/server

# 安装 Python 依赖
RUN python3.10 -m pip install -r requirements.txt --index https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 9021

# 启动 Gunicorn 服务器
CMD ["./start_prod.sh"]
