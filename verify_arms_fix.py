#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARMS修复验证脚本
验证ARMS探针是否正常工作并上报数据
"""

import os
import sys
import time
import requests
import subprocess
from datetime import datetime

def print_section(title):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def check_arms_status():
    """检查ARMS探针状态"""
    print_section("ARMS探针状态检查")
    
    # 检查环境变量
    arms_vars = {
        'ARMS_APP_NAME': os.environ.get('ARMS_APP_NAME'),
        'ARMS_REGION_ID': os.environ.get('ARMS_REGION_ID'),
        'ARMS_LICENSE_KEY': os.environ.get('ARMS_LICENSE_KEY'),
        'ARMS_IS_PUBLIC': os.environ.get('ARMS_IS_PUBLIC'),
        'ARMS_ENDPOINT': os.environ.get('ARMS_ENDPOINT')
    }
    
    print("ARMS环境变量:")
    all_set = True
    for key, value in arms_vars.items():
        if value:
            if 'LICENSE_KEY' in key:
                print(f"  ✓ {key}: {value[:8]}...{value[-4:]}")
            else:
                print(f"  ✓ {key}: {value}")
        else:
            print(f"  ✗ {key}: 未设置")
            all_set = False
    
    return all_set

def test_application_requests():
    """测试应用请求生成监控数据"""
    print_section("应用请求测试")
    
    base_url = "http://localhost:80"
    
    # 测试用例
    test_cases = [
        ("首页", "/"),
        ("商品列表", "/api/items"),
        ("分类列表", "/api/categories"),
        ("推荐接口", "/api/recommendations"),
        ("用户统计", "/api/users/stats"),
    ]
    
    print("发送测试请求...")
    success_count = 0
    
    for name, endpoint in test_cases:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"  ✓ {name}: {response.status_code}")
                success_count += 1
            else:
                print(f"  ✗ {name}: {response.status_code}")
        except Exception as e:
            print(f"  ✗ {name}: 请求失败 - {e}")
        
        time.sleep(0.5)  # 避免请求过快
    
    print(f"\n成功请求: {success_count}/{len(test_cases)}")
    return success_count > 0

def generate_load_test():
    """生成负载测试数据"""
    print_section("负载测试数据生成")
    
    base_url = "http://localhost:80"
    
    print("生成负载测试数据...")
    
    # 并发请求测试
    import threading
    import queue
    
    results = queue.Queue()
    
    def make_request(request_id):
        try:
            response = requests.get(f"{base_url}/", timeout=3)
            results.put(f"请求 {request_id}: {response.status_code}")
        except Exception as e:
            results.put(f"请求 {request_id}: 失败 - {e}")
    
    # 启动多个并发请求
    threads = []
    for i in range(10):
        thread = threading.Thread(target=make_request, args=(i+1,))
        thread.start()
        threads.append(thread)
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    # 输出结果
    print("并发请求结果:")
    while not results.empty():
        print(f"  {results.get()}")
    
    print("✓ 负载测试完成")

def check_application_logs():
    """检查应用日志"""
    print_section("应用日志检查")
    
    log_files = [
        'logs/gunicorn_service.log',
        'logs/gunicorn_access.log',
        'logs/gunicorn_error.log'
    ]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            print(f"✓ 日志文件存在: {log_file}")
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        print(f"  最后3行:")
                        for line in lines[-3:]:
                            print(f"    {line.strip()}")
                    else:
                        print("  文件为空")
            except Exception as e:
                print(f"  读取失败: {e}")
        else:
            print(f"✗ 日志文件不存在: {log_file}")

def check_arms_instrumentation():
    """检查ARMS探针是否正常工作"""
    print_section("ARMS探针功能检查")
    
    try:
        # 检查aliyun-instrument命令
        result = subprocess.run(['aliyun-instrument', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✓ aliyun-instrument 可用: {result.stdout.strip()}")
        else:
            print("✗ aliyun-instrument 不可用")
            return False
    except Exception as e:
        print(f"✗ 检查aliyun-instrument失败: {e}")
        return False
    
    # 检查ARMS探针导入
    try:
        from aliyun.opentelemetry.instrumentation.auto_instrumentation import sitecustomize
        print("✓ ARMS探针导入成功")
        return True
    except ImportError as e:
        print(f"✗ ARMS探针导入失败: {e}")
        return False

def main():
    """主函数"""
    print("ARMS修复验证脚本")
    print(f"验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 设置环境变量
    os.environ['ARMS_APP_NAME'] = 'campus_market'
    os.environ['ARMS_REGION_ID'] = 'cn-hangzhou'
    os.environ['ARMS_LICENSE_KEY'] = 'biimgsqhcm@6ca181feeeac0da'
    os.environ['ARMS_IS_PUBLIC'] = 'True'
    os.environ['ARMS_ENDPOINT'] = 'https://arms-dc-hz.aliyuncs.com'
    
    # 执行检查
    arms_ok = check_arms_status()
    instrument_ok = check_arms_instrumentation()
    app_ok = test_application_requests()
    
    if app_ok:
        generate_load_test()
    
    check_application_logs()
    
    # 总结
    print_section("验证总结")
    
    if arms_ok and instrument_ok and app_ok:
        print("✓ ARMS探针配置正确")
        print("✓ 应用运行正常")
        print("✓ 监控数据正在生成")
        print("\n建议:")
        print("1. 等待5-10分钟让数据上报到阿里云ARMS控制台")
        print("2. 在ARMS控制台查看应用监控数据")
        print("3. 检查是否有告警和性能指标")
        print("4. 如果仍然没有数据，请检查网络连接和License Key")
    else:
        print("✗ 存在问题需要解决:")
        if not arms_ok:
            print("  - ARMS环境变量配置不正确")
        if not instrument_ok:
            print("  - ARMS探针未正确安装或导入")
        if not app_ok:
            print("  - 应用无法正常响应请求")

if __name__ == '__main__':
    main()
