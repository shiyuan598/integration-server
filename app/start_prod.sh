#!/bin/bash
# 设置环境变量
export FLASK_ENV=production

# 1.执行 Flask 数据库迁移
python3.10 -m flask db upgrade
# 等待上一步完成
wait

# 2.删除任务锁文件
rm -f schedule_task* ;
# 检查文件是否存在
if [ $? -eq 0 ]; then
  echo "文件已删除";
fi
# 等待上一步完成
wait

# 3.运行程序
python3.10 -m gunicorn -c gunicorn.conf app:app