#!/bin/bash

# 购买系统设置脚本
echo "开始设置购买系统..."

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. 更新数据库结构
echo "1. 更新数据库结构..."
source /root/miniconda3/bin/activate condavenv
python update_database.py

if [ $? -ne 0 ]; then
    echo "数据库更新失败，请检查错误信息"
    exit 1
fi

# 2. 设置交易处理定时任务
echo "2. 设置交易处理定时任务..."
./setup_cron_transactions.sh

# 3. 创建日志目录
echo "3. 创建日志目录..."
mkdir -p logs

# 4. 设置文件权限
echo "4. 设置文件权限..."
chmod +x process_transactions.py
chmod +x update_database.py

# 5. 测试邮件服务
echo "5. 测试邮件服务..."
source /root/miniconda3/bin/activate condavenv
python -c "
from app import create_app
from app.services.email_service import EmailService

app = create_app()
with app.app_context():
    email_service = EmailService()
    print('邮件服务初始化成功')
"

echo "购买系统设置完成！"
echo ""
echo "功能说明："
echo "1. 商品详情页已添加购买按钮和微信支付弹窗"
echo "2. 支持完整的交易流程：购买 -> 支付确认 -> 发货 -> 收货 -> 完成"
echo "3. 自动邮件通知：卖家发货提醒、买家收货提醒、交易超时通知"
echo "4. 系统公告定向推送：根据用户角色（买家/卖家）推送相关公告"
echo "5. 定时任务：每30分钟检查并处理超时交易"
echo "6. 管理后台：完整的交易监控和管理功能"
echo ""
echo "注意事项："
echo "1. 请确保MySQL服务正在运行"
echo "2. 请确保邮件服务配置正确"
echo "3. 定时任务已设置，请确保cron服务正在运行"
echo "4. 如有问题，请联系系统管理员：21641685@qq.com"
