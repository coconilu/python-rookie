# 文本处理工具集

这是一个综合性的文本处理工具集，展示了Python函数编程的各种概念和技巧。该项目包含了文本分析、格式化、转换、验证等多种功能，是学习函数编程的优秀实践项目。

## 项目特色

- **模块化设计**: 将不同功能分为独立的类和模块
- **装饰器应用**: 使用计时、验证、缓存等装饰器
- **高阶函数**: 实现函数组合和管道处理
- **类型提示**: 完整的类型注解支持
- **错误处理**: 完善的异常处理机制
- **实用功能**: 涵盖日常文本处理的各种需求

## 功能模块

### 1. 文本分析模块 (TextAnalyzer)
- 字符统计（总字符数、字母、数字、中文字符等）
- 单词统计（总词数、唯一词数、平均长度等）
- 句子统计（句子数、平均长度等）
- 可读性分析（可读性评分、难度等级）

### 2. 文本格式化模块 (TextFormatter)
- 标题格式转换（标准、智能、全大写）
- 文本对齐（左对齐、右对齐、居中）
- 缩进处理（首行缩进、全文缩进）
- 文本换行（指定宽度换行）
- 表格创建（数据表格生成）

### 3. 文本转换模块 (TextConverter)
- 中文转拼音（简化版）
- 摩尔斯电码转换
- 二进制编码/解码
- Unicode标准化

### 4. 文本验证模块 (TextValidator)
- 邮箱地址验证
- 电话号码验证（中国/美国）
- 身份证号码验证（中国）
- 密码强度验证
- URL地址验证

### 5. 文本处理模块 (TextProcessor)
- 文本清理（去除多余空格、特殊字符等）
- 模式提取（邮箱、电话、URL、数字）
- 模式替换（普通替换、正则替换）
- 单词过滤（移除、替换、高亮）

### 6. 装饰器功能
- **计时装饰器**: 测量函数执行时间
- **验证装饰器**: 输入类型和内容验证
- **缓存装饰器**: 结果缓存优化性能

### 7. 高阶函数
- **函数组合**: 将多个操作组合成一个函数
- **处理管道**: 创建文本处理流水线
- **批量处理**: 对文本列表进行批量操作

## 使用方法

### 基本使用

```python
from text_processor import TextAnalyzer, TextFormatter, TextValidator

# 文本分析
analyzer = TextAnalyzer()
stats = analyzer.count_characters("Hello World 你好世界")
print(stats)

# 文本格式化
formatter = TextFormatter()
title = formatter.to_title_case("hello world", "smart")
print(title)

# 文本验证
validator = TextValidator()
is_valid = validator.is_valid_email("test@example.com")
print(is_valid)
```

### 装饰器使用

```python
from text_processor import timing_decorator, validate_input, cache_result

@timing_decorator
@validate_input(str, True)
@cache_result
def process_text(text):
    # 你的文本处理逻辑
    return text.upper()

result = process_text("hello world")
```

### 高阶函数使用

```python
from text_processor import create_text_pipeline, batch_process_texts

# 创建处理管道
pipeline = create_text_pipeline(
    lambda text: text.strip(),
    lambda text: text.lower(),
    lambda text: text.replace(" ", "_")
)

result = pipeline("  Hello World  ")
print(result)  # "hello_world"

# 批量处理
texts = ["Hello", "World", "Python"]
processed = batch_process_texts(texts, str.upper)
print(processed)  # ["HELLO", "WORLD", "PYTHON"]
```

## 运行演示

直接运行主文件查看完整演示：

```bash
python text_processor.py
```

演示将展示所有功能模块的使用方法和效果。

## 学习要点

### 函数编程概念
1. **纯函数**: 大部分函数都是纯函数，相同输入产生相同输出
2. **高阶函数**: 接受函数作为参数或返回函数的函数
3. **函数组合**: 将简单函数组合成复杂功能
4. **装饰器**: 在不修改原函数的情况下增加功能

### 设计模式
1. **单一职责**: 每个类和函数都有明确的单一职责
2. **开闭原则**: 对扩展开放，对修改封闭
3. **依赖注入**: 通过参数传递依赖关系
4. **策略模式**: 通过参数选择不同的处理策略

### 最佳实践
1. **类型提示**: 使用类型注解提高代码可读性
2. **文档字符串**: 详细的函数和类文档
3. **错误处理**: 适当的异常处理和验证
4. **代码复用**: 通过函数组合避免重复代码

## 扩展建议

1. **添加更多语言支持**: 扩展多语言文本处理功能
2. **性能优化**: 使用更高效的算法和数据结构
3. **配置文件**: 添加配置文件支持自定义设置
4. **插件系统**: 设计插件接口支持功能扩展
5. **GUI界面**: 创建图形用户界面
6. **Web API**: 提供REST API接口

## 相关资源

- [Python官方文档 - 函数](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Python官方文档 - 装饰器](https://docs.python.org/3/glossary.html#term-decorator)
- [Python官方文档 - 高阶函数](https://docs.python.org/3/howto/functional.html)
- [正则表达式教程](https://docs.python.org/3/library/re.html)
- [Unicode处理](https://docs.python.org/3/library/unicodedata.html)

## 注意事项

1. 某些功能（如中文转拼音）使用了简化实现，实际项目中建议使用专门的库
2. 正则表达式模式可能需要根据具体需求调整
3. 性能敏感的应用建议进行性能测试和优化
4. 建议在生产环境中添加更完善的错误处理和日志记录

---

这个项目展示了函数编程在实际应用中的强大威力，通过学习和实践这些代码，你将深入理解Python函数编程的精髓。