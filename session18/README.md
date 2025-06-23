# 第18课：数据库集成

## 课程概述

本课程将深入学习Flask与数据库的集成，重点介绍SQLAlchemy ORM的使用。通过本课程，你将学会如何在Web应用中设计和操作数据库，为构建真正的动态Web应用奠定基础。

## 学习目标

通过本课程的学习，你将能够：
- 理解ORM（对象关系映射）的概念和优势
- 掌握SQLAlchemy ORM的基本使用方法
- 学会设计和创建数据模型
- 掌握数据库迁移的概念和实践
- 实现用户注册、登录和会话管理
- 构建一个完整的用户注册登录系统

## 课程内容

### 1. SQLAlchemy ORM介绍
- ORM概念和优势
- SQLAlchemy的特点
- Flask-SQLAlchemy扩展
- 数据库配置

### 2. 数据模型设计
- 模型类定义
- 字段类型和约束
- 表关系（一对一、一对多、多对多）
- 模型方法

### 3. 数据库迁移
- 迁移的概念
- Flask-Migrate扩展
- 创建和应用迁移
- 版本控制

### 4. 项目实战：用户注册登录系统
- 用户模型设计
- 密码加密存储
- 用户注册功能
- 用户登录验证
- 会话管理

## 项目结构

```
session18/
├── README.md           # 本文件
├── tutorial.md         # 详细教程
├── demo.py            # SQLAlchemy基础演示
├── examples/          # 示例代码
│   ├── example1.py    # 基础模型示例
│   ├── example2.py    # 数据关系示例
│   └── example3.py    # 数据操作示例
├── exercises/         # 练习题
│   ├── exercise1.py   # 模型设计练习
│   ├── exercise2.py   # 数据操作练习
│   ├── exercise3.py   # 综合练习
│   └── solutions/     # 参考答案
├── project/           # 用户注册登录系统
│   ├── app.py         # 主应用文件
│   ├── models.py      # 数据模型
│   ├── forms.py       # 表单定义
│   ├── routes.py      # 路由处理
│   ├── templates/     # 模板文件
│   ├── static/        # 静态文件
│   ├── migrations/    # 数据库迁移文件
│   └── README.md      # 项目说明
└── assets/            # 资源文件
    └── database_design.png
```

## 环境准备

```bash
# 安装所需依赖
uv add flask flask-sqlalchemy flask-migrate werkzeug

# 验证安装
uv run python -c "import flask_sqlalchemy; print('SQLAlchemy安装成功')"
```

## 快速开始

```bash
# 运行演示代码
cd session18
uv run python demo.py

# 运行项目
cd project
# 初始化数据库
uv run python -c "from app import db; db.create_all()"
# 启动应用
uv run python app.py
```

## 学习建议

1. **理解ORM概念**：首先理解为什么要使用ORM，它解决了什么问题
2. **从简单开始**：先学会定义简单的模型，再学习复杂的关系
3. **多练习查询**：SQLAlchemy的查询API很强大，需要多练习
4. **注意数据安全**：特别是密码处理和SQL注入防护
5. **理解迁移**：数据库迁移是实际开发中的重要技能

## 参考资源

- [SQLAlchemy官方文档](https://docs.sqlalchemy.org/)
- [Flask-SQLAlchemy文档](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate文档](https://flask-migrate.readthedocs.io/)
- [数据库设计最佳实践](https://en.wikipedia.org/wiki/Database_design) 