#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
纯净服务功能测试脚本
测试不带ARMS探针的服务是否正常工作
"""

import requests
import time
import json
from datetime import datetime

def test_service():
    """测试服务基本功能"""
    base_url = "http://localhost:80"
    
    print("🧪 纯净服务功能测试")
    print("=" * 50)
    print(f"测试目标: {base_url}")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    test_results = []
    
    # 测试用例
    test_cases = [
        ("首页访问", "/", 200),
        ("API测试", "/api/categories", 200),
        ("API测试", "/api/users/stats", 200),
        ("静态资源", "/static/js/main.js", 200),
        ("错误页面", "/nonexistent-page", 404),
    ]
    
    print("📋 基础功能测试")
    print("-" * 30)
    
    for test_name, endpoint, expected_status in test_cases:
        try:
            start_time = time.time()
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            response_time = time.time() - start_time
            
            status = "SUCCESS" if response.status_code == expected_status else "FAILED"
            print(f"✅ {test_name}: {status}")
            print(f"   响应时间: {response_time:.3f}s")
            print(f"   HTTP状态码: {response.status_code}")
            
            test_results.append({
                "test": test_name,
                "endpoint": endpoint,
                "status": status,
                "response_time": response_time,
                "http_code": response.status_code,
                "expected": expected_status
            })
            
        except Exception as e:
            print(f"❌ {test_name}: ERROR")
            print(f"   错误信息: {str(e)}")
            test_results.append({
                "test": test_name,
                "endpoint": endpoint,
                "status": "ERROR",
                "error": str(e)
            })
        print()
    
    # 统计结果
    total_tests = len(test_results)
    success_tests = len([r for r in test_results if r.get("status") == "SUCCESS"])
    failed_tests = len([r for r in test_results if r.get("status") == "FAILED"])
    error_tests = len([r for r in test_results if r.get("status") == "ERROR"])
    
    print("📊 测试报告")
    print("=" * 50)
    print(f"总测试数: {total_tests}")
    print(f"成功: {success_tests}")
    print(f"失败: {failed_tests}")
    print(f"错误: {error_tests}")
    print(f"成功率: {(success_tests/total_tests)*100:.1f}%")
    
    # 响应时间统计
    response_times = [r.get("response_time", 0) for r in test_results if r.get("response_time")]
    if response_times:
        print()
        print("响应时间统计:")
        print(f"  平均响应时间: {sum(response_times)/len(response_times):.3f}s")
        print(f"  最小响应时间: {min(response_times):.3f}s")
        print(f"  最大响应时间: {max(response_times):.3f}s")
    
    # 保存详细报告
    report_data = {
        "test_time": datetime.now().isoformat(),
        "base_url": base_url,
        "total_tests": total_tests,
        "success_tests": success_tests,
        "failed_tests": failed_tests,
        "error_tests": error_tests,
        "success_rate": (success_tests/total_tests)*100,
        "response_times": response_times,
        "test_results": test_results
    }
    
    with open("logs/clean_service_test_report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print()
    print("📄 详细报告已保存到: logs/clean_service_test_report.json")
    print()
    print("✅ 服务测试完成！现在可以单独测试ARMS探针功能了。")

if __name__ == "__main__":
    test_service()
