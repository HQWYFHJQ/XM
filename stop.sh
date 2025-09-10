#!/bin/bash

# 校园跳蚤市场智能推荐平台 - 停止脚本

echo "=========================================="
echo "停止校园跳蚤市场智能推荐平台"
echo "=========================================="

# 停止主应用
if [ -f "main.pid" ]; then
    MAIN_PID=$(cat main.pid)
    if ps -p $MAIN_PID > /dev/null; then
        echo "停止主应用 (PID: $MAIN_PID)..."
        kill $MAIN_PID
        rm -f main.pid
        echo "主应用已停止"
    else
        echo "主应用进程不存在"
        rm -f main.pid
    fi
else
    echo "未找到主应用PID文件"
fi

# 停止管理后台
if [ -f "admin.pid" ]; then
    ADMIN_PID=$(cat admin.pid)
    if ps -p $ADMIN_PID > /dev/null; then
        echo "停止管理后台 (PID: $ADMIN_PID)..."
        kill $ADMIN_PID
        rm -f admin.pid
        echo "管理后台已停止"
    else
        echo "管理后台进程不存在"
        rm -f admin.pid
    fi
else
    echo "未找到管理后台PID文件"
fi

# 强制停止所有相关进程
echo "检查并停止所有相关进程..."
pkill -f "python app.py"
pkill -f "flask run"

echo "=========================================="
echo "所有服务已停止"
echo "=========================================="
