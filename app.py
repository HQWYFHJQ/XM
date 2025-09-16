#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
校园跳蚤市场
主应用入口文件
"""

from app import create_app, db
from app.models import User, Item, Category, UserBehavior, Recommendation, Transaction, Announcement
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Shell上下文处理器"""
    return {
        'db': db,
        'User': User,
        'Item': Item,
        'Category': Category,
        'UserBehavior': UserBehavior,
        'Recommendation': Recommendation,
        'Transaction': Transaction,
        'Announcement': Announcement
    }

@app.cli.command()
def init_db():
    """初始化数据库"""
    db.create_all()
    print("数据库表创建完成！")
    print("请运行 'python init_categories.py' 来初始化校园二手电子产品分类！")

@app.cli.command()
def init_categories():
    """初始化校园二手电子产品分类"""
    from init_categories import init_categories as init_cat
    init_cat()

@app.cli.command()
def create_admin():
    """创建管理员用户"""
    username = input("请输入管理员用户名: ")
    email = input("请输入管理员邮箱: ")
    password = input("请输入管理员密码: ")
    
    if User.query.filter_by(username=username).first():
        print("用户名已存在！")
        return
    
    if User.query.filter_by(email=email).first():
        print("邮箱已存在！")
        return
    
    admin = User(
        username=username,
        email=email,
        is_admin=True,
        is_active=True
    )
    admin.set_password(password)
    
    db.session.add(admin)
    db.session.commit()
    print("管理员用户创建成功！")

if __name__ == '__main__':
    # 确保上传目录存在
    os.makedirs('uploads/avatars', exist_ok=True)
    os.makedirs('uploads/items', exist_ok=True)
    
    # 运行应用
    app.run(
        host='0.0.0.0',
        port=app.config['MAIN_PORT'],
        debug=app.config['DEBUG']
    )
