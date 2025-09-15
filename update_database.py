#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库更新脚本
用于添加购买功能相关的数据库字段
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Transaction, Announcement

def update_database():
    """更新数据库结构"""
    print("开始更新数据库结构...")
    
    # 创建应用上下文
    app = create_app()
    
    with app.app_context():
        try:
            # 检查并添加Transaction表的新字段
            print("检查Transaction表...")
            
            # 检查字段是否存在，如果不存在则添加
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('transactions')]
            
            new_columns = [
                ('payment_confirmed_at', 'DATETIME'),
                ('shipped_at', 'DATETIME'),
                ('delivered_at', 'DATETIME'),
                ('timeout_at', 'DATETIME'),
                ('shipping_notes', 'TEXT'),
                ('delivery_notes', 'TEXT'),
                ('dispute_reason', 'TEXT'),
                ('admin_notes', 'TEXT')
            ]
            
            for column_name, column_type in new_columns:
                if column_name not in columns:
                    print(f"添加字段 {column_name}...")
                    db.engine.execute(f"ALTER TABLE transactions ADD COLUMN {column_name} {column_type}")
                else:
                    print(f"字段 {column_name} 已存在")
            
            # 更新status枚举值
            print("更新Transaction表status枚举值...")
            try:
                db.engine.execute("""
                    ALTER TABLE transactions 
                    MODIFY COLUMN status ENUM('pending', 'paid', 'shipped', 'delivered', 'completed', 'cancelled', 'timeout') 
                    DEFAULT 'pending'
                """)
                print("Transaction表status枚举值更新成功")
            except Exception as e:
                print(f"更新Transaction表status枚举值失败: {e}")
            
            # 检查并添加Announcement表的新字段
            print("检查Announcement表...")
            
            columns = [col['name'] for col in inspector.get_columns('announcements')]
            
            new_announcement_columns = [
                ('target_type', "ENUM('all', 'buyer', 'seller', 'specific') DEFAULT 'all'"),
                ('target_user_ids', 'TEXT'),
                ('target_conditions', 'TEXT'),
                ('is_direct_push', 'BOOLEAN DEFAULT FALSE'),
                ('push_sent', 'BOOLEAN DEFAULT FALSE'),
                ('push_sent_at', 'DATETIME')
            ]
            
            for column_name, column_definition in new_announcement_columns:
                if column_name not in columns:
                    print(f"添加字段 {column_name}...")
                    db.engine.execute(f"ALTER TABLE announcements ADD COLUMN {column_name} {column_definition}")
                else:
                    print(f"字段 {column_name} 已存在")
            
            print("数据库结构更新完成！")
            
        except Exception as e:
            print(f"更新数据库失败: {str(e)}")
            return False
    
    return True

if __name__ == '__main__':
    success = update_database()
    if success:
        print("数据库更新成功！")
        sys.exit(0)
    else:
        print("数据库更新失败！")
        sys.exit(1)
