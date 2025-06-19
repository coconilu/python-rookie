# Session03 项目：BMI健康计算器

## 项目概述

这是一个综合性的BMI（身体质量指数）健康计算器项目，旨在帮助用户了解自己的健康状况。项目将运用Session03学到的运算符知识，包括算术运算、比较运算和逻辑运算。

## 项目目标

通过完成这个项目，你将：

1. **掌握算术运算符的实际应用**
   - 使用基本运算符进行BMI计算
   - 实现单位转换功能
   - 计算健康指标的统计数据

2. **熟练使用比较运算符**
   - 实现BMI等级分类
   - 比较不同时期的健康数据
   - 设置健康目标和进度跟踪

3. **应用逻辑运算符**
   - 实现复杂的健康建议逻辑
   - 处理用户输入验证
   - 组合多个条件进行综合判断

## 功能特性

### 核心功能

1. **BMI计算**
   - 支持公制和英制单位
   - 自动单位转换
   - 精确的BMI计算

2. **健康等级分类**
   - 根据WHO标准分类
   - 亚洲人群特殊标准
   - 年龄相关的调整建议

3. **健康建议系统**
   - 基于BMI的个性化建议
   - 运动和饮食指导
   - 健康风险评估

### 扩展功能

1. **历史记录管理**
   - 保存多次测量数据
   - 趋势分析和可视化
   - 进度跟踪

2. **目标设置**
   - 设定健康目标
   - 计算达成时间
   - 进度监控

3. **数据导出**
   - 生成健康报告
   - 数据备份和恢复
   - 分享功能

## 项目结构

```
project/
├── README.md              # 项目说明文档
├── bmi_calculator.py      # 主程序文件
├── health_advisor.py      # 健康建议模块
├── data_manager.py        # 数据管理模块
├── utils.py              # 工具函数
├── config.py             # 配置文件
├── tests/                # 测试文件目录
│   ├── test_calculator.py
│   ├── test_advisor.py
│   └── test_data_manager.py
└── data/                 # 数据文件目录
    ├── user_data.json
    └── health_standards.json
```

## 技术要求

### 必须使用的运算符

1. **算术运算符**
   - `+`, `-`, `*`, `/` - 基本计算
   - `**` - 平方计算（BMI公式）
   - `//`, `%` - 整除和取模（数据处理）

2. **比较运算符**
   - `<`, `<=`, `>`, `>=` - 数值比较
   - `==`, `!=` - 等值判断
   - 链式比较 - 范围判断

3. **逻辑运算符**
   - `and`, `or`, `not` - 条件组合
   - 短路求值的应用
   - 复杂条件判断

### 编程规范

1. **代码结构**
   - 函数式编程思想
   - 模块化设计
   - 清晰的函数命名

2. **错误处理**
   - 输入验证
   - 异常处理
   - 用户友好的错误信息

3. **文档规范**
   - 详细的函数文档
   - 代码注释
   - 使用示例

## 实现步骤

### 第一阶段：基础功能（必做）

1. **创建BMI计算器**
   ```python
   def calculate_bmi(weight, height, unit='metric'):
       # 实现BMI计算逻辑
       pass
   ```

2. **实现等级分类**
   ```python
   def classify_bmi(bmi, age=None, ethnicity='general'):
       # 实现BMI分类逻辑
       pass
   ```

3. **添加单位转换**
   ```python
   def convert_units(value, from_unit, to_unit):
       # 实现单位转换
       pass
   ```

### 第二阶段：增强功能（推荐）

1. **健康建议系统**
   ```python
   def generate_health_advice(bmi, age, gender, activity_level):
       # 生成个性化健康建议
       pass
   ```

2. **数据验证**
   ```python
   def validate_input(weight, height, age):
       # 验证用户输入
       pass
   ```

3. **历史记录**
   ```python
   def save_record(user_data):
       # 保存用户数据
       pass
   
   def load_history(user_id):
       # 加载历史记录
       pass
   ```

### 第三阶段：高级功能（挑战）

