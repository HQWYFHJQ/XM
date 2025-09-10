#!/bin/bash
# 设置消息清理定时任务

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 创建cron任务
# 每天凌晨2点执行消息清理
(crontab -l 2>/dev/null; echo "0 2 * * * cd $SCRIPT_DIR && python3 cleanup_messages.py >> logs/cleanup.log 2>&1") | crontab -

echo "消息清理定时任务已设置完成"
echo "任务将在每天凌晨2点执行"
echo "日志文件: logs/cleanup.log"
