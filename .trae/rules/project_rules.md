# Python新手教程项目规则

## 项目概述

本项目是一个完整的Python教学体系，包含30个session（课程），旨在帮助新手从零基础成长为能够独立负责项目的Python开发者。

## 项目结构规范

### 根目录结构

```
python-rookie/
├── session01/              # 第1课：环境搭建与Hello World
├── session02/              # 第2课：变量与数据类型
├── session03/              # 第3课：运算符与表达式
├── ...
├── session30/              # 第30课：综合项目实战
├── projects/               # 项目实战目录
├── resources/              # 学习资源
├── tests/                  # 测试代码
├── docs/                   # 文档
├── README.md               # 项目说明
├── requirements.txt        # 依赖管理
└── .gitignore             # Git忽略文件
```

### Session目录结构

每个session目录必须包含以下标准结构：

```
sessionXX/
├── README.md               # 课程概述和学习目标
├── tutorial.md             # 详细教程文档
├── demo.py                 # 主要演示代码
├── examples/               # 示例代码目录
│   ├── example1.py
│   ├── example2.py
│   └── ...
├── exercises/              # 练习题目录
│   ├── exercise1.py
│   ├── exercise2.py
│   ├── solutions/          # 练习答案
│   │   ├── exercise1_solution.py
│   │   └── exercise2_solution.py
│   └── README.md           # 练习说明
├── project/                # 本课演示项目
│   ├── main.py             # 项目主文件
│   ├── requirements.txt    # 项目依赖（如需要）
│   └── README.md           # 项目说明
└── assets/                 # 资源文件（图片、数据等）
    ├── images/
    ├── data/
    └── ...
```

## 命名规范

### 文件命名

1. **Session目录**：`sessionXX`（XX为两位数字，如session01, session02）
2. **Python文件**：使用小写字母和下划线，如`demo.py`, `student_manager.py`
3. **Markdown文件**：使用小写字母，如`tutorial.md`, `readme.md`
4. **项目目录**：使用小写字母和下划线，如`calculator_app`, `blog_system`

### 变量和函数命名

1. **变量名**：使用小写字母和下划线（snake_case），如`user_name`, `total_score`
2. **函数名**：使用小写字母和下划线（snake_case），如`calculate_bmi()`, `get_user_info()`
3. **类名**：使用大驼峰命名（PascalCase），如`StudentManager`, `BankAccount`
4. **常量**：使用大写字母和下划线，如`MAX_SCORE`, `DEFAULT_PORT`

## 内容规范

### README.md（Session级别）

每个session的README.md必须包含：

```markdown
# SessionXX: 课程标题

## 学习目标
- 目标1
- 目标2
- 目标3

## 课程内容
- 知识点1
- 知识点2
- 知识点3

## 演示项目
项目名称和简要描述

## 前置知识
需要掌握的前置知识点

## 学习时间
预计学习时间：X小时

## 文件说明
- `tutorial.md` - 详细教程
- `demo.py` - 主要演示代码
- `examples/` - 示例代码
- `exercises/` - 练习题
- `project/` - 演示项目
```

### tutorial.md规范

教程文档必须包含：

1. **理论讲解**：清晰的概念解释
2. **代码示例**：每个概念都要有对应的代码示例
3. **运行结果**：展示代码的执行结果
4. **注意事项**：常见错误和注意点
5. **扩展阅读**：相关资源链接

### 代码规范

1. **注释规范**：
   - 文件头部必须包含文件说明、作者、创建日期
   - 函数必须有docstring说明
   - 复杂逻辑必须有行内注释

2. **代码风格**：
   - 遵循PEP 8规范
   - 每行代码不超过79字符
   - 函数和类之间空两行
   - 导入语句按标准库、第三方库、本地模块分组

3. **示例代码模板**：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SessionXX: 课程标题 - 演示代码

本文件演示了XXX的基本用法和实际应用。

