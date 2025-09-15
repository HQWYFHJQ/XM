#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WSGI入口文件
供Gunicorn等WSGI服务器使用
"""

from app import create_app

# 创建Flask应用实例
app = create_app()

if __name__ == '__main__':
    app.run()
