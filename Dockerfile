FROM dp-harbor.zhito.com/vehicle/integration-server:20230915

WORKDIR /app

COPY app /app/server

WORKDIR /app/server
# 安装 Python 依赖
RUN python3.10 -m pip install -r requirements.txt --index https://pypi.tuna.tsinghua.edu.cn/simple

# 执行 Flask 数据库迁移
RUN python3.10 -m flask db upgrade

# 启动 Gunicorn 服务器
CMD ["./start_dev.sh"]
