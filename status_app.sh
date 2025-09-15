#!/bin/bash

echo "=== 校园跳蚤市场应用状态检查 ==="
echo "时间: $(date)"
echo ""

# 检查PID文件
if [ -f "logs/app.pid" ]; then
    APP_PID=$(cat logs/app.pid)
    echo "PID文件存在: logs/app.pid"
    echo "记录PID: $APP_PID"
else
    echo "PID文件不存在: logs/app.pid"
    APP_PID=""
fi

echo ""

# 检查进程状态
echo "进程状态:"
if [ -n "$APP_PID" ] && ps -p $APP_PID > /dev/null 2>&1; then
    echo "✓ 主进程运行中 (PID: $APP_PID)"
    ps -p $APP_PID -o pid,ppid,cmd
else
    echo "✗ 主进程未运行"
fi

echo ""

# 检查所有gunicorn进程
echo "所有Gunicorn进程:"
GUNICORN_PIDS=$(ps aux | grep gunicorn | grep -v grep | awk '{print $2}')
if [ -n "$GUNICORN_PIDS" ]; then
    for pid in $GUNICORN_PIDS; do
        echo "  PID $pid: $(ps -p $pid -o cmd --no-headers)"
    done
else
    echo "  无Gunicorn进程运行"
fi

echo ""

# 检查端口状态
echo "端口状态:"
if netstat -tlnp | grep :8000 > /dev/null; then
    echo "✓ 端口8000正在监听"
    netstat -tlnp | grep :8000
else
    echo "✗ 端口8000未监听"
fi

echo ""

# 检查应用响应
echo "应用响应测试:"
if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo "✓ 应用响应正常"
else
    echo "✗ 应用无响应"
fi

echo ""

# 检查日志
echo "最近日志 (最后10行):"
if [ -f "logs/arms_daemon.log" ]; then
    tail -10 logs/arms_daemon.log
else
    echo "  日志文件不存在"
fi