1. **趋势分析**
   ```python
   def analyze_trend(history_data):
       # 分析健康趋势
       pass
   ```

2. **目标管理**
   ```python
   def set_health_goal(current_bmi, target_bmi, timeline):
       # 设置健康目标
       pass
   ```

3. **报告生成**
   ```python
   def generate_report(user_data, history):
       # 生成健康报告
       pass
   ```

## 测试用例

### 基础测试

```python
# BMI计算测试
assert calculate_bmi(70, 1.75) == 22.86  # 正常体重
assert calculate_bmi(50, 1.60) == 19.53  # 偏瘦
assert calculate_bmi(90, 1.70) == 31.14  # 肥胖

# 分类测试
assert classify_bmi(18.4) == "偏瘦"
assert classify_bmi(22.0) == "正常"
assert classify_bmi(28.0) == "偏胖"
assert classify_bmi(32.0) == "肥胖"
```

### 边界测试

```python
# 边界值测试
assert classify_bmi(18.5) == "正常"  # 正常下限
assert classify_bmi(24.0) == "正常"  # 正常上限
assert classify_bmi(24.1) == "偏胖"  # 偏胖下限
```

### 异常测试

```python
# 异常输入测试
try:
    calculate_bmi(-70, 1.75)  # 负重量
    assert False, "应该抛出异常"
except ValueError:
    pass  # 预期的异常
```

## 评分标准

### 基础功能（60分）

- [ ] BMI计算正确性（20分）
- [ ] 等级分类准确性（20分）
- [ ] 单位转换功能（10分）
- [ ] 基本错误处理（10分）

### 代码质量（25分）

- [ ] 代码结构清晰（10分）
- [ ] 函数设计合理（8分）
- [ ] 注释和文档（7分）

### 扩展功能（15分）

- [ ] 健康建议系统（8分）
- [ ] 数据管理功能（7分）

## 学习资源

### 相关知识点

1. **BMI计算公式**
   - BMI = 体重(kg) / 身高²(m²)
   - 英制转换：1磅 = 0.453592公斤，1英寸 = 0.0254米

2. **WHO BMI分类标准**
   - 偏瘦：< 18.5
   - 正常：18.5 - 24.9
   - 偏胖：25.0 - 29.9
   - 肥胖：≥ 30.0

3. **亚洲人群标准**
   - 偏瘦：< 18.5
   - 正常：18.5 - 22.9
   - 偏胖：23.0 - 27.4
   - 肥胖：≥ 27.5

### 参考资料

- [WHO BMI分类标准](https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight)
- [Python官方文档 - 运算符](https://docs.python.org/3/library/operator.html)
- [健康生活方式指南](https://www.cdc.gov/healthyweight/)

## 提交要求

1. **代码文件**
   - 所有Python源文件
   - 测试文件
   - 配置文件

2. **文档**
   - 项目说明文档
   - 使用说明
   - 测试报告

3. **演示**
   - 功能演示视频或截图
   - 测试结果展示
   - 问题和解决方案总结

## 常见问题

### Q: 如何处理浮点数精度问题？
A: 使用`round()`函数控制小数位数，或使用`decimal`模块进行精确计算。

### Q: 如何验证用户输入的合理性？
A: 设置合理的数值范围，例如体重在1-1000kg之间，身高在0.5-3.0m之间。

### Q: 如何处理不同年龄段的BMI标准？
A: 可以为儿童和老年人设置不同的分类标准，或提供年龄相关的建议。

### Q: 如何实现数据持久化？
A: 可以使用JSON文件、CSV文件或SQLite数据库来保存用户数据。

## 扩展挑战

1. **图形界面**：使用tkinter创建GUI界面
2. **数据可视化**：使用matplotlib绘制BMI趋势图
3. **Web应用**：使用Flask创建Web版本
4. **移动应用**：使用Kivy开发移动应用
5. **API集成**：集成营养和运动数据API

---

**祝你编程愉快！记住，这个项目不仅是为了练习运算符，更是为了学习如何将编程知识应用到实际问题中。**