#!/bin/bash
# 校园跳蚤市场应用管理脚本

case "$1" in
    start)
        echo "🚀 启动校园跳蚤市场应用..."
        ./start_app.sh
        ;;
    stop)
        echo "🛑 停止校园跳蚤市场应用..."
        if [ -f logs/app.pid ]; then
            PID=$(cat logs/app.pid)
            if ps -p $PID > /dev/null; then
                kill $PID
                echo "✅ 应用已停止 (PID: $PID)"
            else
                echo "❌ 应用进程不存在"
            fi
        else
            echo "❌ PID文件不存在"
        fi
        ;;
    restart)
        echo "🔄 重启校园跳蚤市场应用..."
        ./manage_app.sh stop
        sleep 3
        ./manage_app.sh start
        ;;
    status)
        echo "📊 校园跳蚤市场应用状态:"
        if [ -f logs/app.pid ]; then
            PID=$(cat logs/app.pid)
            if ps -p $PID > /dev/null; then
                echo "✅ 应用运行中 (PID: $PID)"
                echo "📁 进程信息:"
                ps aux | grep $PID | grep -v grep
                echo ""
                echo "🌐 端口监听:"
                netstat -tlnp | grep :80
                echo ""
                echo "📈 最近日志:"
                tail -5 logs/gunicorn_service.log
            else
                echo "❌ 应用未运行"
            fi
        else
            echo "❌ PID文件不存在"
        fi
        ;;
    logs)
        echo "📋 查看应用日志..."
        if [ -f logs/gunicorn_service.log ]; then
            tail -f logs/gunicorn_service.log
        else
            echo "❌ 日志文件不存在"
        fi
        ;;
    *)
        echo "校园跳蚤市场应用管理脚本"
        echo ""
        echo "用法: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "命令说明:"
        echo "  start   - 启动应用"
        echo "  stop    - 停止应用"
        echo "  restart - 重启应用"
        echo "  status  - 查看应用状态"
        echo "  logs    - 查看实时日志"
        echo ""
        echo "示例:"
        echo "  $0 start    # 启动应用"
        echo "  $0 status   # 查看状态"
        echo "  $0 logs     # 查看日志"
        ;;
esac
