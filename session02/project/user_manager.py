#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户管理模块

负责用户数据的存储、管理和操作。
这个模块展示了如何使用Python的基本数据类型来管理复杂的数据结构。

作者: Python教程团队
创建日期: 2024-12-19
"""

from typing import List, Dict, Any, Optional
from utils import calculate_bmi, get_age_group


class UserManager:
    """
    用户管理器类
    
    负责管理所有用户信息，包括添加、删除、查询和统计功能。
    """
    
    def __init__(self):
        """
        初始化用户管理器
        """
        # 使用列表存储所有用户信息
        self._users: List[Dict[str, Any]] = []
        
        # 用户计数器
        self._user_count: int = 0
        
        # 添加一些示例数据（可选）
        self._add_sample_data()
    
    def _add_sample_data(self):
        """
        添加示例数据（用于演示）
        """
        sample_users = [
            {
                'name': '张三',
                'age': 25,
                'height': 1.75,
                'weight': 70.0,
                'is_student': False,
                'phone': '13800138000',
                'email': 'zhangsan@example.com'
            },
            {
                'name': '李四',
                'age': 20,
                'height': 1.68,
                'weight': 55.5,
                'is_student': True,
                'phone': '13900139000',
                'email': 'lisi@student.edu.cn'
            },
            {
                'name': 'Alice',
                'age': 28,
                'height': 1.65,
                'weight': 58.0,
                'is_student': False,
                'phone': '15800158000',
                'email': 'alice@company.com'
            }
        ]
        
        # 注释掉下面这行如果不想要示例数据
        # for user in sample_users:
        #     self.add_user(user)
    
    def add_user(self, user_info: Dict[str, Any]) -> bool:
        """
        添加新用户
        
        Args:
            user_info (Dict[str, Any]): 用户信息字典
            
        Returns:
            bool: 添加是否成功
        """
        try:
            # 验证用户信息
            if not self._validate_user_info(user_info):
                return False
            
            # 添加用户ID和创建时间戳
            user_info['id'] = self._user_count + 1
            user_info['created_at'] = self._get_current_timestamp()
            
            # 计算衍生信息
            user_info['bmi'] = calculate_bmi(user_info['weight'], user_info['height'])
            user_info['age_group'] = get_age_group(user_info['age'])
            
            # 添加到用户列表
            self._users.append(user_info.copy())
            self._user_count += 1
            
            return True
            
        except Exception as e:
            print(f"添加用户失败: {e}")
            return False
    
    def _validate_user_info(self, user_info: Dict[str, Any]) -> bool:
        """
        验证用户信息的有效性
        
        Args:
            user_info (Dict[str, Any]): 用户信息字典
            
        Returns:
            bool: 验证是否通过
        """
        required_fields = ['name', 'age', 'height', 'weight', 'is_student', 'phone', 'email']
        
        # 检查必需字段
        for field in required_fields:
            if field not in user_info:
                print(f"缺少必需字段: {field}")
                return False
        
        # 检查数据类型和范围
        if not isinstance(user_info['name'], str) or len(user_info['name'].strip()) == 0:
            print("姓名必须是非空字符串")
            return False
        
        if not isinstance(user_info['age'], int) or not (0 < user_info['age'] < 150):
            print("年龄必须是1-149之间的整数")
            return False
        
        if not isinstance(user_info['height'], (int, float)) or not (0.5 < user_info['height'] < 3.0):
            print("身高必须是0.5-3.0米之间的数字")
            return False
        
        if not isinstance(user_info['weight'], (int, float)) or not (10 < user_info['weight'] < 500):
            print("体重必须是10-500公斤之间的数字")
            return False
        
        if not isinstance(user_info['is_student'], bool):
            print("学生状态必须是布尔值")
            return False
        
        if not isinstance(user_info['phone'], str) or len(user_info['phone'].strip()) < 8:
            print("电话号码必须是至少8位的字符串")
            return False
        
        if not isinstance(user_info['email'], str) or '@' not in user_info['email']:
            print("邮箱地址格式不正确")
            return False
        
        # 检查姓名是否重复
        if self._is_name_exists(user_info['name']):
            print(f"用户名 '{user_info['name']}' 已存在")
            return False
        
        return True
    
    def _is_name_exists(self, name: str) -> bool:
        """
        检查姓名是否已存在
        
        Args:
            name (str): 要检查的姓名
            
        Returns:
            bool: 姓名是否已存在
        """
        return any(user['name'].lower() == name.lower() for user in self._users)
    
    def _get_current_timestamp(self) -> str:
        """
        获取当前时间戳（简化版本）
        
        Returns:
            str: 时间戳字符串
        """
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        获取所有用户信息
        
        Returns:
            List[Dict[str, Any]]: 用户信息列表
        """
        return self._users.copy()
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        根据ID获取用户信息
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            Optional[Dict[str, Any]]: 用户信息，如果不存在则返回None
        """
        for user in self._users:
            if user.get('id') == user_id:
                return user.copy()
        return None
    
    def get_user_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        根据姓名获取用户信息
        
        Args:
            name (str): 用户姓名
            
        Returns:
            Optional[Dict[str, Any]]: 用户信息，如果不存在则返回None
        """
        for user in self._users:
            if user['name'].lower() == name.lower():
                return user.copy()
        return None
    
    def search_users(self, **criteria) -> List[Dict[str, Any]]:
        """
        根据条件搜索用户
        
        Args:
            **criteria: 搜索条件
            
        Returns:
            List[Dict[str, Any]]: 匹配的用户列表
        """
        results = []
        
        for user in self._users:
            match = True
            
            for key, value in criteria.items():
                if key not in user:
                    match = False
                    break
                
                if key == 'name':
                    # 姓名支持部分匹配
                    if value.lower() not in user[key].lower():
                        match = False
                        break
                elif key in ['age', 'height', 'weight', 'bmi']:
                    # 数值类型支持范围匹配
                    if isinstance(value, tuple) and len(value) == 2:
                        min_val, max_val = value
                        if not (min_val <= user[key] <= max_val):
                            match = False
                            break
                    else:
                        if user[key] != value:
                            match = False
                            break
                else:
                    # 其他字段精确匹配
                    if user[key] != value:
                        match = False
                        break
            
            if match:
                results.append(user.copy())
        
        return results
    
    def update_user(self, user_id: int, updates: Dict[str, Any]) -> bool:
        """
        更新用户信息
        
        Args:
            user_id (int): 用户ID
            updates (Dict[str, Any]): 要更新的字段
            
        Returns:
            bool: 更新是否成功
        """
        for i, user in enumerate(self._users):
            if user.get('id') == user_id:
                # 创建临时用户信息进行验证
                temp_user = user.copy()
                temp_user.update(updates)
                
                # 验证更新后的信息
                if self._validate_user_info(temp_user):
                    # 更新用户信息
                    self._users[i].update(updates)
                    
                    # 重新计算衍生信息
                    if 'weight' in updates or 'height' in updates:
                        self._users[i]['bmi'] = calculate_bmi(
                            self._users[i]['weight'], 
                            self._users[i]['height']
                        )
                    
                    if 'age' in updates:
                        self._users[i]['age_group'] = get_age_group(self._users[i]['age'])
                    
                    return True
                else:
                    return False
        
        return False
    
    def delete_user(self, user_id: int) -> bool:
        """
        删除用户
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            bool: 删除是否成功
        """
        for i, user in enumerate(self._users):
            if user.get('id') == user_id:
                del self._users[i]
                return True
        return False
    
    def get_user_count(self) -> int:
        """
        获取用户总数
        
        Returns:
            int: 用户总数
        """
        return len(self._users)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取用户统计信息
        
        Returns:
            Dict[str, Any]: 统计信息字典
        """
        if not self._users:
            return {}
        
        # 基本统计
        total_users = len(self._users)
        
        # 年龄统计
        ages = [user['age'] for user in self._users]
        age_stats = {
            'total': total_users,
            'avg_age': sum(ages) / len(ages),
            'min_age': min(ages),
            'max_age': max(ages)
        }
        
        # 身高体重统计
        heights = [user['height'] for user in self._users]
        weights = [user['weight'] for user in self._users]
        
        physical_stats = {
            'avg_height': sum(heights) / len(heights),
            'min_height': min(heights),
            'max_height': max(heights),
            'avg_weight': sum(weights) / len(weights),
            'min_weight': min(weights),
            'max_weight': max(weights)
        }
        
        # 学生统计
        students = [user for user in self._users if user['is_student']]
        student_stats = {
            'student_count': len(students),
            'non_student_count': total_users - len(students),
            'student_percentage': (len(students) / total_users) * 100
        }
        
        # BMI统计
        bmis = [user['bmi'] for user in self._users]
        bmi_stats = {
            'avg_bmi': sum(bmis) / len(bmis),
            'min_bmi': min(bmis),
            'max_bmi': max(bmis)
        }
        
        # 年龄组统计
        age_groups = {}
        for user in self._users:
            group = user['age_group']
            age_groups[group] = age_groups.get(group, 0) + 1
        
        return {
            'age_stats': age_stats,
            'physical_stats': physical_stats,
            'student_stats': student_stats,
            'bmi_stats': bmi_stats,
            'age_groups': age_groups
        }
    
    def export_users_data(self) -> str:
        """
        导出用户数据为字符串格式
        
        Returns:
            str: 格式化的用户数据
        """
        if not self._users:
            return "暂无用户数据"
        
        lines = []
        lines.append("用户信息导出")
        lines.append("=" * 50)
        lines.append(f"导出时间: {self._get_current_timestamp()}")
        lines.append(f"用户总数: {len(self._users)}")
        lines.append("=" * 50)
        
        for i, user in enumerate(self._users, 1):
            lines.append(f"\n{i}. {user['name']}")
            lines.append(f"   ID: {user.get('id', 'N/A')}")
            lines.append(f"   年龄: {user['age']}岁 ({user['age_group']})")
            lines.append(f"   身高: {user['height']:.2f}米")
            lines.append(f"   体重: {user['weight']:.1f}公斤")
            lines.append(f"   BMI: {user['bmi']:.1f}")
            lines.append(f"   类型: {'学生' if user['is_student'] else '非学生'}")
            lines.append(f"   电话: {user['phone']}")
            lines.append(f"   邮箱: {user['email']}")
            lines.append(f"   创建时间: {user.get('created_at', 'N/A')}")
        
        return "\n".join(lines)
    
    def clear_all_users(self) -> bool:
        """
        清空所有用户数据
        
        Returns:
            bool: 操作是否成功
        """
        try:
            self._users.clear()
            self._user_count = 0
            return True
        except Exception:
            return False
    
    def __str__(self) -> str:
        """
        字符串表示
        
        Returns:
            str: 用户管理器的字符串描述
        """
        return f"UserManager(users={len(self._users)}, total_created={self._user_count})"
    
    def __len__(self) -> int:
        """
        返回用户数量
        
        Returns:
            int: 用户数量
        """
        return len(self._users)