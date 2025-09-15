#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交易处理定时任务
用于处理交易超时和自动确认
"""

import os
import sys
import time
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services.transaction_service import TransactionService

def main():
    """主函数"""
    print(f"[{datetime.now()}] 开始处理交易超时任务...")
    
    # 创建应用上下文
    app = create_app()
    
    with app.app_context():
        try:
            # 创建交易服务实例
            transaction_service = TransactionService()
            
            # 处理超时交易
            result = transaction_service.process_timeout_transactions()
            
            if result['success']:
                print(f"[{datetime.now()}] {result['message']}")
            else:
                print(f"[{datetime.now()}] 错误: {result['message']}")
            
            # 获取交易统计
            stats_result = transaction_service.get_transaction_stats()
            if stats_result['success']:
                stats = stats_result['stats']
                print(f"[{datetime.now()}] 交易统计:")
                print(f"  总交易数: {stats['total_transactions']}")
                print(f"  待支付: {stats['pending_transactions']}")
                print(f"  已支付: {stats['paid_transactions']}")
                print(f"  已发货: {stats['shipped_transactions']}")
                print(f"  已收货: {stats['delivered_transactions']}")
                print(f"  已完成: {stats['completed_transactions']}")
                print(f"  已取消: {stats['cancelled_transactions']}")
                print(f"  已超时: {stats['timeout_transactions']}")
                print(f"  今日交易: {stats['today_transactions']}")
                print(f"  本周交易: {stats['week_transactions']}")
                print(f"  本月交易: {stats['month_transactions']}")
            
        except Exception as e:
            print(f"[{datetime.now()}] 处理交易超时任务失败: {str(e)}")
            sys.exit(1)
    
    print(f"[{datetime.now()}] 交易超时任务处理完成")

if __name__ == '__main__':
    main()
