# 代码质量检查器项目

这是Session23的演示项目，展示了一个完整的代码质量检查工具的实现。

## 项目概述

代码质量检查器是一个集成多种Python代码质量工具的命令行应用程序，它可以：

- 运行多种代码质量检查工具（Ruff、Black、MyPy、Bandit）
- 生成详细的质量报告
- 提供代码改进建议
- 支持配置文件和命令行参数
- 提供JSON格式的报告输出

## 功能特性

### 🔍 多工具集成
- **Ruff**: 快速Python代码检查器
- **Black**: 代码格式化检查
- **MyPy**: 静态类型检查
- **Bandit**: 安全漏洞检测

### 📊 详细报告
- 问题统计和分类
- 执行时间分析
- 改进建议生成
- JSON格式输出

### ⚙️ 灵活配置
- 支持配置文件
- 命令行参数覆盖
- 工具选择性运行
- 自定义输出格式

### 🛡️ 错误处理
- 完善的异常处理
- 超时保护
- 工具可用性检查
- 详细的错误信息

## 安装要求

### Python版本
- Python 3.8+

### 依赖工具
```bash
# 安装代码质量工具
pip install ruff black mypy bandit

# 或者使用requirements.txt
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
# 检查当前目录
python quality_checker.py .

# 检查指定项目
python quality_checker.py /path/to/project

# 详细输出
python quality_checker.py . --verbose
```

### 选择性运行工具

```bash
# 只运行Ruff和Black
python quality_checker.py . --tools ruff black

# 只运行类型检查
python quality_checker.py . --tools mypy

# 只运行安全检查
python quality_checker.py . --tools bandit
```

### 使用配置文件

```bash
# 创建示例配置文件
python quality_checker.py . --create-config

# 使用配置文件
python quality_checker.py . --config quality_config.json
```

### 保存报告

```bash
# 保存报告到JSON文件
python quality_checker.py . --output quality_report.json

# 同时显示和保存报告
python quality_checker.py . --output report.json --verbose
```

## 配置文件格式

创建 `quality_config.json` 文件：

```json
{
  "tools": {
    "ruff": {
      "enabled": true,
      "args": ["--select=E,W,F,I,N"]
    },
    "black": {
      "enabled": true,
      "args": ["--line-length=88"]
    },
    "mypy": {
      "enabled": true,
      "args": ["--strict"]
    },
    "bandit": {
      "enabled": true,
      "args": ["--skip=B101"]
    }
  },
  "output": {
    "format": "json",
    "file": "quality_report.json"
  }
}
```

## 报告格式

### 控制台输出

```
============================================================
代码质量检查报告
============================================================

项目路径: /path/to/project
检查时间: 2024-01-01T12:00:00
Python文件数: 25

摘要:
------------------------------
total_tools: 4
successful_tools: 4
failed_tools: 0
total_issues: 12
total_warnings: 3
total_execution_time: 5.67
overall_success: false

工具检查结果:
------------------------------
✓ ruff: 8 问题, 0 警告 (1.23s)
✓ black: 2 问题, 0 警告 (0.45s)
✓ mypy: 2 问题, 3 警告 (3.12s)
✓ bandit: 0 问题, 0 警告 (0.87s)

改进建议:
------------------------------
1. 解决 ruff 检测到的 8 个问题
2. 解决 black 检测到的 2 个问题
3. 解决 mypy 检测到的 2 个问题
4. 定期运行代码质量检查
5. 在CI/CD流程中集成质量检查
```

### JSON报告格式

```json
{
  "timestamp": "2024-01-01T12:00:00",
  "project_path": "/path/to/project",
  "total_files": 25,
  "summary": {
    "total_tools": 4,
    "successful_tools": 4,
    "failed_tools": 0,
    "total_issues": 12,
    "total_warnings": 3,
    "total_execution_time": 5.67,
    "overall_success": false
  },
  "recommendations": [
    "解决 ruff 检测到的 8 个问题",
    "解决 black 检测到的 2 个问题"
  ],
  "results": [
    {
      "tool": "ruff",
      "success": true,
      "exit_code": 1,
      "output": "...",
      "errors": "",
      "execution_time": 1.23,
      "issues_count": 8,
      "warnings_count": 0
    }
  ]
}
```

## 集成到CI/CD

### GitHub Actions

```yaml
name: Code Quality Check

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: |
        pip install ruff black mypy bandit
    - name: Run quality checks
      run: |
        python session23/project/quality_checker.py . --output quality_report.json
    - name: Upload report
      uses: actions/upload-artifact@v3
      with:
        name: quality-report
        path: quality_report.json
```

### Pre-commit Hook

创建 `.pre-commit-config.yaml`：

```yaml
repos:
  - repo: local
    hooks:
      - id: quality-check
        name: Code Quality Check
        entry: python session23/project/quality_checker.py
        args: ['.', '--tools', 'ruff', 'black']
        language: system
        pass_filenames: false
```

## 扩展功能

### 添加新工具

在 `CodeQualityChecker` 类中添加新工具：

```python
self.tools['pylint'] = {
    'command': ['pylint'],
    'args': ['--output-format=json'],
    'description': 'Pylint 代码检查',
    'enabled': True
}
```

### 自定义报告格式

扩展 `save_report` 方法支持其他格式：

```python
def save_report_html(self, report: QualityReport, output_file: str) -> None:
    """保存HTML格式报告"""
    # 实现HTML报告生成
    pass
```

## 最佳实践

### 1. 定期检查
- 每次提交前运行质量检查
- 在CI/CD流程中集成检查
- 定期审查和更新质量标准

### 2. 团队协作
- 统一使用相同的配置文件
- 制定代码质量标准
- 定期讨论和改进规范

### 3. 渐进改善
- 从基本检查开始
- 逐步提高质量标准
- 重构现有代码

### 4. 工具配置
- 根据项目需求调整工具参数
- 排除不适用的规则
- 保持配置文件的版本控制

## 故障排除

### 常见问题

1. **工具未安装**
   ```bash
   pip install ruff black mypy bandit
   ```

2. **权限问题**
   ```bash
   chmod +x quality_checker.py
   ```

3. **路径问题**
   ```bash
   python quality_checker.py $(pwd)
   ```

4. **配置文件错误**
   ```bash
   python quality_checker.py . --create-config
   ```

### 调试模式

```bash
# 启用详细输出
python quality_checker.py . --verbose

# 检查工具可用性
python -c "from quality_checker import CodeQualityChecker; print(CodeQualityChecker('.').check_tool_availability())"
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 运行质量检查
5. 创建Pull Request

## 许可证

本项目仅用于教学目的。

## 联系方式

如有问题或建议，请联系Python教程团队。