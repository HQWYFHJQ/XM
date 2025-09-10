#!/bin/bash

# 校园跳蚤市场智能推荐平台 - 一键启动脚本

echo "=========================================="
echo "校园跳蚤市场智能推荐平台启动脚本"
echo "=========================================="

# 检查Python环境
echo "检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python版本: $PYTHON_VERSION"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "错误: 未找到pip3，请先安装pip3"
    exit 1
fi

# 检查MySQL连接
echo "检查MySQL连接..."
if ! command -v mysql &> /dev/null; then
    echo "警告: 未找到mysql客户端，请确保MySQL服务正在运行"
else
    # 测试MySQL连接
    mysql -h localhost -P 5081 -u root -p'4mapg]zj2Am"]9(;' -e "SELECT 1;" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "MySQL连接正常"
    else
        echo "警告: MySQL连接失败，请检查数据库配置"
    fi
fi

# 检查Redis连接
echo "检查Redis连接..."
if ! command -v redis-cli &> /dev/null; then
    echo "警告: 未找到redis-cli，请确保Redis服务正在运行"
else
    redis-cli ping 2>/dev/null | grep -q PONG
    if [ $? -eq 0 ]; then
        echo "Redis连接正常"
    else
        echo "警告: Redis连接失败，请检查Redis配置"
    fi
fi

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "升级pip..."
pip install --trusted-host mirrors.aliyun.com --upgrade pip

# 安装依赖
echo "安装Python依赖包..."
pip install --trusted-host mirrors.aliyun.com -r requirements.txt

# 创建必要的目录
echo "创建必要的目录..."
mkdir -p uploads/avatars
mkdir -p uploads/items
mkdir -p logs

# 设置权限
chmod 755 uploads/avatars
chmod 755 uploads/items
chmod 755 logs

# 初始化数据库
echo "初始化数据库..."
python app.py init-db

# 创建管理员用户（如果不存在）
echo "检查管理员用户..."
ADMIN_COUNT=$(python -c "
from app import create_app, db
from app.models import User
app = create_app()
with app.app_context():
    admin_count = User.query.filter_by(is_admin=True).count()
    print(admin_count)
" 2>/dev/null)

if [ "$ADMIN_COUNT" = "0" ]; then
    echo "未找到管理员用户，请创建管理员账户："
    python app.py create-admin
fi

# 启动应用
echo "=========================================="
echo "启动校园跳蚤市场智能推荐平台..."
echo "主应用端口: 8000"
echo "管理后台端口: 8080"
echo "=========================================="

# 启动主应用
echo "启动主应用 (端口 8000)..."
PYTHONPATH="/usr/lib/python3.8/site-packages:$PYTHONPATH" python app.py &
MAIN_PID=$!

# 等待主应用启动
sleep 3

# 启动管理后台
echo "启动管理后台 (端口 8080)..."
PYTHONPATH="/usr/lib/python3.8/site-packages:$PYTHONPATH" python -c "
from app import create_app
import os
os.environ['ADMIN_PORT'] = '8080'
app = create_app()
app.run(host='0.0.0.0', port=8080, debug=False)
" &
ADMIN_PID=$!

# 保存PID到文件
echo $MAIN_PID > main.pid
echo $ADMIN_PID > admin.pid

echo "=========================================="
echo "应用启动完成！"
echo "主应用: http://localhost:8000"
echo "管理后台: http://localhost:8080/admin"
echo "=========================================="
echo "按 Ctrl+C 停止服务"

# 等待用户中断
trap 'echo "正在停止服务..."; kill $MAIN_PID $ADMIN_PID 2>/dev/null; rm -f main.pid admin.pid; echo "服务已停止"; exit 0' INT

# 保持脚本运行
wait
