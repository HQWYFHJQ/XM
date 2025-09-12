#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建公告表的数据库迁移脚本
"""

from app import create_app, db
from app.models import Announcement

def create_announcement_table():
    """创建公告表"""
    app = create_app()
    
    with app.app_context():
        try:
            # 创建公告表
            db.create_all()
            print("✅ 公告表创建成功！")
            
            # 检查表是否存在
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'announcements' in tables:
                print("✅ 公告表 'announcements' 已存在")
                
                # 显示表结构
                columns = inspector.get_columns('announcements')
                print("\n📋 公告表结构：")
                for column in columns:
                    print(f"  - {column['name']}: {column['type']}")
            else:
                print("❌ 公告表创建失败")
                
        except Exception as e:
            print(f"❌ 创建公告表时出错: {e}")

if __name__ == '__main__':
    create_announcement_table()
