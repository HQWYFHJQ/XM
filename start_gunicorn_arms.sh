#!/bin/bash
# 使用Gunicorn + ARMS探针启动脚本（推荐生产环境）

# 激活conda环境
source ~/miniconda3/etc/profile.d/conda.sh
conda activate condavenv

# 设置阿里云ARMS环境变量
export ARMS_APP_NAME=campus_market
export ARMS_REGION_ID=cn-hangzhou
export ARMS_LICENSE_KEY=biimgsqhcm@6ca181feeeac0da
export ARMS_IS_PUBLIC=True

# 设置工作目录
cd /root/campus_market

# 确保必要目录存在
mkdir -p uploads/avatars
mkdir -p uploads/items
mkdir -p logs

# 安装Gunicorn（如果未安装）
pip install gunicorn>=20.1.0

echo "正在启动校园跳蚤市场应用（Gunicorn + ARMS云控模式）..."
echo "应用名称: $ARMS_APP_NAME"
echo "区域: $ARMS_REGION_ID"
echo "Worker进程数: $(($(nproc) * 2 + 1))"
echo "启动时间: $(date)"

# 使用ARMS探针启动Gunicorn
aliyun-instrument gunicorn --config gunicorn.conf.py app:app
