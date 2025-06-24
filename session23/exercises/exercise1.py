#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session23 练习1：代码质量检查练习

任务：修复以下代码中的质量问题

请使用以下工具检查并修复代码：
1. ruff check . --fix
2. black .
3. mypy exercise1.py

修复后的代码应该：
- 符合PEP 8规范
- 通过类型检查
- 没有安全问题
- 具有良好的可读性
"""

# TODO: 以下代码包含多个质量问题，请修复它们

import os,sys,json
from typing import *

# 问题1：硬编码敏感信息
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "mysql://admin:password123@localhost/mydb"

# 问题2：不规范的类定义
class userManager:
    def __init__(self,db_url):
        self.db_url=db_url
        self.users=[]
    
    # 问题3：函数过于复杂
    def process_user(self,user_data,action,options=None):
        if action=="create":
            if "name" in user_data and "email" in user_data:
                if len(user_data["name"])>0 and "@" in user_data["email"]:
                    if options and "validate" in options and options["validate"]:
                        if self.validate_email(user_data["email"]):
                            user_id=len(self.users)+1
                            new_user={"id":user_id,"name":user_data["name"],"email":user_data["email"],"status":"active"}
                            self.users.append(new_user)
                            return new_user
                        else:
                            return None
                    else:
                        user_id=len(self.users)+1
                        new_user={"id":user_id,"name":user_data["name"],"email":user_data["email"],"status":"active"}
                        self.users.append(new_user)
                        return new_user
                else:
                    return None
            else:
                return None
        elif action=="update":
            if "id" in user_data:
                for user in self.users:
                    if user["id"]==user_data["id"]:
                        if "name" in user_data:
                            user["name"]=user_data["name"]
                        if "email" in user_data:
                            user["email"]=user_data["email"]
                        return user
                return None
            else:
                return None
        elif action=="delete":
            if "id" in user_data:
                for i,user in enumerate(self.users):
                    if user["id"]==user_data["id"]:
                        deleted_user=self.users.pop(i)
                        return deleted_user
                return None
            else:
                return None
        else:
            return None
    
    # 问题4：缺少类型注解
    def validate_email(self,email):
        import re
        pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern,email) is not None
    
    # 问题5：SQL注入风险
    def find_user_by_name(self,name):
        query=f"SELECT * FROM users WHERE name = '{name}'"
        # 这里应该使用参数化查询
        return query
    
    # 问题6：不安全的文件操作
    def save_users_to_file(self,filename):
        with open(filename,'w') as f:
            json.dump(self.users,f)
    
    def load_users_from_file(self,filename):
        with open(filename,'r') as f:
            self.users=json.load(f)

# 问题7：全局函数缺少类型注解和文档
def calculate_user_stats(users):
    total=len(users)
    active=0
    for user in users:
        if user["status"]=="active":
            active+=1
    return {"total":total,"active":active,"inactive":total-active}

# 问题8：不规范的常量定义
max_users=1000
default_status="active"

# 问题9：主函数缺少异常处理
def main():
    manager=userManager(DATABASE_URL)
    
    # 测试数据
    test_users=[
        {"name":"Alice","email":"alice@example.com"},
        {"name":"Bob","email":"bob@example.com"},
        {"name":"","email":"invalid-email"},
    ]
    
    for user_data in test_users:
        result=manager.process_user(user_data,"create",{"validate":True})
        print(f"创建用户结果: {result}")
    
    stats=calculate_user_stats(manager.users)
    print(f"用户统计: {stats}")
    
    # 保存用户数据
    manager.save_users_to_file("users.json")
    
    print("程序执行完成")

if __name__=="__main__":
    main()

# 练习要求：
# 1. 修复所有PEP 8规范问题
# 2. 添加适当的类型注解
# 3. 修复安全问题
# 4. 重构复杂的函数
# 5. 添加异常处理
# 6. 改善代码结构和可读性
# 7. 添加适当的文档字符串