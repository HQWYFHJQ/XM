#!/bin/bash
# 阿里云ARMS云控系统启动脚本

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

# 确保上传目录存在
mkdir -p uploads/avatars
mkdir -p uploads/items

# 使用ARMS探针启动应用
echo "正在启动校园跳蚤市场应用（ARMS云控模式）..."
echo "应用名称: $ARMS_APP_NAME"
echo "区域: $ARMS_REGION_ID"
echo "启动时间: $(date)"

# 方式1: 使用ARMS探针直接启动Python应用
aliyun-instrument python app.py

# 方式2: 使用Gunicorn + ARMS探针（推荐生产环境）
# aliyun-instrument gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 --keep-alive 2 --max-requests 1000 --max-requests-jitter 100 app:app
