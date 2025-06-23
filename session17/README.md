# 第17课：Web开发入门 - Flask

## 课程概述

本课程将带你进入Web开发的世界，学习使用Flask框架构建Web应用。Flask是一个轻量级的Python Web框架，以其简洁和灵活性著称，非常适合初学者入门Web开发。

## 学习目标

通过本课程的学习，你将能够：
- 理解Web开发的基本概念（HTTP、请求/响应、路由等）
- 掌握Flask框架的基本使用方法
- 学会创建路由和视图函数
- 掌握Jinja2模板引擎的使用
- 能够构建一个完整的个人博客系统

## 课程内容

### 1. Flask框架介绍
- 什么是Web框架
- Flask的特点和优势
- Flask vs Django
- 安装和环境配置

### 2. 路由与视图
- 路由的概念
- 创建基本路由
- 动态路由
- HTTP方法处理

### 3. 模板引擎
- Jinja2模板语法
- 模板继承
- 变量传递
- 控制结构

### 4. 项目实战：个人博客系统
- 项目架构设计
- 路由规划
- 模板设计
- 数据管理

## 项目结构

```
session17/
├── README.md           # 本文件
├── tutorial.md         # 详细教程
├── demo.py            # Flask基础演示
├── examples/          # 示例代码
│   ├── example1.py    # 基础路由示例
│   ├── example2.py    # 模板使用示例
│   └── example3.py    # 表单处理示例
├── exercises/         # 练习题
│   ├── exercise1.py   # 路由练习
│   ├── exercise2.py   # 模板练习
│   ├── exercise3.py   # 综合练习
│   └── solutions/     # 参考答案
├── project/           # 个人博客项目
│   ├── app.py         # 主应用文件
│   ├── templates/     # 模板文件
│   ├── static/        # 静态文件
│   └── README.md      # 项目说明
└── assets/            # 资源文件
    └── flask_architecture.png
```

## 环境准备

```bash
# 安装Flask
uv add flask

# 验证安装
uv run python -c "import flask; print(flask.__version__)"
```

## 快速开始

```bash
# 运行演示代码
cd session17
uv run python demo.py

# 运行项目
cd project
uv run python app.py
```

## 学习建议

1. **理解Web基础**：在开始之前，了解HTTP协议的基本概念
2. **动手实践**：跟随教程编写每一行代码
3. **调试技巧**：学会使用Flask的调试模式
4. **扩展学习**：尝试修改和扩展示例代码

## 参考资源

- [Flask官方文档](https://flask.palletsprojects.com/)
- [Jinja2模板文档](https://jinja.palletsprojects.com/)
- [MDN Web文档](https://developer.mozilla.org/zh-CN/) 