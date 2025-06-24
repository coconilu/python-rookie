# Session23 快速开始指南

欢迎来到Python代码质量与规范教程！这个快速指南将帮助您在5分钟内开始学习和使用代码质量工具。

## 🚀 快速开始

### 1. 检查环境

首先确保您的Python环境正常：

```bash
python --version  # 确保Python 3.8+
pip --version     # 确保pip可用
```

### 2. 安装工具（推荐）

运行我们提供的安装脚本：

```bash
# 自动安装必需工具
python install_tools.py --essential-only

# 或者安装所有工具
python install_tools.py --install-all
```

### 3. 运行演示

```bash
# 查看完整演示
python run_demo.py

# 或者直接运行主演示
python demo.py
```

### 4. 尝试项目

```bash
cd project
python quality_checker.py --help
python quality_checker.py .
```

## 📚 学习路径

### 初学者路径（30分钟）

1. **阅读教程** (10分钟)
   - 打开 `tutorial.md`
   - 重点阅读"PEP 8规范"和"基本工具使用"部分

2. **运行演示** (10分钟)
   ```bash
   python run_demo.py
   ```

3. **查看示例** (10分钟)
   - 查看 `examples/example1.py` - PEP 8规范示例
   - 查看 `examples/example2.py` - 代码格式化示例

### 进阶路径（1小时）

1. **完成练习** (30分钟)
   - 打开 `exercises/exercise1.py`
   - 尝试修复代码问题
   - 对比 `exercises/solutions/exercise1_solution.py`

2. **配置工具** (15分钟)
   - 复制 `exercises/solutions/pyproject.toml` 到您的项目
   - 运行工具检查您的代码

3. **项目实践** (15分钟)
   - 使用 `project/quality_checker.py` 检查您的项目
   - 根据报告改进代码

### 专家路径（2小时）

1. **深入学习** (60分钟)
   - 完整阅读 `tutorial.md`
   - 理解所有工具的配置选项
   - 学习CI/CD集成

2. **高级练习** (30分钟)
   - 完成 `exercises/exercise2.py`
   - 创建自定义配置文件
   - 集成到您的开发流程

3. **项目集成** (30分钟)
   - 在真实项目中应用学到的知识
   - 设置pre-commit钩子
   - 配置IDE集成

## 🛠️ 常用命令

### 代码检查
```bash
# 使用ruff检查代码
ruff check .
ruff check --fix .  # 自动修复

# 使用black格式化
black .
black --check .     # 仅检查，不修改

# 类型检查
mypy .

# 安全检查
bandit -r .
```

### 项目工具
```bash
# 运行完整质量检查
python project/quality_checker.py .

# 生成报告
python project/quality_checker.py . --output report.json

# 仅运行特定工具
python project/quality_checker.py . --tools ruff,black
```

## 📁 文件结构说明

```
session23/
├── README.md              # 课程概述
├── QUICKSTART.md          # 快速开始指南（本文件）
├── tutorial.md            # 详细教程
├── demo.py                # 主演示脚本
├── run_demo.py            # 完整演示脚本
├── install_tools.py       # 工具安装脚本
├── examples/              # 示例代码
│   ├── example1.py        # PEP 8规范示例
│   ├── example2.py        # 代码格式化示例
│   └── example3.py        # 静态分析示例
├── exercises/             # 练习题
│   ├── exercise1.py       # 基础练习
│   ├── exercise2.py       # 进阶练习
│   └── solutions/         # 练习答案
└── project/               # 实际项目
    ├── quality_checker.py # 代码质量检查器
    ├── requirements.txt   # 依赖列表
    └── README.md          # 项目说明
```

## 🎯 学习目标检查

完成学习后，您应该能够：

- [ ] 理解PEP 8编码规范的重要性
- [ ] 使用ruff进行代码检查和修复
- [ ] 使用black进行代码格式化
- [ ] 使用mypy进行类型检查
- [ ] 识别和修复常见的代码质量问题
- [ ] 配置代码质量工具
- [ ] 将工具集成到开发流程中

## 🔧 故障排除

### 工具安装问题

**问题**: pip install 失败
```bash
# 解决方案：升级pip
python -m pip install --upgrade pip

# 或使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ ruff
```

**问题**: 工具命令不可用
```bash
# 检查PATH环境变量
echo $PATH  # Linux/Mac
echo %PATH% # Windows

# 或使用python -m运行
python -m ruff check .
python -m black .
```

### 常见错误

**问题**: "command not found"
- 确保工具已正确安装
- 检查虚拟环境是否激活
- 尝试使用 `python -m tool_name` 格式

**问题**: 配置文件不生效
- 确保配置文件在正确位置
- 检查文件格式和语法
- 查看工具文档了解配置优先级

## 📞 获取帮助

1. **查看工具帮助**
   ```bash
   ruff --help
   black --help
   mypy --help
   ```

2. **运行测试**
   ```bash
   python project/test_quality_checker.py
   ```

3. **查看示例配置**
   - `exercises/solutions/pyproject.toml`
   - `exercises/solutions/mypy.ini`

## 🎉 下一步

完成本教程后，建议您：

1. **在实际项目中应用**
   - 为您的项目添加代码质量检查
   - 配置适合的规则和设置

2. **学习更多工具**
   - pytest（测试框架）
   - coverage（代码覆盖率）
   - sphinx（文档生成）

3. **建立团队规范**
   - 制定团队编码标准
   - 设置CI/CD流水线
   - 定期进行代码审查

4. **持续改进**
   - 关注工具更新
   - 学习新的最佳实践
   - 分享经验和知识

---

**祝您学习愉快！** 🐍✨

如果您觉得这个教程有帮助，请考虑：
- 在您的项目中应用这些实践
- 与同事分享这些知识
- 为开源项目贡献代码质量改进