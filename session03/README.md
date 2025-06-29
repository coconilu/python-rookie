# Session03: 运算符与表达式

## 📚 学习目标

通过本节课的学习，你将掌握：

- **算术运算符**：掌握加减乘除、取模、幂运算等基本数学运算
- **比较运算符**：学会使用等于、不等于、大于、小于等比较操作
- **逻辑运算符**：理解and、or、not逻辑运算的使用
- **运算符优先级**：掌握不同运算符的执行顺序
- **表达式求值**：学会编写和计算复杂的数学表达式
- **实际应用**：通过BMI计算器项目巩固所学知识

## 🎯 核心概念

### 1. 算术运算符 (Arithmetic Operators)

| 运算符 | 名称 | 示例 | 结果 |
|--------|------|------|------|
| `+` | 加法 | `5 + 3` | `8` |
| `-` | 减法 | `5 - 3` | `2` |
| `*` | 乘法 | `5 * 3` | `15` |
| `/` | 除法 | `5 / 2` | `2.5` |
| `//` | 整除 | `5 // 2` | `2` |
| `%` | 取模 | `5 % 2` | `1` |
| `**` | 幂运算 | `5 ** 2` | `25` |

### 2. 比较运算符 (Comparison Operators)

| 运算符 | 名称 | 示例 | 结果 |
|--------|------|------|------|
| `==` | 等于 | `5 == 5` | `True` |
| `!=` | 不等于 | `5 != 3` | `True` |
| `>` | 大于 | `5 > 3` | `True` |
| `<` | 小于 | `5 < 3` | `False` |
| `>=` | 大于等于 | `5 >= 5` | `True` |
| `<=` | 小于等于 | `3 <= 5` | `True` |

### 3. 逻辑运算符 (Logical Operators)

| 运算符 | 名称 | 示例 | 结果 |
|--------|------|------|------|
| `and` | 逻辑与 | `True and False` | `False` |
| `or` | 逻辑或 | `True or False` | `True` |
| `not` | 逻辑非 | `not True` | `False` |

## 演示项目

**BMI计算器** - 一个能够计算身体质量指数(BMI)并给出健康建议的程序

功能特点：
- 输入身高和体重
- 计算BMI值
- 根据BMI值判断健康状况
- 提供健康建议

## 前置知识

- Session01: 环境搭建与Hello World
- Session02: 变量与数据类型
- 基本的数学概念

## 学习时间

预计学习时间：2-3小时

## 文件说明

- `tutorial.md` - 详细教程文档
- `demo.py` - 主要演示代码
- `examples/` - 示例代码目录
  - `example1.py` - 算术运算符示例
  - `example2.py` - 比较运算符示例
  - `example3.py` - 逻辑运算符示例
- `exercises/` - 练习题目录
  - `exercise1.py` - 基础运算练习
  - `exercise2.py` - 比较运算练习
  - `exercise3.py` - 逻辑运算练习
  - `solutions/` - 练习答案
- `project/` - 演示项目（BMI计算器）
- `assets/` - 资源文件

## 快速开始

```bash
# 进入session03目录
cd session03

# 运行演示代码
uv run python demo.py

# 运行示例代码
uv run python examples/example1.py

# 运行演示项目
cd project
uv run python main.py
```

## 学习检查清单

- [ ] 理解所有算术运算符的用法
- [ ] 掌握比较运算符的使用场景
- [ ] 学会使用逻辑运算符组合条件
- [ ] 理解运算符优先级规则
- [ ] 完成所有练习题
- [ ] 成功运行BMI计算器项目
- [ ] 能够编写包含复杂表达式的程序

## 重点难点

### 🔥 重点内容
- 算术运算符的正确使用
- 比较运算符在条件判断中的应用
- 逻辑运算符的组合使用

### ⚠️ 注意事项
- 除法运算符`/`和整除运算符`//`的区别
- 运算符优先级可能导致的计算错误
- 浮点数比较时的精度问题

### 💡 学习技巧
- 多做计算练习，熟悉各种运算符
- 使用括号明确运算顺序
- 通过实际项目理解运算符的应用场景

## 扩展学习

- 位运算符（高级话题）
- 赋值运算符的简写形式
- 运算符重载（面向对象编程中的概念）

---

**准备好开始学习运算符与表达式了吗？让我们通过实际代码来掌握这些重要的编程基础！** 🚀