#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session23 示例1：PEP 8规范示例

本文件展示了PEP 8编码规范的正确和错误示例，
帮助理解Python代码的标准格式要求。

作者: Python教程团队
创建日期: 2024-01-01
"""

import os
import sys
from typing import Dict, List, Optional, Tuple

# 正确的常量定义
MAX_USERS = 100
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"


class UserManager:
    """
    用户管理器类
    
    负责用户的创建、查询、更新和删除操作。
    遵循PEP 8命名规范和代码格式要求。
    """
    
    def __init__(self, database_url: str):
        """
        初始化用户管理器
        
        Args:
            database_url: 数据库连接URL
        """
        self.database_url = database_url
        self._users: Dict[int, Dict[str, str]] = {}
        self._next_id = 1
    
    def create_user(self, name: str, email: str, age: Optional[int] = None) -> int:
        """
        创建新用户
        
        Args:
            name: 用户姓名
            email: 用户邮箱
            age: 用户年龄（可选）
        
        Returns:
            新创建用户的ID
        
        Raises:
            ValueError: 当用户信息无效时
        """
        if not name or not email:
            raise ValueError("用户姓名和邮箱不能为空")
        
        if '@' not in email:
            raise ValueError("邮箱格式无效")
        
        user_id = self._next_id
        self._users[user_id] = {
            'name': name,
            'email': email,
            'age': str(age) if age is not None else 'Unknown'
        }
        self._next_id += 1
        
        return user_id
    
    def get_user(self, user_id: int) -> Optional[Dict[str, str]]:
        """
        获取用户信息
        
        Args:
            user_id: 用户ID
        
        Returns:
            用户信息字典，如果用户不存在则返回None
        """
        return self._users.get(user_id)
    
    def update_user(self, user_id: int, **kwargs) -> bool:
        """
        更新用户信息
        
        Args:
            user_id: 用户ID
            **kwargs: 要更新的字段
        
        Returns:
            更新是否成功
        """
        if user_id not in self._users:
            return False
        
        for key, value in kwargs.items():
            if key in ['name', 'email', 'age']:
                self._users[user_id][key] = str(value)
        
        return True
    
    def delete_user(self, user_id: int) -> bool:
        """
        删除用户
        
        Args:
            user_id: 用户ID
        
        Returns:
            删除是否成功
        """
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False
    
    def list_users(self) -> List[Tuple[int, Dict[str, str]]]:
        """
        列出所有用户
        
        Returns:
            用户列表，每个元素为(用户ID, 用户信息)的元组
        """
        return [(user_id, user_info) 
                for user_id, user_info in self._users.items()]
    
    def search_users_by_name(self, name_pattern: str) -> List[Dict[str, str]]:
        """
        按姓名搜索用户
        
        Args:
            name_pattern: 姓名模式（支持部分匹配）
        
        Returns:
            匹配的用户列表
        """
        results = []
        for user_info in self._users.values():
            if name_pattern.lower() in user_info['name'].lower():
                results.append(user_info)
        return results


def calculate_user_statistics(users: List[Dict[str, str]]) -> Dict[str, int]:
    """
    计算用户统计信息
    
    Args:
        users: 用户列表
    
    Returns:
        统计信息字典
    """
    stats = {
        'total_users': len(users),
        'users_with_age': 0,
        'average_age': 0
    }
    
    ages = []
    for user in users:
        if user.get('age') and user['age'] != 'Unknown':
            try:
                age = int(user['age'])
                ages.append(age)
                stats['users_with_age'] += 1
            except ValueError:
                continue
    
    if ages:
        stats['average_age'] = sum(ages) // len(ages)
    
    return stats


def format_user_info(user: Dict[str, str]) -> str:
    """
    格式化用户信息为字符串
    
    Args:
        user: 用户信息字典
    
    Returns:
        格式化的用户信息字符串
    """
    name = user.get('name', 'Unknown')
    email = user.get('email', 'Unknown')
    age = user.get('age', 'Unknown')
    
    return f"姓名: {name}, 邮箱: {email}, 年龄: {age}"


def demonstrate_pep8_compliance():
    """
    演示PEP 8规范的正确使用
    """
    print("PEP 8规范演示")
    print("=" * 30)
    
    # 创建用户管理器
    manager = UserManager("sqlite:///users.db")
    
    # 创建用户（正确的函数调用格式）
    user1_id = manager.create_user(
        name="张三",
        email="zhangsan@example.com",
        age=25
    )
    
    user2_id = manager.create_user(
        name="李四",
        email="lisi@example.com"
    )
    
    # 获取用户信息
    user1 = manager.get_user(user1_id)
    user2 = manager.get_user(user2_id)
    
    if user1:
        print(f"用户1: {format_user_info(user1)}")
    
    if user2:
        print(f"用户2: {format_user_info(user2)}")
    
    # 列出所有用户
    all_users = manager.list_users()
    print(f"\n总用户数: {len(all_users)}")
    
    # 计算统计信息
    user_list = [user_info for _, user_info in all_users]
    stats = calculate_user_statistics(user_list)
    
    print(f"统计信息:")
    print(f"  总用户数: {stats['total_users']}")
    print(f"  有年龄信息的用户: {stats['users_with_age']}")
    print(f"  平均年龄: {stats['average_age']}")
    
    # 搜索用户
    search_results = manager.search_users_by_name("张")
    print(f"\n搜索结果 (包含'张'): {len(search_results)}个用户")
    
    # 更新用户信息
    success = manager.update_user(user1_id, age=26)
    print(f"\n更新用户1年龄: {'成功' if success else '失败'}")
    
    # 删除用户
    success = manager.delete_user(user2_id)
    print(f"删除用户2: {'成功' if success else '失败'}")
    
    print(f"\n最终用户数: {len(manager.list_users())}")


# 以下是一些常见的PEP 8违规示例（仅作教学用途）
"""
错误示例1：命名不规范
class userManager:  # 类名应该使用PascalCase
    def getUserInfo(self):  # 方法名应该使用snake_case
        pass

错误示例2：空格使用不当
result=x+y  # 运算符周围应该有空格
function( arg1 , arg2 )  # 函数调用中不应该有多余空格

错误示例3：行太长
very_long_variable_name = some_function_with_very_long_name(argument1, argument2, argument3, argument4, argument5)

错误示例4：导入语句不规范
import os, sys  # 应该分行导入
from module import *  # 避免使用通配符导入

错误示例5：缺少文档字符串
def important_function(x, y):
    return x + y  # 缺少docstring
"""


def main():
    """
    主函数：演示PEP 8规范的正确使用
    """
    print("Session23 示例1：PEP 8规范演示")
    print("=" * 40)
    
    try:
        demonstrate_pep8_compliance()
        
        print("\n=" * 40)
        print("PEP 8规范要点总结:")
        print("1. 使用4个空格进行缩进")
        print("2. 每行不超过79个字符")
        print("3. 类名使用PascalCase")
        print("4. 函数和变量名使用snake_case")
        print("5. 常量使用UPPER_CASE")
        print("6. 运算符周围使用空格")
        print("7. 函数和类之间使用两个空行")
        print("8. 导入语句分组并按字母顺序排列")
        print("9. 为函数和类编写文档字符串")
        print("10. 避免行尾空格和多余的空行")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()