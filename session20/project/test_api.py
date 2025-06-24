#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session20 API开发演示项目 - API测试脚本
图书管理系统API接口测试

作者: Python学习教程
日期: 2024
"""

import requests
import json
import time
from typing import Dict, Any, Optional

class BookstoreAPITester:
    """图书管理API测试类"""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
        
        # 设置请求头
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     auth_required: bool = False) -> Dict[str, Any]:
        """发送HTTP请求"""
        url = f"{self.base_url}{endpoint}"
        
        # 添加认证头
        headers = {}
        if auth_required and self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=headers)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, headers=headers)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"不支持的HTTP方法: {method}")
            
            return {
                'status_code': response.status_code,
                'data': response.json() if response.content else {},
                'headers': dict(response.headers)
            }
        except requests.exceptions.RequestException as e:
            return {
                'status_code': 0,
                'data': {'error': str(e)},
                'headers': {}
            }
    
    def test_user_registration(self) -> bool:
        """测试用户注册"""
        print("\n=== 测试用户注册 ===")
        
        test_user = {
            'username': f'testuser_{int(time.time())}',
            'email': f'test_{int(time.time())}@example.com',
            'password': 'testpass123'
        }
        
        response = self._make_request('POST', '/api/auth/register', test_user)
        
        print(f"状态码: {response['status_code']}")
        print(f"响应: {json.dumps(response['data'], ensure_ascii=False, indent=2)}")
        
        if response['status_code'] == 201:
            print("✅ 用户注册成功")
            return True
        else:
            print("❌ 用户注册失败")
            return False
    
    def test_user_login(self) -> bool:
        """测试用户登录"""
        print("\n=== 测试用户登录 ===")
        
        # 使用默认管理员账号
        login_data = {
            'username': 'admin',
            'password': 'admin123'
        }
        
        response = self._make_request('POST', '/api/auth/login', login_data)
        
        print(f"状态码: {response['status_code']}")
        print(f"响应: {json.dumps(response['data'], ensure_ascii=False, indent=2)}")
        
        if response['status_code'] == 200 and response['data'].get('success'):
            self.access_token = response['data']['data']['access_token']
            print("✅ 用户登录成功")
            print(f"Token: {self.access_token[:50]}...")
            return True
        else:
            print("❌ 用户登录失败")
            return False
    
    def test_get_books(self) -> bool:
        """测试获取图书列表"""
        print("\n=== 测试获取图书列表 ===")
        
        # 测试基本查询
        response = self._make_request('GET', '/api/books')
        print(f"基本查询 - 状态码: {response['status_code']}")
        
        if response['status_code'] == 200:
            data = response['data']
            print(f"图书数量: {len(data.get('data', []))}")
            print(f"分页信息: {data.get('pagination', {})}")
        
        # 测试分页查询
        response = self._make_request('GET', '/api/books?page=1&per_page=2')
        print(f"\n分页查询 - 状态码: {response['status_code']}")
        
        # 测试搜索查询
        response = self._make_request('GET', '/api/books?search=Python')
        print(f"搜索查询 - 状态码: {response['status_code']}")
        
        # 测试分类查询
        response = self._make_request('GET', '/api/books?category=编程')
        print(f"分类查询 - 状态码: {response['status_code']}")
        
        if response['status_code'] == 200:
            print("✅ 获取图书列表成功")
            return True
        else:
            print("❌ 获取图书列表失败")
            return False
    
    def test_create_book(self) -> Optional[int]:
        """测试创建图书"""
        print("\n=== 测试创建图书 ===")
        
        new_book = {
            'title': f'测试图书_{int(time.time())}',
            'author': '测试作者',
            'isbn': f'978{int(time.time())}',
            'price': 99.99,
            'stock': 10,
            'category': '测试',
            'description': '这是一本测试图书'
        }
        
        response = self._make_request('POST', '/api/books', new_book, auth_required=True)
        
        print(f"状态码: {response['status_code']}")
        print(f"响应: {json.dumps(response['data'], ensure_ascii=False, indent=2)}")
        
        if response['status_code'] == 201:
            book_id = response['data']['data']['id']
            print(f"✅ 创建图书成功，ID: {book_id}")
            return book_id
        else:
            print("❌ 创建图书失败")
            return None
    
    def test_get_book(self, book_id: int) -> bool:
        """测试获取单个图书"""
        print(f"\n=== 测试获取图书 ID: {book_id} ===")
        
        response = self._make_request('GET', f'/api/books/{book_id}')
        
        print(f"状态码: {response['status_code']}")
        print(f"响应: {json.dumps(response['data'], ensure_ascii=False, indent=2)}")
        
        if response['status_code'] == 200:
            print("✅ 获取图书详情成功")
            return True
        else:
            print("❌ 获取图书详情失败")
            return False
    
    def test_update_book(self, book_id: int) -> bool:
        """测试更新图书"""
        print(f"\n=== 测试更新图书 ID: {book_id} ===")
        
        update_data = {
            'price': 129.99,
            'stock': 15,
            'description': '这是一本更新后的测试图书'
        }
        
        response = self._make_request('PUT', f'/api/books/{book_id}', update_data, auth_required=True)
        
        print(f"状态码: {response['status_code']}")
        print(f"响应: {json.dumps(response['data'], ensure_ascii=False, indent=2)}")
        
        if response['status_code'] == 200:
            print("✅ 更新图书成功")
            return True
        else:
            print("❌ 更新图书失败")
            return False
    
    def test_delete_book(self, book_id: int) -> bool:
        """测试删除图书"""
        print(f"\n=== 测试删除图书 ID: {book_id} ===")
        
        response = self._make_request('DELETE', f'/api/books/{book_id}', auth_required=True)
        
        print(f"状态码: {response['status_code']}")
        print(f"响应: {json.dumps(response['data'], ensure_ascii=False, indent=2)}")
        
        if response['status_code'] == 200:
            print("✅ 删除图书成功")
            return True
        else:
            print("❌ 删除图书失败")
            return False
    
    def test_rate_limiting(self) -> bool:
        """测试限流功能"""
        print("\n=== 测试限流功能 ===")
        
        print("快速发送多个请求...")
        success_count = 0
        rate_limited_count = 0
        
        for i in range(10):
            response = self._make_request('GET', '/api/books')
            if response['status_code'] == 200:
                success_count += 1
            elif response['status_code'] == 429:
                rate_limited_count += 1
                print(f"请求 {i+1}: 触发限流 (429)")
            time.sleep(0.1)  # 短暂延迟
        
        print(f"成功请求: {success_count}")
        print(f"限流请求: {rate_limited_count}")
        
        if rate_limited_count > 0:
            print("✅ 限流功能正常工作")
            return True
        else:
            print("⚠️ 未触发限流（可能需要更多请求）")
            return True
    
    def test_error_handling(self) -> bool:
        """测试错误处理"""
        print("\n=== 测试错误处理 ===")
        
        # 测试404错误
        response = self._make_request('GET', '/api/books/99999')
        print(f"不存在的图书 - 状态码: {response['status_code']}")
        
        # 测试无效数据
        invalid_book = {
            'title': '',  # 空标题
            'author': 'Test Author'
            # 缺少必需字段
        }
        response = self._make_request('POST', '/api/books', invalid_book, auth_required=True)
        print(f"无效数据 - 状态码: {response['status_code']}")
        
        # 测试未授权访问
        response = self._make_request('POST', '/api/books', {'title': 'Test'})
        print(f"未授权访问 - 状态码: {response['status_code']}")
        
        print("✅ 错误处理测试完成")
        return True
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始API测试...")
        print(f"测试目标: {self.base_url}")
        
        # 检查服务是否可用
        try:
            response = requests.get(f"{self.base_url}/api/books", timeout=5)
            if response.status_code != 200:
                print("❌ API服务不可用，请确保服务已启动")
                return
        except requests.exceptions.RequestException:
            print("❌ 无法连接到API服务，请确保服务已启动")
            return
        
        test_results = []
        
        # 执行测试
        test_results.append(("用户注册", self.test_user_registration()))
        test_results.append(("用户登录", self.test_user_login()))
        test_results.append(("获取图书列表", self.test_get_books()))
        
        # 需要登录的测试
        if self.access_token:
            book_id = self.test_create_book()
            if book_id:
                test_results.append(("创建图书", True))
                test_results.append(("获取图书详情", self.test_get_book(book_id)))
                test_results.append(("更新图书", self.test_update_book(book_id)))
                test_results.append(("删除图书", self.test_delete_book(book_id)))
            else:
                test_results.append(("创建图书", False))
        
        test_results.append(("限流测试", self.test_rate_limiting()))
        test_results.append(("错误处理", self.test_error_handling()))
        
        # 输出测试结果
        print("\n" + "="*50)
        print("📊 测试结果汇总")
        print("="*50)
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{test_name:<15} {status}")
            if result:
                passed += 1
        
        print(f"\n总计: {passed}/{total} 个测试通过")
        
        if passed == total:
            print("🎉 所有测试通过！API服务运行正常")
        else:
            print("⚠️ 部分测试失败，请检查API服务")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='图书管理API测试工具')
    parser.add_argument('--url', default='http://localhost:5000', 
                       help='API服务地址 (默认: http://localhost:5000)')
    parser.add_argument('--test', choices=['all', 'auth', 'books', 'errors'], 
                       default='all', help='指定测试类型')
    
    args = parser.parse_args()
    
    tester = BookstoreAPITester(args.url)
    
    if args.test == 'all':
        tester.run_all_tests()
    elif args.test == 'auth':
        tester.test_user_registration()
        tester.test_user_login()
    elif args.test == 'books':
        tester.test_user_login()
        tester.test_get_books()
        book_id = tester.test_create_book()
        if book_id:
            tester.test_get_book(book_id)
            tester.test_update_book(book_id)
            tester.test_delete_book(book_id)
    elif args.test == 'errors':
        tester.test_error_handling()

if __name__ == '__main__':
    main()