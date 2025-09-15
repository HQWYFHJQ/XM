#!/usr/bin/env python3
"""
测试管理后台功能
"""

from app import create_app, db
from app.models import User, Transaction
from flask import url_for

def test_admin_panel():
    app = create_app()
    
    with app.app_context():
        # 检查管理员用户
        admin_user = User.query.filter_by(is_admin=True).first()
        if not admin_user:
            print("❌ 没有找到管理员用户")
            return
        
        print(f"✅ 找到管理员用户: {admin_user.username}")
        
        # 检查交易数据
        transaction_count = Transaction.query.count()
        print(f"✅ 交易总数: {transaction_count}")
        
        # 检查管理后台路由
        with app.test_client() as client:
            # 使用Flask-Login的login_user方法
            from flask_login import login_user
            with client.session_transaction() as sess:
                # 模拟用户登录状态
                sess['_user_id'] = str(admin_user.id)
                sess['_fresh'] = True
                sess['_id'] = '1'
            
            # 测试管理后台首页
            response = client.get('/admin/')
            print(f"✅ 管理后台首页状态码: {response.status_code}")
            
            # 测试交易管理页面
            response = client.get('/admin/transactions')
            print(f"✅ 交易管理页面状态码: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ 交易管理面板可以正常访问！")
                
                # 检查页面内容
                content = response.get_data(as_text=True)
                if '交易管理' in content:
                    print("✅ 页面包含'交易管理'标题")
                if '总交易数' in content:
                    print("✅ 页面包含交易统计信息")
                if 'table' in content:
                    print("✅ 页面包含交易列表表格")
            else:
                print(f"❌ 交易管理页面访问失败: {response.status_code}")

if __name__ == '__main__':
    test_admin_panel()
