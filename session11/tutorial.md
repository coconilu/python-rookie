# Session11: 错误处理与调试 - 详细教程

## 1. 异常处理概述

### 1.1 什么是异常？

异常（Exception）是程序运行时发生的错误事件，它会中断程序的正常执行流程。Python中的异常是一种面向对象的错误处理机制。

### 1.2 常见的异常类型

```python
# 常见异常示例
print(10 / 0)           # ZeroDivisionError: 除零错误
print(int("abc"))       # ValueError: 值错误
print(my_list[10])      # IndexError: 索引错误
print(my_dict["key"])   # KeyError: 键错误
open("nonexistent.txt") # FileNotFoundError: 文件未找到
```

### 1.3 异常的层次结构

```
BaseException
 +-- SystemExit
 +-- KeyboardInterrupt
 +-- GeneratorExit
 +-- Exception
      +-- StopIteration
      +-- ArithmeticError
      |    +-- ZeroDivisionError
      |    +-- OverflowError
      +-- AttributeError
      +-- EOFError
      +-- ImportError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- NameError
      +-- OSError
      |    +-- FileNotFoundError
      +-- RuntimeError
      +-- TypeError
      +-- ValueError
```

## 2. try/except语句

### 2.1 基本语法

```python
try:
    # 可能出现异常的代码
    risky_code()
except ExceptionType:
    # 处理异常的代码
    handle_exception()
```

### 2.2 捕获特定异常

```python
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("错误：不能除以零！")
        return None
    except TypeError:
        print("错误：参数类型不正确！")
        return None

# 测试
print(safe_divide(10, 2))    # 5.0
print(safe_divide(10, 0))    # 错误：不能除以零！
print(safe_divide(10, "a"))  # 错误：参数类型不正确！
```

### 2.3 捕获多个异常

```python
def process_data(data, index):
    try:
        value = data[index]
        result = 100 / value
        return result
    except (IndexError, KeyError):
        print("错误：索引或键不存在！")
    except (ZeroDivisionError, TypeError):
        print("错误：计算错误或类型错误！")
    except Exception as e:
        print(f"未知错误：{e}")
```

### 2.4 获取异常信息

```python
def detailed_error_handling():
    try:
        num = int(input("请输入一个数字："))
        result = 100 / num
        print(f"结果：{result}")
    except ValueError as e:
        print(f"值错误：{e}")
        print(f"异常类型：{type(e).__name__}")
    except ZeroDivisionError as e:
        print(f"除零错误：{e}")
        print(f"异常类型：{type(e).__name__}")
```

## 3. else和finally子句

### 3.1 else子句

else子句在try块没有发生异常时执行：

```python
def file_operation(filename):
    try:
        file = open(filename, 'r')
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
    else:
        print(f"文件 {filename} 打开成功")
        content = file.read()
        print(f"文件内容长度：{len(content)}")
        file.close()
```

### 3.2 finally子句

finally子句无论是否发生异常都会执行，通常用于清理资源：

```python
def safe_file_operation(filename):
    file = None
    try:
        file = open(filename, 'r')
        content = file.read()
        return content
    except FileNotFoundError:
        print(f"文件 {filename} 不存在")
        return None
    except IOError:
        print(f"读取文件 {filename} 时发生错误")
        return None
    finally:
        if file:
            file.close()
            print("文件已关闭")
```

### 3.3 完整的try语句结构

```python
def complete_exception_handling():
    try:
        # 尝试执行的代码
        risky_operation()
    except SpecificException as e:
        # 处理特定异常
        handle_specific_exception(e)
    except Exception as e:
        # 处理其他异常
        handle_general_exception(e)
    else:
        # 没有异常时执行
        success_operation()
    finally:
        # 无论如何都执行
        cleanup_operation()
```

## 4. 抛出异常（raise）

### 4.1 主动抛出异常

```python
def validate_age(age):
    if not isinstance(age, int):
        raise TypeError("年龄必须是整数")
    if age < 0:
        raise ValueError("年龄不能为负数")
    if age > 150:
        raise ValueError("年龄不能超过150岁")
    return True

# 测试
try:
    validate_age(-5)
except ValueError as e:
    print(f"验证失败：{e}")
```

### 4.2 重新抛出异常

```python
def process_file(filename):
    try:
        with open(filename, 'r') as file:
            data = file.read()
            # 处理数据
            return process_data(data)
    except FileNotFoundError:
        print(f"日志：文件 {filename} 不存在")
        raise  # 重新抛出异常
    except Exception as e:
        print(f"日志：处理文件时发生错误 - {e}")
        raise  # 重新抛出异常
```

## 5. 自定义异常类

### 5.1 创建自定义异常

```python
class CustomError(Exception):
    """自定义异常基类"""
    pass

class ValidationError(CustomError):
    """验证错误异常"""
    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field

class BusinessLogicError(CustomError):
    """业务逻辑错误异常"""
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code
```

### 5.2 使用自定义异常

```python
class User:
    def __init__(self, username, email, age):
        self.username = self.validate_username(username)
        self.email = self.validate_email(email)
        self.age = self.validate_age(age)
    
    def validate_username(self, username):
        if not username:
            raise ValidationError("用户名不能为空", "username")
        if len(username) < 3:
            raise ValidationError("用户名长度不能少于3个字符", "username")
        return username
    
    def validate_email(self, email):
        if not email or "@" not in email:
            raise ValidationError("邮箱格式不正确", "email")
        return email
    
    def validate_age(self, age):
        if not isinstance(age, int) or age < 0 or age > 150:
            raise ValidationError("年龄必须是0-150之间的整数", "age")
        return age

# 使用示例
try:
    user = User("", "invalid-email", -5)
except ValidationError as e:
    print(f"验证错误：{e} (字段：{e.field})")
```

