#!/bin/bash

# 找到并停止旧的后端进程
echo "停止旧的后端进程..."
OLD_PID=$(ps aux | grep "uvicorn.*8000" | grep -v grep | awk '{print $2}')
if [ ! -z "$OLD_PID" ]; then
    kill $OLD_PID 2>/dev/null
    sleep 2
    echo "已停止PID: $OLD_PID"
else
    echo "没有运行中的后端进程"
fi

# 启动新的后端
echo "启动后端..."
cd /workspaces/geyan-suidong-
nohup python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &
NEW_PID=$!
echo "后端已启动，PID: $NEW_PID"
echo "日志文件: logs/backend.log"

# 等待服务启动
sleep 3

# 测试健康检查
echo "测试健康检查..."
curl -s http://localhost:8000/health | python -m json.tool 2>/dev/null || echo "健康检查失败"
