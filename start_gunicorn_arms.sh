#!/bin/bash
# 使用Gunicorn + ARMS探针启动脚本（系统服务形式）

echo "=== 校园跳蚤市场应用启动脚本（系统服务形式）==="
echo "时间: $(date)"
echo ""

# 激活conda环境
echo "激活conda环境..."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate condavenv

# 设置阿里云ARMS环境变量
export ARMS_APP_NAME=campus_market
export ARMS_REGION_ID=cn-hangzhou
export ARMS_LICENSE_KEY=biimgsqhcm@6ca181feeeac0da
export ARMS_IS_PUBLIC=True
export ARMS_ENDPOINT=https://arms-dc-hz.aliyuncs.com

echo "环境变量设置:"
echo "ARMS_APP_NAME: $ARMS_APP_NAME"
echo "ARMS_REGION_ID: $ARMS_REGION_ID"
echo "ARMS_LICENSE_KEY: ${ARMS_LICENSE_KEY:0:8}...${ARMS_LICENSE_KEY: -4}"
echo "ARMS_IS_PUBLIC: $ARMS_IS_PUBLIC"
echo "ARMS_ENDPOINT: $ARMS_ENDPOINT"
echo ""

# 设置工作目录
cd /root/campus_market

# 确保必要目录存在
echo "创建必要目录..."
mkdir -p uploads/avatars
mkdir -p uploads/items
mkdir -p logs

# 安装Gunicorn（如果未安装）
echo "检查Gunicorn安装..."
if ! command -v gunicorn &> /dev/null; then
    echo "安装Gunicorn..."
    pip install gunicorn>=20.1.0
else
    echo "✓ Gunicorn已安装"
fi

# 检查aliyun-instrument命令
echo "检查aliyun-instrument命令..."
if command -v aliyun-instrument &> /dev/null; then
    echo "✓ aliyun-instrument 命令可用"
    aliyun-instrument --version
else
    echo "✗ aliyun-instrument 命令不可用"
    exit 1
fi
echo ""

# 检查网络连接
echo "检查ARMS网络连接..."
if nslookup arms-dc-hz.aliyuncs.com &> /dev/null; then
    echo "✓ ARMS域名解析正常"
else
    echo "✗ ARMS域名解析失败"
    echo "请检查网络连接和DNS设置"
    exit 1
fi
echo ""

# 停止现有的gunicorn进程
echo "停止现有的gunicorn进程..."
pkill -f "gunicorn.*wsgi:app" || true
sleep 2

# 计算Worker进程数
WORKER_COUNT=$(($(nproc) * 2 + 1))

echo "正在启动校园跳蚤市场应用（Gunicorn + ARMS云控模式）..."
echo "应用名称: $ARMS_APP_NAME"
echo "区域: $ARMS_REGION_ID"
echo "Worker进程数: $WORKER_COUNT"
echo "启动时间: $(date)"
echo ""

# 使用ARMS探针启动Gunicorn（后台运行）
echo "启动应用..."
nohup aliyun-instrument gunicorn --config gunicorn.conf.py wsgi:app > logs/gunicorn_service.log 2>&1 &

APP_PID=$!
echo "应用PID: $APP_PID"

# 保存PID到文件
echo $APP_PID > logs/app.pid

# 等待应用启动
echo "等待应用启动..."
sleep 5

# 检查应用是否启动成功
if ps -p $APP_PID > /dev/null; then
    echo "✓ 应用启动成功"
    
    # 检查端口
    if netstat -tlnp | grep :80 > /dev/null; then
        echo "✓ 端口80监听正常"
    else
        echo "✗ 端口80未监听"
    fi
    
    # 测试应用响应
    echo "测试应用响应..."
    if curl -s http://localhost:80/ > /dev/null 2>&1; then
        echo "✓ 应用响应正常"
    else
        echo "✗ 应用无响应"
    fi
    
    echo ""
    echo "=== 应用状态检查 ==="
    echo "进程信息:"
    ps aux | grep gunicorn | grep -v grep
    echo ""
    echo "端口监听:"
    netstat -tlnp | grep :80
    echo ""
    echo "最近日志:"
    tail -10 logs/gunicorn_service.log
    echo ""
    echo "✓ 校园跳蚤市场应用已成功启动！"
    echo "✓ ARMS探针已正确配置并启动"
    echo "✓ 应用在后台运行，关闭SSH不会影响服务"
    echo "✓ PID已保存到 logs/app.pid"
    echo ""
    echo "访问地址: http://localhost:80"
    echo "日志文件: logs/gunicorn_service.log"
    echo "PID文件: logs/app.pid"
    echo ""
    echo "管理命令:"
    echo "  查看状态: ./status_app.sh"
    echo "  停止应用: ./stop_app.sh"
    echo "  重启应用: ./restart_app.sh"
    echo "  查看日志: tail -f logs/gunicorn_service.log"
    
else
    echo "✗ 应用启动失败"
    echo "错误日志:"
    cat logs/gunicorn_service.log
    exit 1
fi
