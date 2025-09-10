#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消息清理定时任务
用于清理超过30天的消息数据
"""

import os
import sys
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.services.message_service import MessageService

def cleanup_messages():
    """清理过期消息"""
    app = create_app()
    
    with app.app_context():
        try:
            print(f"[{datetime.now()}] 开始清理过期消息...")
            
            # 清理超过30天的消息
            result = MessageService.cleanup_old_messages(retention_days=30)
            
            print(f"[{datetime.now()}] 消息清理完成:")
            print(f"  - 删除消息数量: {result['messages_deleted']}")
            print(f"  - 删除对话数量: {result['conversations_deleted']}")
            
        except Exception as e:
            print(f"[{datetime.now()}] 消息清理失败: {e}")
            return False
    
    return True

if __name__ == '__main__':
    success = cleanup_messages()
    sys.exit(0 if success else 1)
