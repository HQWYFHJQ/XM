#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的ARMS测试程序
用于验证ARMS探针是否正常工作
"""

import os
import sys
import time
import requests
import subprocess
from datetime import datetime

def test_arms_basic():
    """基础ARMS功能测试"""
    print("=== ARMS基础功能测试 ===")
    
    # 设置环境变量
    os.environ['ARMS_APP_NAME'] = 'campus_market_test'
    os.environ['ARMS_REGION_ID'] = 'cn-hangzhou'
    os.environ['ARMS_LICENSE_KEY'] = 'biimgsqhcm@6ca181feeeac0da'
    os.environ['ARMS_IS_PUBLIC'] = 'True'
    os.environ['ARMS_ENDPOINT'] = 'https://arms-dc-hz.aliyuncs.com'
    
    print("环境变量设置完成")
    
    # 导入ARMS探针
    try:
        from aliyun.opentelemetry.instrumentation.auto_instrumentation import sitecustomize
        print("✓ ARMS探针导入成功")
    except ImportError as e:
        print(f"✗ ARMS探针导入失败: {e}")
        return False
    
    # 创建简单的Flask应用
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return jsonify({
            'message': 'ARMS测试应用',
            'timestamp': time.time(),
            'arms_enabled': True
        })
    
    @app.route('/test')
    def test():
        time.sleep(0.1)  # 模拟处理时间
        return jsonify({
            'message': '测试接口',
            'timestamp': time.time()
        })
    
    @app.route('/error')
    def error():
        raise Exception("测试错误")
    
    print("✓ Flask应用创建成功")
    return app

def run_test_server(app, port=8002):
    """运行测试服务器"""
    print(f"启动测试服务器在端口 {port}...")
    
    # 使用aliyun-instrument启动
    try:
        # 创建临时文件保存应用代码
        app_code = f'''
import os
os.environ['ARMS_APP_NAME'] = 'campus_market_test'
os.environ['ARMS_REGION_ID'] = 'cn-hangzhou'
os.environ['ARMS_LICENSE_KEY'] = 'biimgsqhcm@6ca181feeeac0da'
os.environ['ARMS_IS_PUBLIC'] = 'True'
os.environ['ARMS_ENDPOINT'] = 'https://arms-dc-hz.aliyuncs.com'

from aliyun.opentelemetry.instrumentation.auto_instrumentation import sitecustomize

from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({{
        'message': 'ARMS测试应用',
        'timestamp': time.time(),
        'arms_enabled': True
    }})

@app.route('/test')
def test():
    time.sleep(0.1)
    return jsonify({{
        'message': '测试接口',
        'timestamp': time.time()
    }})

@app.route('/error')
def error():
    raise Exception("测试错误")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port={port}, debug=False)
'''
        
        with open('/tmp/test_arms_simple.py', 'w', encoding='utf-8') as f:
            f.write(app_code)
        
        # 启动进程
        process = subprocess.Popen([
            'aliyun-instrument', 'python', '/tmp/test_arms_simple.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 等待启动
        time.sleep(3)
        
        # 测试请求
        test_requests(port)
        
        # 停止进程
        process.terminate()
        process.wait()
        
        print("✓ 测试完成")
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")

def test_requests(port):
    """发送测试请求"""
    print("发送测试请求...")
    
    base_url = f'http://localhost:{port}'
    
    # 测试正常请求
    try:
        response = requests.get(f'{base_url}/', timeout=5)
        if response.status_code == 200:
            print("✓ 首页请求成功")
            print(f"  响应: {response.json()}")
        else:
            print(f"✗ 首页请求失败: {response.status_code}")
    except Exception as e:
        print(f"✗ 首页请求异常: {e}")
    
    # 测试多个请求
    for i in range(3):
        try:
            response = requests.get(f'{base_url}/test', timeout=2)
            print(f"✓ 测试请求 {i+1}: {response.status_code}")
            time.sleep(0.5)
        except Exception as e:
            print(f"✗ 测试请求 {i+1} 失败: {e}")
    
    # 测试错误请求
    try:
        response = requests.get(f'{base_url}/error', timeout=2)
        print(f"✗ 错误请求应该失败但成功了: {response.status_code}")
    except requests.exceptions.HTTPError:
        print("✓ 错误请求正确处理")
    except Exception as e:
        print(f"✓ 错误请求异常处理: {e}")

def main():
    """主函数"""
    print("ARMS简化测试程序")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查aliyun-instrument命令
    try:
        result = subprocess.run(['aliyun-instrument', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✓ aliyun-instrument 可用: {result.stdout.strip()}")
        else:
            print("✗ aliyun-instrument 不可用")
            return
    except Exception as e:
        print(f"✗ 检查aliyun-instrument失败: {e}")
        return
    
    # 创建测试应用
    app = test_arms_basic()
    if not app:
        return
    
    # 运行测试
    run_test_server(app)

if __name__ == '__main__':
    main()