作者: Python教程团队
创建日期: YYYY-MM-DD
最后修改: YYYY-MM-DD
"""

import sys
import os
from typing import List, Dict, Optional


def main():
    """
    主函数：演示程序的入口点
    """
    print("SessionXX: 课程标题演示")
    print("=" * 40)
    
    # 演示代码
    demo_function()
    
    print("\n演示完成！")


def demo_function():
    """
    演示函数：展示本课的核心概念
    """
    # 具体实现
    pass


if __name__ == "__main__":
    main()
```

## Session内容分配

### 第一阶段：Python基础入门（Session 1-6）

- **Session01**: 环境搭建与Hello World
- **Session02**: 变量与数据类型
- **Session03**: 运算符与表达式
- **Session04**: 控制流程
- **Session05**: 数据结构基础
- **Session06**: 函数编程

### 第二阶段：进阶编程技能（Session 7-11）

- **Session07**: 文件操作
- **Session08**: 面向对象编程基础
- **Session09**: 面向对象进阶
- **Session10**: 模块与包
- **Session11**: 错误处理与调试

### 第三阶段：实用库与工具（Session 12-16）

- **Session12**: 数据处理 - NumPy
- **Session13**: 数据分析 - Pandas
- **Session14**: 网络编程
- **Session15**: 数据库操作
- **Session16**: GUI编程 - Tkinter

### 第四阶段：Web开发基础（Session 17-20）

- **Session17**: Web开发入门 - Flask
- **Session18**: 数据库集成
- **Session19**: 前端集成
- **Session20**: API开发

### 第五阶段：项目实战与工程化（Session 21-25）

- **Session21**: 版本控制 - Git
- **Session22**: 测试驱动开发
- **Session23**: 代码质量与规范
- **Session24**: 性能优化
- **Session25**: 部署与运维

### 第六阶段：综合项目实战（Session 26-30）

- **Session26**: 项目需求分析与设计
- **Session27**: 项目架构设计
- **Session28**: 模块化开发实践
- **Session29**: 项目测试与调试
- **Session30**: 项目部署与维护

## 演示项目规范

每个session的演示项目必须：

1. **可运行性**：代码必须能够直接运行，无语法错误
2. **教学性**：突出本课的核心知识点
3. **实用性**：解决实际问题，有实用价值
4. **渐进性**：难度逐步递增，与前面课程衔接
5. **完整性**：包含完整的功能和错误处理

### 项目复杂度指导

- **Session 1-6**: 简单脚本（50-100行代码）
- **Session 7-11**: 中等复杂度（100-200行代码）
- **Session 12-16**: 功能完整的小工具（200-300行代码）
- **Session 17-20**: Web应用原型（300-500行代码）
- **Session 21-25**: 工程化项目（500-800行代码）
- **Session 26-30**: 完整商业项目（1000+行代码）

## 练习题规范

每个session必须包含3-5个练习题：

1. **基础练习**：巩固基本概念（1-2题）
2. **应用练习**：实际应用场景（1-2题）
3. **挑战练习**：拓展思维（1题）

练习题格式：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SessionXX 练习题X：题目标题

题目描述：
详细的题目要求和说明

输入示例：
输入格式说明

输出示例：
期望的输出格式

提示：
- 提示1
- 提示2
"""

# 在这里编写你的代码

def solution():
    """
    在这里实现你的解决方案
    """
    pass


if __name__ == "__main__":
    solution()
```

## 质量控制

### 代码审查清单

- [ ] 代码能够正常运行
- [ ] 遵循PEP 8编码规范
- [ ] 包含适当的注释和文档
- [ ] 错误处理完善
- [ ] 变量和函数命名规范
- [ ] 没有硬编码的魔法数字
- [ ] 代码结构清晰，逻辑合理

### 文档审查清单

- [ ] 教程内容准确无误
- [ ] 代码示例与教程内容匹配
- [ ] 包含运行结果展示
- [ ] 语言表达清晰易懂
- [ ] 格式规范统一
- [ ] 链接有效可访问

## 版本控制规范

### 提交信息格式

```
[SessionXX] 简短描述

详细说明（可选）

- 变更点1
- 变更点2
```

### 分支管理

- `main`: 主分支，稳定版本
- `develop`: 开发分支
- `session/XX`: 单个session开发分支
- `feature/功能名`: 特性开发分支

## 依赖管理

本项目使用 **uv** 作为依赖管理工具，Python版本为 **3.11.12**。

### pyproject.toml规范

```toml
[project]
name = "python-rookie"
version = "1.0.0"
description = "Python新手到项目负责人完整教程"
requires-python = ">=3.11.12"
dependencies = [
    # 基础依赖
    "numpy>=1.21.0",
    "pandas>=1.3.0",
    "matplotlib>=3.4.0",
    # Web开发
    "flask>=2.0.0",
    "requests>=2.25.0",
    # 数据库
    "sqlalchemy>=1.4.0",
]

[project.optional-dependencies]
dev = [
    # 测试
    "pytest>=6.2.0",
    "pytest-cov>=2.12.0",
    # 代码质量
    "flake8>=3.9.0",
    "black>=21.6.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
python = "3.11.12"
```

### 虚拟环境和依赖安装

使用uv管理项目环境和依赖：

```bash
# 安装uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh
# 或者在Windows上
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 创建项目并指定Python版本
uv init --python 3.11.12

# 安装项目依赖
uv sync

# 安装开发依赖
uv sync --extra dev

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 添加新依赖
uv add package_name

# 添加开发依赖
uv add --dev package_name

# 运行Python脚本
uv run python script.py

# 运行测试
uv run pytest
```

### uv的优势

1. **极快的依赖解析和安装速度**：比pip快10-100倍
2. **内置虚拟环境管理**：自动创建和管理.venv目录
3. **锁文件支持**：自动生成uv.lock确保依赖版本一致性
4. **Python版本管理**：可以自动下载和管理Python版本
5. **兼容pip**：支持现有的requirements.txt文件

## 测试规范

### 测试文件命名

- 测试文件以`test_`开头
- 测试函数以`test_`开头
- 测试类以`Test`开头

### 测试覆盖率

- 核心功能测试覆盖率应达到80%以上
- 关键算法和业务逻辑必须有测试
- 边界条件和异常情况必须测试

## 文档维护

### 更新频率

- 代码变更时同步更新文档
- 每月检查一次外部链接有效性
- 每季度审查一次内容准确性

### 反馈收集

- 在每个session的README中提供反馈渠道
- 定期收集学习者反馈
- 根据反馈持续改进内容

---

**注意**：本规则文档是活文档，会根据项目发展和反馈持续更新。所有贡献者都应该遵循这些规范，确保项目的一致性和质量。