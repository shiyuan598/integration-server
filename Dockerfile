FROM dp-harbor.zhito.com/dp-aishop/digital_platform/fe/integration-dev:dev

WORKDIR /app

COPY app /app

# 安装 Python 依赖
RUN pip3 install -r /app/requirements.txt --index https://pypi.tuna.tsinghua.edu.cn/simple

# 执行 Flask 数据库迁移
RUN python3.10 -m flask db upgrade

# 启动 Gunicorn 服务器
CMD ["./start_gunicorn.sh"]