## 6. 调试技巧

### 6.1 使用print调试

```python
def debug_function(data):
    print(f"DEBUG: 输入数据 = {data}")  # 调试信息
    
    result = []
    for i, item in enumerate(data):
        print(f"DEBUG: 处理第{i}个元素：{item}")  # 调试信息
        
        if isinstance(item, str):
            processed = item.upper()
        else:
            processed = str(item)
        
        print(f"DEBUG: 处理结果：{processed}")  # 调试信息
        result.append(processed)
    
    print(f"DEBUG: 最终结果 = {result}")  # 调试信息
    return result
```

### 6.2 使用断言（assert）

```python
def calculate_average(numbers):
    assert isinstance(numbers, list), "输入必须是列表"
    assert len(numbers) > 0, "列表不能为空"
    assert all(isinstance(n, (int, float)) for n in numbers), "列表元素必须是数字"
    
    total = sum(numbers)
    average = total / len(numbers)
    
    assert average >= 0, "平均值不应该为负数"  # 业务逻辑断言
    
    return average
```

### 6.3 使用pdb调试器

```python
import pdb

def complex_calculation(x, y):
    pdb.set_trace()  # 设置断点
    
    step1 = x * 2
    step2 = y + 10
    step3 = step1 + step2
    
    if step3 > 100:
        result = step3 / 2
    else:
        result = step3 * 2
    
    return result

# 调试命令：
# n (next) - 执行下一行
# s (step) - 进入函数
# c (continue) - 继续执行
# l (list) - 显示当前代码
# p variable_name - 打印变量值
# q (quit) - 退出调试器
```

## 7. 日志记录

### 7.1 基础日志记录

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def process_data_with_logging(data):
    logger.info(f"开始处理数据，数据长度：{len(data)}")
    
    try:
        result = []
        for i, item in enumerate(data):
            logger.debug(f"处理第{i}个元素：{item}")
            
            if item < 0:
                logger.warning(f"发现负数：{item}")
                continue
            
            processed = item * 2
            result.append(processed)
        
        logger.info(f"数据处理完成，结果长度：{len(result)}")
        return result
    
    except Exception as e:
        logger.error(f"处理数据时发生错误：{e}", exc_info=True)
        raise
```

### 7.2 高级日志配置

```python
import logging
import logging.handlers
from datetime import datetime

class CustomFormatter(logging.Formatter):
    """自定义日志格式化器"""
    
    def format(self, record):
        # 添加自定义字段
        record.custom_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return super().format(record)

def setup_logger(name, log_file, level=logging.INFO):
    """设置日志记录器"""
    
    formatter = CustomFormatter(
        '%(custom_time)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 文件处理器
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=1024*1024, backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
```

## 8. 代码健壮性设计原则

### 8.1 防御性编程

```python
def robust_function(data, config=None):
    """健壮的函数设计示例"""
    
    # 1. 参数验证
    if data is None:
        raise ValueError("数据不能为None")
    
    if not isinstance(data, (list, tuple)):
        raise TypeError("数据必须是列表或元组")
    
    # 2. 默认值处理
    if config is None:
        config = {'timeout': 30, 'retries': 3}
    
    # 3. 边界条件检查
    if len(data) == 0:
        return []
    
    # 4. 异常处理
    result = []
    errors = []
    
    for i, item in enumerate(data):
        try:
            processed = process_item(item, config)
            result.append(processed)
        except Exception as e:
            error_info = {
                'index': i,
                'item': item,
                'error': str(e)
            }
            errors.append(error_info)
            logger.warning(f"处理第{i}个元素时出错：{e}")
    
    # 5. 结果验证
    if len(errors) > len(data) * 0.5:  # 错误率超过50%
        raise RuntimeError(f"处理失败率过高：{len(errors)}/{len(data)}")
    
    return {
        'result': result,
        'errors': errors,
        'success_rate': (len(data) - len(errors)) / len(data)
    }
```

### 8.2 资源管理

```python
from contextlib import contextmanager
import sqlite3

@contextmanager
def database_connection(db_path):
    """数据库连接上下文管理器"""
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

# 使用示例
def safe_database_operation(db_path, query, params):
    try:
        with database_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.fetchall()
    except sqlite3.Error as e:
        logger.error(f"数据库操作失败：{e}")
        raise
```

## 9. 最佳实践

### 9.1 异常处理最佳实践

1. **具体化异常处理**：捕获具体的异常类型，而不是使用裸露的except
2. **不要忽略异常**：至少要记录异常信息
3. **及早失败**：在问题发生的地方立即处理
4. **清理资源**：使用finally或上下文管理器
5. **提供有意义的错误信息**：帮助用户理解问题

```python
# 好的做法
def good_exception_handling(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"文件不存在：{filename}")
        raise
    except PermissionError:
        logger.error(f"没有权限访问文件：{filename}")
        raise
    except UnicodeDecodeError as e:
        logger.error(f"文件编码错误：{filename} - {e}")
        raise

# 避免的做法
def bad_exception_handling(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except:  # 太宽泛
        pass  # 忽略所有错误
```

### 9.2 调试最佳实践

1. **使用日志而不是print**：便于控制和过滤
2. **分层调试**：从高层到底层逐步定位
3. **保留调试信息**：在生产环境中可以快速启用
4. **单元测试**：预防和快速定位问题

## 10. 总结

异常处理和调试是编写健壮Python程序的关键技能：

1. **异常处理**：使程序能够优雅地处理错误情况
2. **调试技巧**：帮助快速定位和解决问题
3. **日志记录**：提供程序运行的详细信息
4. **防御性编程**：预防问题的发生
5. **资源管理**：确保系统资源的正确释放

掌握这些技能将使你能够编写更加稳定和可维护的Python程序。