#!/bin/bash
rm -f schedule_task* ;
# 检查文件是否存在
if [ $? -eq 0 ]; then
  echo "文件已删除";
fi
nohup gunicorn -c gunicorn.conf app:app &
