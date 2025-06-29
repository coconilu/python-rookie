# Session02 项目：个人信息管理系统

## 项目概述

这是一个基于命令行的个人信息管理系统，旨在帮助学生实践Session02中学到的变量与数据类型知识。通过这个项目，你将学会如何在实际应用中使用不同的数据类型、进行类型转换、处理用户输入以及格式化输出。

## 学习目标

通过完成这个项目，你将能够：

- ✅ 熟练使用Python的基本数据类型（字符串、整数、浮点数、布尔值）
- ✅ 掌握变量的定义、赋值和使用
- ✅ 理解并应用类型转换
- ✅ 处理用户输入和数据验证
- ✅ 使用字符串格式化进行美观的输出
- ✅ 编写结构化的Python程序
- ✅ 应用基本的错误处理

## 项目功能要求

### 核心功能

1. **用户信息录入**
   - 姓名（字符串）
   - 年龄（整数）
   - 身高（浮点数，单位：米）
   - 体重（浮点数，单位：公斤）
   - 是否学生（布尔值）
   - 联系电话（字符串）
   - 邮箱地址（字符串）

2. **信息显示**
   - 格式化显示所有录入的信息
   - 计算并显示BMI指数
   - 根据年龄判断年龄段
   - 显示用户类型（学生/非学生）

3. **数据处理**
   - 输入数据的类型转换
   - 基本的数据验证
   - 计算衍生信息（如BMI、年龄段等）

### 进阶功能（可选）

4. **数据统计**
   - 统计录入的用户数量
   - 计算平均年龄、身高、体重
   - 统计学生和非学生的比例

5. **数据搜索**
   - 按姓名搜索用户
   - 按年龄范围筛选用户
   - 按用户类型筛选

## 技术要求

### 必须使用的知识点

- **变量定义和赋值**：存储用户信息
- **基本数据类型**：字符串、整数、浮点数、布尔值
- **类型转换**：`int()`, `float()`, `str()`, `bool()`
- **字符串操作**：格式化、大小写转换、去除空格
- **用户输入**：`input()` 函数
- **条件判断**：`if-elif-else` 语句
- **基本运算**：算术运算、比较运算

### 代码规范

- 使用有意义的变量名
- 添加适当的注释
- 保持代码整洁和可读性
- 遵循Python命名规范

## 项目结构

```
project/
├── README.md              # 项目说明文档
├── main.py               # 主程序文件
├── user_manager.py       # 用户管理模块
├── utils.py              # 工具函数模块
├── constants.py          # 常量定义
└── examples/             # 示例和测试数据
    ├── sample_data.py    # 示例数据
    └── demo_usage.py     # 使用演示
```

## 实现步骤

### 第一阶段：基础实现

1. **创建主程序框架**
   - 设计程序主菜单
   - 实现基本的用户交互

2. **实现用户信息录入**
   - 获取用户输入
   - 进行类型转换
   - 基本数据验证

3. **实现信息显示**
   - 格式化输出用户信息
   - 计算并显示BMI
   - 判断年龄段

### 第二阶段：功能完善

4. **添加数据验证**
   - 年龄范围检查
   - 身高体重合理性检查
   - 邮箱格式简单验证

5. **优化用户体验**
   - 美化输出格式
   - 添加错误提示
   - 实现重新输入功能

### 第三阶段：进阶功能

6. **多用户管理**
   - 存储多个用户信息
   - 实现用户列表显示

7. **数据统计和搜索**
   - 实现统计功能
   - 添加搜索功能

## 示例运行效果

```
=== 个人信息管理系统 ===

请选择操作：
1. 录入新用户信息
2. 显示用户信息
3. 查看统计信息
4. 搜索用户
5. 退出系统

请输入选择 (1-5): 1

=== 录入用户信息 ===
请输入姓名: 张三
请输入年龄: 25
请输入身高 (米): 1.75
请输入体重 (公斤): 70
是否为学生 (y/n): n
请输入联系电话: 13800138000
请输入邮箱地址: zhangsan@example.com

用户信息录入成功！

=== 用户信息 ===
姓名: 张三
年龄: 25岁 (青年)
身高: 1.75米
体重: 70.0公斤
BMI指数: 22.9 (正常)
用户类型: 非学生
联系电话: 13800138000
邮箱地址: zhangsan@example.com
```

## 评估标准

### 基础要求 (60分)

- ✅ 正确使用各种数据类型
- ✅ 实现基本的用户信息录入和显示
- ✅ 进行必要的类型转换
- ✅ 代码能够正常运行

### 良好实现 (80分)

- ✅ 包含数据验证功能
- ✅ 输出格式美观
- ✅ 代码结构清晰
- ✅ 添加适当注释

### 优秀实现 (100分)

- ✅ 实现多用户管理
- ✅ 包含统计和搜索功能
- ✅ 良好的错误处理
- ✅ 代码模块化
- ✅ 用户体验优秀

## 常见问题和解决方案

### Q1: 如何处理用户输入的无效数据？

**A1**: 使用try-except语句捕获类型转换错误：

```python
try:
    age = int(input("请输入年龄: "))
except ValueError:
    print("请输入有效的数字")
```

### Q2: 如何判断用户输入的布尔值？

**A2**: 将用户输入转换为小写，然后判断：

```python
is_student_input = input("是否为学生 (y/n): ").lower()
is_student = is_student_input in ['y', 'yes', '是', '1']
```

### Q3: 如何计算BMI指数？

**A3**: BMI = 体重(kg) / 身高(m)²

```python
bmi = weight / (height ** 2)
```

### Q4: 如何美化输出格式？

**A4**: 使用字符串格式化：

```python
print(f"BMI指数: {bmi:.1f}")
print("=" * 30)
```

## 扩展学习

完成基础项目后，可以尝试以下扩展：

1. **数据持久化**：将用户信息保存到文件
2. **图形界面**：使用tkinter创建GUI版本
3. **数据分析**：添加更多统计功能
4. **网络功能**：实现用户信息的网络同步

## 提交要求

1. **代码文件**：所有.py文件
2. **运行截图**：展示程序运行效果
3. **说明文档**：简要说明实现思路和遇到的问题
4. **测试数据**：提供一些测试用例

## 时间安排

- **第1-2天**：完成基础功能实现
- **第3-4天**：添加数据验证和优化
- **第5-6天**：实现进阶功能
- **第7天**：测试、调试和文档整理

---

**祝你编程愉快！通过这个项目，你将对Python的变量和数据类型有更深入的理解。**