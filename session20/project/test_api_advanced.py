#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session20 API开发项目高级测试脚本
全面测试图书管理系统API的各项功能

功能特性:
1. 完整的API测试流程
2. 错误处理测试
3. 性能测试
4. 并发测试
5. 数据验证测试

作者: Python学习教程
日期: 2024
"""

import requests
import json
import time
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import string

class APITester:
    """API测试器"""
    
    def __init__(self, base_url='http://localhost:5001'):
        """初始化测试器
        
        Args:
            base_url (str): API基础URL
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None
        self.test_results = []
        
        # 测试数据
        self.test_user = {
            'username': f'testuser_{int(time.time())}',
            'email': f'test_{int(time.time())}@example.com',
            'password': 'testpass123'
        }
        
        self.test_book = {
            'title': 'API测试图书',
            'author': '测试作者',
            'category': '技术',
            'description': '这是一本用于API测试的图书',
            'publisher': '测试出版社',
            'price': 99.99,
            'stock': 10,
            'isbn': '9781234567890'
        }
    
    def log_result(self, test_name, success, message, duration=None, data=None):
        """记录测试结果
        
        Args:
            test_name (str): 测试名称
            success (bool): 是否成功
            message (str): 结果消息
            duration (float): 执行时间
            data (dict): 响应数据
        """
        result = {
            'test_name': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'duration': duration,
            'data': data
        }
        self.test_results.append(result)
        
        status = "✅" if success else "❌"
        duration_str = f" ({duration:.3f}s)" if duration else ""
        print(f"{status} {test_name}: {message}{duration_str}")
    
    def make_request(self, method, endpoint, data=None, headers=None, auth_required=True):
        """发送HTTP请求
        
        Args:
            method (str): HTTP方法
            endpoint (str): API端点
            data (dict): 请求数据
            headers (dict): 请求头
            auth_required (bool): 是否需要认证
            
        Returns:
            tuple: (response, duration)
        """
        url = f"{self.base_url}{endpoint}"
        
        # 设置请求头
        request_headers = {'Content-Type': 'application/json'}
        if headers:
            request_headers.update(headers)
        
        # 添加认证头
        if auth_required and self.access_token:
            request_headers['Authorization'] = f'Bearer {self.access_token}'
        
        # 发送请求
        start_time = time.time()
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=request_headers, params=data)
            elif method.upper() == 'POST':
                response = self.session.post(url, headers=request_headers, json=data)
            elif method.upper() == 'PUT':
                response = self.session.put(url, headers=request_headers, json=data)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=request_headers)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            duration = time.time() - start_time
            return response, duration
            
        except Exception as e:
            duration = time.time() - start_time
            print(f"请求失败: {str(e)}")
            return None, duration
    
    def test_server_connection(self):
        """测试服务器连接"""
        try:
            response, duration = self.make_request('GET', '/', auth_required=False)
            if response and response.status_code == 200:
                self.log_result(
                    "服务器连接测试", True, 
                    "服务器连接正常", duration, response.json()
                )
                return True
            else:
                self.log_result(
                    "服务器连接测试", False, 
                    f"服务器响应异常: {response.status_code if response else 'No response'}"
                )
                return False
        except Exception as e:
            self.log_result("服务器连接测试", False, f"连接失败: {str(e)}")
            return False
    
    def test_user_registration(self):
        """测试用户注册"""
        response, duration = self.make_request(
            'POST', '/api/auth/register', 
            self.test_user, auth_required=False
        )
        
        if response and response.status_code == 201:
            data = response.json()
            self.log_result(
                "用户注册测试", True, 
                f"用户 {self.test_user['username']} 注册成功", 
                duration, data
            )
            return True
        else:
            error_msg = response.json().get('error', '未知错误') if response else '请求失败'
            self.log_result(
                "用户注册测试", False, 
                f"注册失败: {error_msg}", duration
            )
            return False
    
    def test_user_login(self):
        """测试用户登录"""
        login_data = {
            'username': self.test_user['username'],
            'password': self.test_user['password']
        }
        
        response, duration = self.make_request(
            'POST', '/api/auth/login', 
            login_data, auth_required=False
        )
        
        if response and response.status_code == 200:
            data = response.json()
            self.access_token = data.get('access_token')
            self.refresh_token = data.get('refresh_token')
            
            self.log_result(
                "用户登录测试", True, 
                f"用户 {self.test_user['username']} 登录成功", 
                duration, {'user': data.get('user')}
            )
            return True
        else:
            error_msg = response.json().get('error', '未知错误') if response else '请求失败'
            self.log_result(
                "用户登录测试", False, 
                f"登录失败: {error_msg}", duration
            )
            return False
    
    def test_admin_login(self):
        """测试管理员登录"""
        admin_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        
        response, duration = self.make_request(
            'POST', '/api/auth/login', 
            admin_data, auth_required=False
        )
        
        if response and response.status_code == 200:
            data = response.json()
            self.access_token = data.get('access_token')
            self.refresh_token = data.get('refresh_token')
            
            self.log_result(
                "管理员登录测试", True, 
                "管理员登录成功", duration, {'user': data.get('user')}
            )
            return True
        else:
            error_msg = response.json().get('error', '未知错误') if response else '请求失败'
            self.log_result(
                "管理员登录测试", False, 
                f"管理员登录失败: {error_msg}", duration
            )
            return False
    
    def test_token_refresh(self):
        """测试Token刷新"""
        if not self.refresh_token:
            self.log_result("Token刷新测试", False, "没有可用的刷新令牌")
            return False
        
        # 使用刷新令牌
        headers = {'Authorization': f'Bearer {self.refresh_token}'}
        response, duration = self.make_request(
            'POST', '/api/auth/refresh', 
            headers=headers, auth_required=False
        )
        
        if response and response.status_code == 200:
            data = response.json()
            self.access_token = data.get('access_token')
            
            self.log_result(
                "Token刷新测试", True, 
                "Token刷新成功", duration, data
            )
            return True
        else:
            error_msg = response.json().get('error', '未知错误') if response else '请求失败'
            self.log_result(
                "Token刷新测试", False, 
                f"Token刷新失败: {error_msg}", duration
            )
            return False
    
    def test_create_book(self):
        """测试创建图书"""
        response, duration = self.make_request(
            'POST', '/api/books', self.test_book
        )
        
        if response and response.status_code == 201:
            data = response.json()
            self.test_book['id'] = data.get('book', {}).get('id')
            
            self.log_result(
                "创建图书测试", True, 
                f"图书 '{self.test_book['title']}' 创建成功", 
                duration, data
            )
            return True
        else:
            error_msg = response.json().get('error', '未知错误') if response else '请求失败'
            self.log_result(
                "创建图书测试", False, 
                f"创建图书失败: {error_msg}", duration
            )
            return False
    
    def test_get_books(self):
        """测试获取图书列表"""
        response, duration = self.make_request(
            'GET', '/api/books', auth_required=False
        )
        
        if response and response.status_code == 200:
            data = response.json()
            book_count = len(data.get('books', []))
            
            self.log_result(
                "获取图书列表测试", True, 
                f"成功获取 {book_count} 本图书", 
                duration, {'count': book_count}
            )
            return True
        else:
            error_msg = response.json().get('error', '未知错误') if response else '请求失败'
            self.log_result(
                "获取图书列表测试", False, 
                f"获取图书列表失败: {error_msg}", duration
            )
            return False
    
    def test_get_book_detail(self):
        """测试获取图书详情"""
        if not self.test_book.get('id'):
            self.log_result("获取图书详情测试", False, "没有可用的图书ID")
            return False
        
        response, duration = self.make_request(
            'GET', f'/api/books/{self.test_book["id"]}', auth_required=False
        )
        
        if response and response.status_code == 200:
            data = response.json()
            self.log_result(
                "获取图书详情测试", True, 
                f"成功获取图书 '{data.get('book', {}).get('title')}' 的详情", 
                duration, data
            )
            return True
        else:
            error_msg = response.json().get('error', '未知错误') if response else '请求失败'
            self.log_result(
                "获取图书详情测试", False, 
                f"获取图书详情失败: {error_msg}", duration
            )
            return False
    
    def test_update_book(self):
        """测试更新图书"""
        if not self.test_book.get('id'):
            self.log_result("更新图书测试", False, "没有可用的图书ID")
            return False
        
        update_data = {
            'title': self.test_book['title'] + ' (已更新)',
            'price': self.test_book['price'] + 10.00
        }
        
        response, duration = self.make_request(
            'PUT', f'/api/books/{self.test_book["id"]}', update_data
        )
        
        if response and response.status_code == 200:
            data = response.json()
            self.log_result(
                "更新图书测试", True, 
                f"图书更新成功", duration, data
            )
            return True
        else:
            error_msg = response.json().get('error', '未知错误') if response else '请求失败'
            self.log_result(
                "更新图书测试", False, 
                f"更新图书失败: {error_msg}", duration
            )
            return False
    
    def test_search_books(self):
        """测试搜索图书"""
        search_params = {'search': 'Python'}
        response, duration = self.make_request(
            'GET', '/api/books', search_params, auth_required=False
        )
        
        if response and response.status_code == 200:
            data = response.json()
            book_count = len(data.get('books', []))
            
            self.log_result(
                "搜索图书测试", True, 
                f"搜索到 {book_count} 本相关图书", 
                duration, {'count': book_count}
            )
            return True
        else:
            error_msg = response.json().get('error', '未知错误') if response else '请求失败'
            self.log_result(
                "搜索图书测试", False, 
                f"搜索图书失败: {error_msg}", duration
            )
            return False
    
    def test_get_statistics(self):
        """测试获取统计信息"""
        response, duration = self.make_request(
            'GET', '/api/books/stats', auth_required=False
        )
        
        if response and response.status_code == 200:
            data = response.json()
            stats = data.get('statistics', {})
            
            self.log_result(
                "获取统计信息测试", True, 
                f"成功获取统计信息", duration, stats
            )
            return True
        else:
            error_msg = response.json().get('error', '未知错误') if response else '请求失败'
            self.log_result(
                "获取统计信息测试", False, 
                f"获取统计信息失败: {error_msg}", duration
            )
            return False
    
    def test_rate_limiting(self):
        """测试限流功能"""
        print("\n🔄 开始限流测试...")
        
        # 快速发送多个请求
        request_count = 0
        rate_limited = False
        
        for i in range(20):
            response, duration = self.make_request(
                'GET', '/api/books', auth_required=False
            )
            request_count += 1
            
            if response and response.status_code == 429:
                rate_limited = True
                self.log_result(
                    "限流测试", True, 
                    f"在第 {request_count} 个请求时触发限流", duration
                )
                break
            
            time.sleep(0.1)  # 短暂延迟
        
        if not rate_limited:
            self.log_result(
                "限流测试", False, 
                f"发送了 {request_count} 个请求但未触发限流"
            )
        
        return rate_limited
    
    def test_error_handling(self):
        """测试错误处理"""
        print("\n🔄 开始错误处理测试...")
        
        # 测试404错误
        response, duration = self.make_request(
            'GET', '/api/books/99999', auth_required=False
        )
        
        if response and response.status_code == 404:
            self.log_result(
                "404错误处理测试", True, 
                "正确返回404错误", duration
            )
        else:
            self.log_result(
                "404错误处理测试", False, 
                f"期望404错误，实际返回: {response.status_code if response else 'No response'}"
            )
        
        # 测试401错误（未认证）
        self.access_token = None  # 清除token
        response, duration = self.make_request(
            'POST', '/api/books', self.test_book
        )
        
        if response and response.status_code == 401:
            self.log_result(
                "401错误处理测试", True, 
                "正确返回401错误", duration
            )
        else:
            self.log_result(
                "401错误处理测试", False, 
                f"期望401错误，实际返回: {response.status_code if response else 'No response'}"
            )
    
    def test_concurrent_requests(self, num_threads=5, requests_per_thread=10):
        """测试并发请求"""
        print(f"\n🔄 开始并发测试 ({num_threads} 线程，每线程 {requests_per_thread} 请求)...")
        
        def make_concurrent_request(thread_id):
            """并发请求函数"""
            results = []
            for i in range(requests_per_thread):
                start_time = time.time()
                response, duration = self.make_request(
                    'GET', '/api/books', auth_required=False
                )
                
                success = response and response.status_code == 200
                results.append({
                    'thread_id': thread_id,
                    'request_id': i,
                    'success': success,
                    'duration': duration,
                    'status_code': response.status_code if response else None
                })
            
            return results
        
        # 执行并发测试
        start_time = time.time()
        all_results = []
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(make_concurrent_request, i) for i in range(num_threads)]
            
            for future in as_completed(futures):
                all_results.extend(future.result())
        
        total_duration = time.time() - start_time
        
        # 分析结果
        successful_requests = sum(1 for r in all_results if r['success'])
        total_requests = len(all_results)
        avg_duration = sum(r['duration'] for r in all_results) / total_requests
        
        self.log_result(
            "并发请求测试", True, 
            f"完成 {total_requests} 个并发请求，成功率: {successful_requests/total_requests*100:.1f}%，"
            f"平均响应时间: {avg_duration:.3f}s，总耗时: {total_duration:.3f}s"
        )
        
        return all_results
    
    def test_data_validation(self):
        """测试数据验证"""
        print("\n🔄 开始数据验证测试...")
        
        # 测试无效的图书数据
        invalid_books = [
            {'title': '', 'author': '作者', 'category': '技术'},  # 空标题
            {'title': '标题', 'author': '', 'category': '技术'},  # 空作者
            {'title': '标题', 'author': '作者', 'category': '无效分类'},  # 无效分类
            {'title': '标题', 'author': '作者', 'category': '技术', 'price': -10},  # 负价格
            {'title': '标题', 'author': '作者', 'category': '技术', 'stock': -5},  # 负库存
        ]
        
        validation_passed = 0
        
        for i, invalid_book in enumerate(invalid_books):
            response, duration = self.make_request(
                'POST', '/api/books', invalid_book
            )
            
            if response and response.status_code == 400:
                validation_passed += 1
                self.log_result(
                    f"数据验证测试 {i+1}", True, 
                    "正确拒绝无效数据", duration
                )
            else:
                self.log_result(
                    f"数据验证测试 {i+1}", False, 
                    f"应该拒绝无效数据，实际返回: {response.status_code if response else 'No response'}"
                )
        
        return validation_passed == len(invalid_books)
    
    def test_delete_book(self):
        """测试删除图书"""
        if not self.test_book.get('id'):
            self.log_result("删除图书测试", False, "没有可用的图书ID")
            return False
        
        response, duration = self.make_request(
            'DELETE', f'/api/books/{self.test_book["id"]}'
        )
        
        if response and response.status_code == 200:
            self.log_result(
                "删除图书测试", True, 
                f"图书删除成功", duration
            )
            return True
        else:
            error_msg = response.json().get('error', '未知错误') if response else '请求失败'
            self.log_result(
                "删除图书测试", False, 
                f"删除图书失败: {error_msg}", duration
            )
            return False
    
    def test_logout(self):
        """测试用户登出"""
        response, duration = self.make_request(
            'POST', '/api/auth/logout'
        )
        
        if response and response.status_code == 200:
            self.access_token = None
            self.refresh_token = None
            
            self.log_result(
                "用户登出测试", True, 
                "用户登出成功", duration
            )
            return True
        else:
            error_msg = response.json().get('error', '未知错误') if response else '请求失败'
            self.log_result(
                "用户登出测试", False, 
                f"登出失败: {error_msg}", duration
            )
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "="*60)
        print("🧪 Session20 API 高级测试开始")
        print("="*60)
        
        start_time = time.time()
        
        # 基础连接测试
        if not self.test_server_connection():
            print("\n❌ 服务器连接失败，终止测试")
            return
        
        # 认证流程测试
        print("\n🔐 认证流程测试")
        print("-" * 30)
        self.test_user_registration()
        self.test_user_login()
        self.test_token_refresh()
        
        # 切换到管理员账户
        print("\n👑 管理员功能测试")
        print("-" * 30)
        self.test_admin_login()
        
        # 图书管理测试
        print("\n📚 图书管理测试")
        print("-" * 30)
        self.test_create_book()
        self.test_get_books()
        self.test_get_book_detail()
        self.test_update_book()
        self.test_search_books()
        self.test_get_statistics()
        
        # 高级功能测试
        print("\n🔧 高级功能测试")
        print("-" * 30)
        self.test_rate_limiting()
        self.test_error_handling()
        self.test_data_validation()
        self.test_concurrent_requests()
        
        # 清理测试
        print("\n🧹 清理测试")
        print("-" * 30)
        self.test_delete_book()
        self.test_logout()
        
        # 测试总结
        total_duration = time.time() - start_time
        self.print_test_summary(total_duration)
    
    def print_test_summary(self, total_duration):
        """打印测试总结"""
        print("\n" + "="*60)
        print("📊 测试总结")
        print("="*60)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for r in self.test_results if r['success'])
        failed_tests = total_tests - successful_tests
        
        print(f"\n📈 测试统计:")
        print(f"  总测试数: {total_tests}")
        print(f"  成功: {successful_tests} ✅")
        print(f"  失败: {failed_tests} ❌")
        print(f"  成功率: {successful_tests/total_tests*100:.1f}%")
        print(f"  总耗时: {total_duration:.3f}秒")
        
        if failed_tests > 0:
            print(f"\n❌ 失败的测试:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test_name']}: {result['message']}")
        
        # 性能统计
        durations = [r['duration'] for r in self.test_results if r['duration']]
        if durations:
            avg_duration = sum(durations) / len(durations)
            max_duration = max(durations)
            min_duration = min(durations)
            
            print(f"\n⚡ 性能统计:")
            print(f"  平均响应时间: {avg_duration:.3f}秒")
            print(f"  最快响应时间: {min_duration:.3f}秒")
            print(f"  最慢响应时间: {max_duration:.3f}秒")
        
        print("\n" + "="*60)
        
        # 保存测试结果到文件
        self.save_test_results()
    
    def save_test_results(self):
        """保存测试结果到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"api_test_results_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.test_results, f, ensure_ascii=False, indent=2)
            print(f"\n💾 测试结果已保存到: {filename}")
        except Exception as e:
            print(f"\n❌ 保存测试结果失败: {str(e)}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Session20 API高级测试工具')
    parser.add_argument('--url', default='http://localhost:5001', 
                       help='API服务器URL (默认: http://localhost:5001)')
    parser.add_argument('--threads', type=int, default=5, 
                       help='并发测试线程数 (默认: 5)')
    parser.add_argument('--requests', type=int, default=10, 
                       help='每线程请求数 (默认: 10)')
    
    args = parser.parse_args()
    
    # 创建测试器并运行测试
    tester = APITester(args.url)
    tester.run_all_tests()

if __name__ == '__main__':
    main()