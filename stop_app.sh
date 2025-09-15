#!/bin/bash

echo "=== 停止校园跳蚤市场应用 ==="
echo "时间: $(date)"
echo ""

# 检查PID文件
if [ -f "logs/app.pid" ]; then
    APP_PID=$(cat logs/app.pid)
    echo "从PID文件读取: $APP_PID"
    
    if ps -p $APP_PID > /dev/null 2>&1; then
        echo "停止主进程 (PID: $APP_PID)..."
        kill $APP_PID
        sleep 2
        
        if ps -p $APP_PID > /dev/null 2>&1; then
            echo "强制停止进程..."
            kill -9 $APP_PID
            sleep 1
        fi
        
        if ps -p $APP_PID > /dev/null 2>&1; then
            echo "✗ 无法停止进程 $APP_PID"
        else
            echo "✓ 主进程已停止"
        fi
    else
        echo "主进程未运行"
    fi
else
    echo "PID文件不存在"
fi

echo ""

# 停止所有gunicorn进程
echo "停止所有Gunicorn进程..."
GUNICORN_PIDS=$(ps aux | grep gunicorn | grep -v grep | awk '{print $2}')
if [ -n "$GUNICORN_PIDS" ]; then
    for pid in $GUNICORN_PIDS; do
        echo "停止进程 $pid..."
        kill $pid 2>/dev/null || true
    done
    sleep 2
    
    # 强制停止仍在运行的进程
    REMAINING_PIDS=$(ps aux | grep gunicorn | grep -v grep | awk '{print $2}')
    if [ -n "$REMAINING_PIDS" ]; then
        echo "强制停止剩余进程..."
        for pid in $REMAINING_PIDS; do
            kill -9 $pid 2>/dev/null || true
        done
    fi
else
    echo "无Gunicorn进程运行"
fi

echo ""

# 检查端口
echo "检查端口状态..."
if netstat -tlnp | grep :8000 > /dev/null; then
    echo "✗ 端口8000仍在监听"
    netstat -tlnp | grep :8000
else
    echo "✓ 端口8000已释放"
fi

echo ""

# 清理PID文件
if [ -f "logs/app.pid" ]; then
    rm logs/app.pid
    echo "✓ PID文件已清理"
fi

echo "✓ 应用停止完成"
