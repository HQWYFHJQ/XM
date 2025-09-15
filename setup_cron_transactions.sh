#!/bin/bash

# 设置交易处理定时任务
# 每30分钟检查一次交易超时

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 设置cron任务，每30分钟运行一次
(crontab -l 2>/dev/null; echo "*/30 * * * * cd $SCRIPT_DIR && /root/miniconda3/envs/condavenv/bin/python process_transactions.py >> logs/transaction_cron.log 2>&1") | crontab -

echo "交易处理定时任务已设置完成"
echo "任务将每30分钟运行一次"
echo "日志文件: logs/transaction_cron.log"

# 创建日志目录
mkdir -p logs

# 给脚本执行权限
chmod +x process_transactions.py

echo "设置完成！"
