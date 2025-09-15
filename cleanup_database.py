#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库清理脚本
删除campus_market数据库中多余的表，保留核心功能表
"""

import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': int(os.environ.get('DB_PORT', 5081)),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', '4mapg]zj2Am"]9(;'),
    'database': os.environ.get('DB_NAME', 'campus_market'),
    'charset': 'utf8mb4'
}

# 需要保留的核心表
CORE_TABLES = {
    'users', 'items', 'categories', 'transactions',
    'user_behaviors', 'recommendations',
    'conversations', 'messages', 'message_notifications', 
    'chat_sessions', 'message_cleanup_logs',
    'user_audits', 'item_audits', 'user_profile_audits', 
    'item_profile_audits', 'user_avatar_audits', 'item_image_audits',
    'announcements', 'announcement_reads'
}

# 需要删除的多余表（AI相关，项目未使用）
TABLES_TO_DELETE = {
    'ai_chat_messages', 'ai_chat_sessions', 
    'ai_recommendations', 'ai_user_preferences'
}

def get_existing_tables():
    """获取数据库中现有的所有表"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        cursor.execute("SHOW TABLES")
        tables = {row[0] for row in cursor.fetchall()}
        
        cursor.close()
        connection.close()
        
        return tables
    except Exception as e:
        print(f"错误: 无法连接到数据库 - {e}")
        return set()

def delete_tables(tables_to_delete):
    """删除指定的表"""
    if not tables_to_delete:
        print("没有需要删除的表")
        return True
    
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        print(f"准备删除以下表: {', '.join(tables_to_delete)}")
        
        # 禁用外键检查
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        deleted_tables = []
        for table in tables_to_delete:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
                deleted_tables.append(table)
                print(f"✓ 已删除表: {table}")
            except Exception as e:
                print(f"✗ 删除表 {table} 失败: {e}")
        
        # 重新启用外键检查
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        cursor.close()
        connection.close()
        
        print(f"\n成功删除 {len(deleted_tables)} 个表")
        return True
        
    except Exception as e:
        print(f"错误: 删除表时发生错误 - {e}")
        return False

def verify_core_tables():
    """验证核心表是否完整"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        cursor.execute("SHOW TABLES")
        existing_tables = {row[0] for row in cursor.fetchall()}
        
        missing_tables = CORE_TABLES - existing_tables
        if missing_tables:
            print(f"警告: 以下核心表缺失: {', '.join(missing_tables)}")
            return False
        else:
            print("✓ 所有核心表都存在")
            return True
            
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"错误: 验证核心表时发生错误 - {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("校园跳蚤市场 - 数据库清理脚本")
    print("=" * 60)
    
    # 获取现有表
    print("\n1. 检查数据库连接...")
    existing_tables = get_existing_tables()
    if not existing_tables:
        print("无法连接到数据库，退出")
        return
    
    print(f"✓ 数据库连接成功，发现 {len(existing_tables)} 个表")
    
    # 找出需要删除的表
    tables_to_delete = TABLES_TO_DELETE & existing_tables
    print(f"\n2. 分析表结构...")
    print(f"核心表数量: {len(CORE_TABLES)}")
    print(f"需要删除的表: {len(tables_to_delete)}")
    
    if tables_to_delete:
        print(f"将删除的表: {', '.join(tables_to_delete)}")
    else:
        print("没有需要删除的表")
    
    # 确认删除
    if tables_to_delete:
        print(f"\n3. 确认删除操作...")
        confirm = input("确定要删除这些表吗？(y/N): ").strip().lower()
        if confirm != 'y':
            print("操作已取消")
            return
    
    # 执行删除
    if tables_to_delete:
        print(f"\n4. 执行删除操作...")
        if not delete_tables(tables_to_delete):
            print("删除操作失败")
            return
    
    # 验证核心表
    print(f"\n5. 验证核心表...")
    if not verify_core_tables():
        print("警告: 核心表验证失败")
        return
    
    print(f"\n6. 清理完成！")
    print("=" * 60)
    print("数据库清理成功完成")
    print("已删除多余表，保留核心功能表")
    print("=" * 60)

if __name__ == "__main__":
    main()
