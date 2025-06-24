#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session23 练习1解决方案：代码质量检查练习

这是exercise1.py的修复版本，展示了如何解决各种代码质量问题。

修复的问题包括：
1. PEP 8规范问题
2. 类型注解缺失
3. 安全问题
4. 代码复杂度过高
5. 异常处理缺失
6. 代码结构问题

作者: Python教程团队
创建日期: 2024-01-01
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


# 修复1：使用环境变量替代硬编码敏感信息
API_KEY: Optional[str] = os.getenv("API_KEY")
DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL", "sqlite:///default.db")

# 修复8：规范的常量定义
MAX_USERS: int = 1000
DEFAULT_STATUS: str = "active"
VALID_STATUSES: List[str] = ["active", "inactive", "pending"]


class UserValidationError(Exception):
    """用户验证错误异常"""
    pass


class UserManager:
    """用户管理器类
    
    负责用户的创建、更新、删除和查询操作。
    提供数据验证和安全的数据库操作。
    """
    
    def __init__(self, db_url: str) -> None:
        """
        初始化用户管理器
        
        Args:
            db_url: 数据库连接URL
        """
        self.db_url: str = db_url
        self.users: List[Dict[str, Union[int, str]]] = []
        self._next_user_id: int = 1
    
    def create_user(
        self,
        user_data: Dict[str, str],
        validate: bool = True
    ) -> Dict[str, Union[int, str]]:
        """
        创建新用户
        
        Args:
            user_data: 用户数据字典，包含name和email
            validate: 是否验证邮箱格式
            
        Returns:
            创建的用户字典
            
        Raises:
            UserValidationError: 用户数据验证失败
        """
        if not self._validate_user_data(user_data):
            raise UserValidationError("用户数据验证失败")
        
        if validate and not self.validate_email(user_data["email"]):
            raise UserValidationError("邮箱格式无效")
        
        if len(self.users) >= MAX_USERS:
            raise UserValidationError(f"用户数量已达到上限 {MAX_USERS}")
        
        new_user: Dict[str, Union[int, str]] = {
            "id": self._next_user_id,
            "name": user_data["name"],
            "email": user_data["email"],
            "status": DEFAULT_STATUS
        }
        
        self.users.append(new_user)
        self._next_user_id += 1
        
        return new_user
    
    def update_user(
        self,
        user_id: int,
        user_data: Dict[str, str]
    ) -> Optional[Dict[str, Union[int, str]]]:
        """
        更新用户信息
        
        Args:
            user_id: 用户ID
            user_data: 要更新的用户数据
            
        Returns:
            更新后的用户字典，如果用户不存在则返回None
        """
        user = self._find_user_by_id(user_id)
        if user is None:
            return None
        
        # 更新允许的字段
        updatable_fields = ["name", "email", "status"]
        for field in updatable_fields:
            if field in user_data:
                if field == "email" and not self.validate_email(user_data[field]):
                    raise UserValidationError(f"无效的邮箱格式: {user_data[field]}")
                if field == "status" and user_data[field] not in VALID_STATUSES:
                    raise UserValidationError(f"无效的状态: {user_data[field]}")
                user[field] = user_data[field]
        
        return user
    
    def delete_user(self, user_id: int) -> Optional[Dict[str, Union[int, str]]]:
        """
        删除用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            被删除的用户字典，如果用户不存在则返回None
        """
        for i, user in enumerate(self.users):
            if user["id"] == user_id:
                return self.users.pop(i)
        return None
    
    def process_user(
        self,
        user_data: Dict[str, Union[int, str]],
        action: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Union[int, str]]]:
        """
        处理用户操作（保持向后兼容）
        
        Args:
            user_data: 用户数据
            action: 操作类型（create, update, delete）
            options: 操作选项
            
        Returns:
            操作结果
        """
        if options is None:
            options = {}
        
        try:
            if action == "create":
                validate = options.get("validate", True)
                return self.create_user(user_data, validate)
            elif action == "update":
                user_id = user_data.get("id")
                if user_id is None:
                    raise UserValidationError("更新操作需要用户ID")
                return self.update_user(int(user_id), user_data)
            elif action == "delete":
                user_id = user_data.get("id")
                if user_id is None:
                    raise UserValidationError("删除操作需要用户ID")
                return self.delete_user(int(user_id))
            else:
                raise UserValidationError(f"不支持的操作: {action}")
        except (ValueError, TypeError) as e:
            raise UserValidationError(f"数据类型错误: {e}") from e
    
    def validate_email(self, email: str) -> bool:
        """
        验证邮箱格式
        
        Args:
            email: 邮箱地址
            
        Returns:
            邮箱格式是否有效
        """
        if not email or not isinstance(email, str):
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def find_user_by_name_safe(self, name: str) -> str:
        """
        安全的按姓名查找用户的SQL查询
        
        Args:
            name: 用户姓名
            
        Returns:
            参数化的SQL查询字符串
        """
        # 修复5：使用参数化查询防止SQL注入
        query = "SELECT * FROM users WHERE name = ?"
        # 在实际应用中，应该返回查询结果而不是查询字符串
        # 这里为了演示目的返回查询字符串
        return f"Query: {query}, Parameter: {name}"
    
    def save_users_to_file(self, filename: str) -> None:
        """
        安全地保存用户数据到文件
        
        Args:
            filename: 文件名
            
        Raises:
            OSError: 文件操作失败
        """
        # 修复6：安全的文件操作
        file_path = Path(filename)
        
        # 确保目录存在
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 验证文件路径安全性
        if not self._is_safe_path(file_path):
            raise ValueError(f"不安全的文件路径: {filename}")
        
        try:
            with file_path.open('w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
        except (OSError, json.JSONEncodeError) as e:
            raise OSError(f"保存文件失败: {e}") from e
    
    def load_users_from_file(self, filename: str) -> None:
        """
        安全地从文件加载用户数据
        
        Args:
            filename: 文件名
            
        Raises:
            OSError: 文件操作失败
            ValueError: 数据格式错误
        """
        file_path = Path(filename)
        
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {filename}")
        
        if not self._is_safe_path(file_path):
            raise ValueError(f"不安全的文件路径: {filename}")
        
        try:
            with file_path.open('r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 验证加载的数据格式
            if not isinstance(data, list):
                raise ValueError("文件格式错误：期望用户列表")
            
            # 验证每个用户数据
            for user in data:
                if not self._validate_loaded_user(user):
                    raise ValueError(f"无效的用户数据: {user}")
            
            self.users = data
            # 更新下一个用户ID
            if self.users:
                max_id = max(user["id"] for user in self.users if isinstance(user.get("id"), int))
                self._next_user_id = max_id + 1
                
        except (OSError, json.JSONDecodeError) as e:
            raise OSError(f"加载文件失败: {e}") from e
    
    def _validate_user_data(self, user_data: Dict[str, str]) -> bool:
        """
        验证用户数据
        
        Args:
            user_data: 用户数据字典
            
        Returns:
            数据是否有效
        """
        required_fields = ["name", "email"]
        
        for field in required_fields:
            if field not in user_data:
                return False
            if not isinstance(user_data[field], str) or not user_data[field].strip():
                return False
        
        return True
    
    def _validate_loaded_user(self, user: Any) -> bool:
        """
        验证从文件加载的用户数据
        
        Args:
            user: 用户数据
            
        Returns:
            数据是否有效
        """
        if not isinstance(user, dict):
            return False
        
        required_fields = {"id": int, "name": str, "email": str, "status": str}
        
        for field, expected_type in required_fields.items():
            if field not in user or not isinstance(user[field], expected_type):
                return False
        
        return True
    
    def _find_user_by_id(self, user_id: int) -> Optional[Dict[str, Union[int, str]]]:
        """
        根据ID查找用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户字典或None
        """
        for user in self.users:
            if user["id"] == user_id:
                return user
        return None
    
    def _is_safe_path(self, file_path: Path) -> bool:
        """
        检查文件路径是否安全
        
        Args:
            file_path: 文件路径
            
        Returns:
            路径是否安全
        """
        try:
            # 解析绝对路径
            resolved_path = file_path.resolve()
            
            # 检查是否在当前工作目录或其子目录中
            current_dir = Path.cwd().resolve()
            return str(resolved_path).startswith(str(current_dir))
        except (OSError, ValueError):
            return False


def calculate_user_stats(users: List[Dict[str, Union[int, str]]]) -> Dict[str, int]:
    """
    计算用户统计信息
    
    Args:
        users: 用户列表
        
    Returns:
        包含统计信息的字典
    """
    if not users:
        return {"total": 0, "active": 0, "inactive": 0}
    
    total = len(users)
    active = sum(1 for user in users if user.get("status") == "active")
    
    return {
        "total": total,
        "active": active,
        "inactive": total - active
    }


def main() -> None:
    """
    主函数：演示用户管理器的使用
    
    包含完整的异常处理和错误报告。
    """
    print("Session23 练习1解决方案：用户管理系统")
    print("=" * 50)
    
    try:
        # 检查必要的环境变量
        if not DATABASE_URL:
            print("警告: 未设置DATABASE_URL环境变量，使用默认值")
        
        # 创建用户管理器
        manager = UserManager(DATABASE_URL or "sqlite:///default.db")
        
        # 测试数据
        test_users = [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "email": "bob@example.com"},
            {"name": "Charlie", "email": "charlie@example.com"},
            {"name": "", "email": "invalid-email"},  # 无效数据
        ]
        
        print("\n创建用户测试:")
        print("-" * 20)
        
        created_users = []
        for i, user_data in enumerate(test_users, 1):
            try:
                result = manager.process_user(user_data, "create", {"validate": True})
                print(f"用户 {i}: 创建成功 - {result}")
                created_users.append(result)
            except UserValidationError as e:
                print(f"用户 {i}: 创建失败 - {e}")
        
        # 更新用户测试
        if created_users:
            print("\n更新用户测试:")
            print("-" * 20)
            
            try:
                first_user = created_users[0]
                update_data = {
                    "id": first_user["id"],
                    "name": "Alice Updated",
                    "status": "inactive"
                }
                updated_user = manager.process_user(update_data, "update")
                print(f"更新成功: {updated_user}")
            except UserValidationError as e:
                print(f"更新失败: {e}")
        
        # 统计信息
        print("\n用户统计:")
        print("-" * 20)
        stats = calculate_user_stats(manager.users)
        for key, value in stats.items():
            print(f"{key}: {value}")
        
        # 文件操作测试
        print("\n文件操作测试:")
        print("-" * 20)
        
        try:
            filename = "users_backup.json"
            manager.save_users_to_file(filename)
            print(f"用户数据已保存到 {filename}")
            
            # 创建新的管理器实例并加载数据
            new_manager = UserManager(DATABASE_URL or "sqlite:///default.db")
            new_manager.load_users_from_file(filename)
            print(f"从 {filename} 加载了 {len(new_manager.users)} 个用户")
            
        except (OSError, ValueError) as e:
            print(f"文件操作失败: {e}")
        
        # 安全查询演示
        print("\n安全查询演示:")
        print("-" * 20)
        safe_query = manager.find_user_by_name_safe("Alice")
        print(safe_query)
        
        print("\n程序执行完成")
        
    except Exception as e:
        print(f"程序执行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()