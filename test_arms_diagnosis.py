#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARMS云控系统诊断测试程序
用于检查ARMS探针安装、配置和数据上报问题
"""

import os
import sys
import time
import requests
import subprocess
import json
from datetime import datetime

def print_section(title):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def check_environment():
    """检查环境变量和基础环境"""
    print_section("环境检查")
    
    # 检查ARMS环境变量
    arms_vars = {
        'ARMS_APP_NAME': os.environ.get('ARMS_APP_NAME'),
        'ARMS_REGION_ID': os.environ.get('ARMS_REGION_ID'),
        'ARMS_LICENSE_KEY': os.environ.get('ARMS_LICENSE_KEY'),
        'ARMS_IS_PUBLIC': os.environ.get('ARMS_IS_PUBLIC'),
        'ARMS_ENDPOINT': os.environ.get('ARMS_ENDPOINT')
    }
    
    print("ARMS环境变量:")
    for key, value in arms_vars.items():
        if value:
            if 'LICENSE_KEY' in key:
                print(f"  {key}: {value[:8]}...{value[-4:] if len(value) > 12 else '***'}")
            else:
                print(f"  {key}: {value}")
        else:
            print(f"  {key}: ❌ 未设置")
    
    # 检查Python环境
    print(f"\nPython版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    
    # 检查conda环境
    conda_env = os.environ.get('CONDA_DEFAULT_ENV', '未激活')
    print(f"Conda环境: {conda_env}")

def check_arms_installation():
    """检查ARMS探针安装状态"""
    print_section("ARMS探针安装检查")
    
    try:
        # 检查aliyun-instrument命令
        result = subprocess.run(['aliyun-instrument', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✓ aliyun-instrument 命令可用")
            print(f"  版本信息: {result.stdout.strip()}")
        else:
            print(f"✗ aliyun-instrument 命令不可用")
            print(f"  错误: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ aliyun-instrument 命令超时")
        return False
    except FileNotFoundError:
        print("✗ aliyun-instrument 命令未找到")
        return False
    except Exception as e:
        print(f"✗ 检查aliyun-instrument时出错: {e}")
        return False
    
    # 检查aliyun-bootstrap
    try:
        result = subprocess.run(['aliyun-bootstrap', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✓ aliyun-bootstrap 命令可用")
            print(f"  版本信息: {result.stdout.strip()}")
        else:
            print(f"✗ aliyun-bootstrap 命令不可用")
    except Exception as e:
        print(f"✗ 检查aliyun-bootstrap时出错: {e}")
    
    return True

def check_network_connectivity():
    """检查网络连接"""
    print_section("网络连接检查")
    
    # 检查ARMS端点连接
    arms_endpoint = os.environ.get('ARMS_ENDPOINT', 'https://arms-dc-hz.aliyuncs.com')
    print(f"ARMS端点: {arms_endpoint}")
    
    try:
        # 解析域名
        import socket
        host = arms_endpoint.replace('https://', '').replace('http://', '')
        ip = socket.gethostbyname(host)
        print(f"✓ 域名解析成功: {host} -> {ip}")
    except Exception as e:
        print(f"✗ 域名解析失败: {e}")
        return False
    
    # 检查HTTPS连接
    try:
        response = requests.get(arms_endpoint, timeout=10)
        print(f"✓ HTTPS连接成功: {response.status_code}")
    except requests.exceptions.Timeout:
        print("✗ HTTPS连接超时")
        return False
    except requests.exceptions.ConnectionError:
        print("✗ HTTPS连接失败")
        return False
    except Exception as e:
        print(f"✗ HTTPS连接出错: {e}")
        return False
    
    return True

def check_application_status():
    """检查应用运行状态"""
    print_section("应用状态检查")
    
    # 检查端口监听
    try:
        result = subprocess.run(['netstat', '-tlnp'], capture_output=True, text=True)
        if ':80' in result.stdout:
            print("✓ 端口80正在监听")
            # 提取监听进程信息
            for line in result.stdout.split('\n'):
                if ':80' in line:
                    print(f"  监听信息: {line.strip()}")
        else:
            print("✗ 端口80未监听")
    except Exception as e:
        print(f"✗ 检查端口监听时出错: {e}")
    
    # 检查应用响应
    try:
        response = requests.get('http://localhost:80/', timeout=5)
        if response.status_code == 200:
            print("✓ 应用响应正常")
        else:
            print(f"✗ 应用响应异常: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ 应用无响应")
    except Exception as e:
        print(f"✗ 检查应用响应时出错: {e}")

def test_arms_instrumentation():
    """测试ARMS探针功能"""
    print_section("ARMS探针功能测试")
    
    # 创建测试应用
    test_app_code = '''
import os
import time
from flask import Flask, jsonify

# 设置ARMS环境变量
os.environ['ARMS_APP_NAME'] = 'arms_test_app'
os.environ['ARMS_REGION_ID'] = 'cn-hangzhou'
os.environ['ARMS_LICENSE_KEY'] = 'biimgsqhcm@6ca181feeeac0da'
os.environ['ARMS_IS_PUBLIC'] = 'True'
os.environ['ARMS_ENDPOINT'] = 'https://arms-dc-hz.aliyuncs.com'

# 导入ARMS探针（必须在其他导入之前）
try:
    from aliyun.opentelemetry.instrumentation.auto_instrumentation import sitecustomize
    print("ARMS探针导入成功")
except ImportError as e:
    print(f"ARMS探针导入失败: {e}")

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=False)
'''
    
    # 写入测试应用文件
    with open('/tmp/test_arms_app.py', 'w', encoding='utf-8') as f:
        f.write(test_app_code)
    
    print("创建测试应用: /tmp/test_arms_app.py")
    
    # 使用aliyun-instrument启动测试应用
    try:
        print("使用ARMS探针启动测试应用...")
        process = subprocess.Popen([
            'aliyun-instrument', 'python', '/tmp/test_arms_app.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # 等待应用启动
        time.sleep(3)
        
        # 测试应用响应
        try:
            response = requests.get('http://localhost:8001/', timeout=5)
            if response.status_code == 200:
                print("✓ 测试应用启动成功")
                print(f"  响应: {response.json()}")
            else:
                print(f"✗ 测试应用响应异常: {response.status_code}")
        except Exception as e:
            print(f"✗ 测试应用无响应: {e}")
        
        # 测试多个请求
        print("发送测试请求...")
        for i in range(5):
            try:
                response = requests.get('http://localhost:8001/test', timeout=2)
                print(f"  请求 {i+1}: {response.status_code}")
                time.sleep(1)
            except Exception as e:
                print(f"  请求 {i+1} 失败: {e}")
        
        # 停止测试应用
        process.terminate()
        process.wait()
        print("✓ 测试应用已停止")
        
    except Exception as e:
        print(f"✗ 启动测试应用时出错: {e}")

def check_logs():
    """检查日志文件"""
    print_section("日志检查")
    
    log_files = [
        'logs/gunicorn_service.log',
        'logs/gunicorn_access.log',
        'logs/gunicorn_error.log',
        'app.log'
    ]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            print(f"✓ 日志文件存在: {log_file}")
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        print(f"  最后几行:")
                        for line in lines[-3:]:
                            print(f"    {line.strip()}")
                    else:
                        print("  文件为空")
            except Exception as e:
                print(f"  读取日志文件出错: {e}")
        else:
            print(f"✗ 日志文件不存在: {log_file}")

def main():
    """主函数"""
    print("ARMS云控系统诊断工具")
    print(f"诊断时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 执行各项检查
    check_environment()
    arms_ok = check_arms_installation()
    network_ok = check_network_connectivity()
    check_application_status()
    
    if arms_ok and network_ok:
        test_arms_instrumentation()
    
    check_logs()
    
    print_section("诊断总结")
    print("请检查上述输出，重点关注:")
    print("1. ARMS环境变量是否正确设置")
    print("2. aliyun-instrument命令是否可用")
    print("3. 网络连接是否正常")
    print("4. 应用是否正常运行")
    print("5. 日志中是否有错误信息")

if __name__ == '__main__':
    main()
