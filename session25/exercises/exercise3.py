#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session25 练习题3：部署配置生成

题目描述：
编写一个Python脚本，自动为Flask应用生成部署所需的配置文件，包括：
1. Gunicorn配置文件
2. Nginx配置文件
3. systemd服务文件
4. 部署说明文档

脚本应根据用户输入的参数（如应用名称、端口、工作进程数等）生成这些配置文件，并提供部署步骤说明。

输入示例：
应用名称：myapp
应用路径：/var/www/myapp
域名：example.com
端口：8000
工作进程数：4

输出示例：
✅ Gunicorn配置文件已生成：/var/www/myapp/gunicorn.conf.py
✅ Nginx配置文件已生成：/var/www/myapp/nginx.conf
✅ systemd服务文件已生成：/var/www/myapp/myapp.service
✅ 部署说明文档已生成：/var/www/myapp/DEPLOYMENT.md

提示：
- 使用模板字符串生成配置文件
- 考虑不同操作系统的路径差异
- 添加适当的注释说明每个配置项的作用
- 提供完整的部署步骤说明
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional


def generate_gunicorn_config(app_path: str, app_name: str, port: int, workers: int) -> str:
    """
    生成Gunicorn配置文件
    
    Args:
        app_path: 应用路径
        app_name: 应用名称
        port: 端口号
        workers: 工作进程数
    
    Returns:
        str: 配置文件内容
    """
    # 在这里实现你的代码
    pass


def generate_nginx_config(app_name: str, domain: str, port: int, static_path: Optional[str] = None) -> str:
    """
    生成Nginx配置文件
    
    Args:
        app_name: 应用名称
        domain: 域名
        port: 应用端口号
        static_path: 静态文件路径，如果为None则使用默认路径
    
    Returns:
        str: 配置文件内容
    """
    # 在这里实现你的代码
    pass


def generate_systemd_service(app_path: str, app_name: str, user: str = "www-data") -> str:
    """
    生成systemd服务文件
    
    Args:
        app_path: 应用路径
        app_name: 应用名称
        user: 运行服务的用户
    
    Returns:
        str: 配置文件内容
    """
    # 在这里实现你的代码
    pass


def generate_deployment_guide(app_path: str, app_name: str, domain: str) -> str:
    """
    生成部署说明文档
    
    Args:
        app_path: 应用路径
        app_name: 应用名称
        domain: 域名
    
    Returns:
        str: 文档内容
    """
    # 在这里实现你的代码
    pass


def write_file(file_path: str, content: str) -> bool:
    """
    将内容写入文件
    
    Args:
        file_path: 文件路径
        content: 文件内容
    
    Returns:
        bool: 写入成功返回True，失败返回False
    """
    # 在这里实现你的代码
    pass


def get_user_input() -> Dict[str, str]:
    """
    获取用户输入的部署参数
    
    Returns:
        Dict[str, str]: 用户输入的参数
    """
    # 在这里实现你的代码
    pass


def main():
    """
    主函数：执行部署配置生成任务
    """
    print("Session25 练习题3：部署配置生成")
    print("=" * 40)
    
    # 获取用户输入
    # 在实际练习中，你可以使用get_user_input()函数获取用户输入
    # 这里为了演示，使用硬编码的参数
    params = {
        "app_name": "myapp",
        "app_path": "/var/www/myapp",
        "domain": "example.com",
        "port": 8000,
        "workers": 4,
        "user": "www-data",
        "static_path": "/var/www/myapp/static"
    }
    
    # 在这里实现主要逻辑
    # 1. 生成Gunicorn配置
    # 2. 生成Nginx配置
    # 3. 生成systemd服务文件
    # 4. 生成部署说明文档
    # 5. 将配置写入文件
    
    pass


if __name__ == "__main__":
    main()