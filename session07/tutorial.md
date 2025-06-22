# Session07: 文件操作详细教程

## 1. 文件操作基础

### 1.1 什么是文件操作

文件操作是程序与外部数据交互的重要方式。通过文件操作，我们可以：
- 读取配置信息
- 保存程序数据
- 处理日志文件
- 导入导出数据

### 1.2 文件的基本概念

**文件路径**：
- 绝对路径：从根目录开始的完整路径
- 相对路径：相对于当前工作目录的路径

**文件模式**：
- `'r'`：只读模式（默认）
- `'w'`：写入模式（覆盖原文件）
- `'a'`：追加模式
- `'x'`：独占创建模式
- `'b'`：二进制模式
- `'t'`：文本模式（默认）

## 2. 基本文件操作

### 2.1 打开和关闭文件

```python
# 传统方式
file = open('example.txt', 'r', encoding='utf-8')
content = file.read()
file.close()  # 必须手动关闭

# 推荐方式：使用with语句
with open('example.txt', 'r', encoding='utf-8') as file:
    content = file.read()
# 文件会自动关闭
```

### 2.2 读取文件

```python
# 读取整个文件
with open('data.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    print(content)

# 按行读取
with open('data.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line.strip())  # strip()去除换行符

# 读取所有行到列表
with open('data.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(lines)

# 读取一行
with open('data.txt', 'r', encoding='utf-8') as f:
    first_line = f.readline()
    print(first_line)
```

### 2.3 写入文件

```python
# 写入文本（覆盖模式）
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write('Hello, World!\n')
    f.write('这是第二行\n')

# 追加文本
with open('output.txt', 'a', encoding='utf-8') as f:
    f.write('这是追加的内容\n')

# 写入多行
lines = ['第一行\n', '第二行\n', '第三行\n']
with open('output.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines)
```

## 3. 文件路径处理

### 3.1 使用os.path模块

```python
import os

# 获取当前工作目录
current_dir = os.getcwd()
print(f"当前目录: {current_dir}")

# 路径拼接
file_path = os.path.join('data', 'logs', 'app.log')
print(f"文件路径: {file_path}")

# 检查路径是否存在
if os.path.exists(file_path):
    print("文件存在")
else:
    print("文件不存在")

# 获取文件信息
if os.path.isfile(file_path):
    print("这是一个文件")
elif os.path.isdir(file_path):
    print("这是一个目录")

# 分离路径和文件名
dir_name = os.path.dirname(file_path)
file_name = os.path.basename(file_path)
print(f"目录: {dir_name}")
print(f"文件名: {file_name}")

# 分离文件名和扩展名
name, ext = os.path.splitext(file_name)
print(f"文件名: {name}")
print(f"扩展名: {ext}")
```

### 3.2 使用pathlib模块（推荐）

```python
from pathlib import Path

# 创建路径对象
file_path = Path('data') / 'logs' / 'app.log'
print(f"文件路径: {file_path}")

# 检查路径是否存在
if file_path.exists():
    print("文件存在")

# 获取文件信息
if file_path.is_file():
    print("这是一个文件")
elif file_path.is_dir():
    print("这是一个目录")

# 获取路径组件
print(f"父目录: {file_path.parent}")
print(f"文件名: {file_path.name}")
print(f"文件名（无扩展名）: {file_path.stem}")
print(f"扩展名: {file_path.suffix}")

# 创建目录
data_dir = Path('data')
data_dir.mkdir(exist_ok=True)  # exist_ok=True表示目录存在时不报错
```

## 4. 目录操作

### 4.1 创建和删除目录

```python
import os
import shutil
from pathlib import Path

# 使用os模块
os.makedirs('new_folder/sub_folder', exist_ok=True)
os.rmdir('empty_folder')  # 只能删除空目录
shutil.rmtree('folder_with_files')  # 删除目录及其内容

# 使用pathlib
Path('new_folder').mkdir(exist_ok=True)
Path('new_folder/sub_folder').mkdir(parents=True, exist_ok=True)
```

### 4.2 遍历目录

```python
import os
from pathlib import Path

# 使用os.listdir()
for item in os.listdir('.'):
    print(item)

# 使用os.walk()递归遍历
for root, dirs, files in os.walk('.'):
    print(f"目录: {root}")
    for file in files:
        print(f"  文件: {file}")

# 使用pathlib
for item in Path('.').iterdir():
    if item.is_file():
        print(f"文件: {item.name}")
    elif item.is_dir():
        print(f"目录: {item.name}")

# 递归查找特定文件
for txt_file in Path('.').rglob('*.txt'):
    print(f"找到文本文件: {txt_file}")
```

## 5. 处理不同格式的文件

### 5.1 CSV文件处理

```python
import csv

# 读取CSV文件
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# 使用DictReader读取（推荐）
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row['name'], row['age'])

# 写入CSV文件
data = [
    ['姓名', '年龄', '城市'],
    ['张三', '25', '北京'],
    ['李四', '30', '上海']
]

with open('output.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(data)

# 使用DictWriter写入
data = [
    {'name': '张三', 'age': 25, 'city': '北京'},
    {'name': '李四', 'age': 30, 'city': '上海'}
]

with open('output.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['name', 'age', 'city']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
```

### 5.2 JSON文件处理

```python
import json

# 读取JSON文件
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(data)

# 写入JSON文件
data = {
    'users': [
        {'name': '张三', 'age': 25},
        {'name': '李四', 'age': 30}
    ],
    'total': 2
}

with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 处理JSON字符串
json_str = '{"name": "张三", "age": 25}'
data = json.loads(json_str)
print(data['name'])

new_json_str = json.dumps(data, ensure_ascii=False)
print(new_json_str)
```

## 6. 异常处理

### 6.1 文件操作中的常见异常

```python
try:
    with open('nonexistent.txt', 'r') as f:
        content = f.read()
except FileNotFoundError:
    print("文件不存在")
except PermissionError:
    print("没有权限访问文件")
except UnicodeDecodeError:
    print("文件编码错误")
except Exception as e:
    print(f"其他错误: {e}")
```

### 6.2 安全的文件操作

```python
def safe_read_file(filename):
    """
    安全地读取文件内容
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"错误：文件 {filename} 不存在")
        return None
    except PermissionError:
        print(f"错误：没有权限读取文件 {filename}")
        return None
    except UnicodeDecodeError:
        print(f"错误：文件 {filename} 编码格式不正确")
        return None
    except Exception as e:
        print(f"读取文件时发生未知错误: {e}")
        return None

def safe_write_file(filename, content):
    """
    安全地写入文件内容
    """
    try:
        # 确保目录存在
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except PermissionError:
        print(f"错误：没有权限写入文件 {filename}")
        return False
    except Exception as e:
        print(f"写入文件时发生错误: {e}")
        return False
```

## 7. 文件编码

### 7.1 常见编码格式

```python
# UTF-8编码（推荐）
with open('utf8_file.txt', 'w', encoding='utf-8') as f:
    f.write('这是UTF-8编码的文件')

# GBK编码（中文Windows系统常用）
with open('gbk_file.txt', 'w', encoding='gbk') as f:
    f.write('这是GBK编码的文件')

# 自动检测编码
import chardet

def detect_encoding(filename):
    with open(filename, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result['encoding']

# 使用检测到的编码读取文件
encoding = detect_encoding('unknown_encoding.txt')
with open('unknown_encoding.txt', 'r', encoding=encoding) as f:
    content = f.read()
```

## 8. 实用技巧

### 8.1 文件备份

```python
import shutil
from datetime import datetime

def backup_file(filename):
    """
    创建文件备份
    """
    if not Path(filename).exists():
        print(f"文件 {filename} 不存在")
        return False
    
    # 生成备份文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"{filename}.backup_{timestamp}"
    
    try:
        shutil.copy2(filename, backup_name)
        print(f"备份创建成功: {backup_name}")
        return True
    except Exception as e:
        print(f"备份失败: {e}")
        return False
```

### 8.2 批量文件处理

```python
def process_text_files(directory, operation):
    """
    批量处理目录中的文本文件
    """
    directory = Path(directory)
    
    for txt_file in directory.rglob('*.txt'):
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 执行操作
            processed_content = operation(content)
            
            # 写回文件
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(processed_content)
                
            print(f"处理完成: {txt_file}")
            
        except Exception as e:
            print(f"处理文件 {txt_file} 时出错: {e}")

# 使用示例：将所有文本转换为大写
def to_uppercase(text):
    return text.upper()

process_text_files('documents', to_uppercase)
```

## 9. 性能优化

### 9.1 大文件处理

```python
def process_large_file(filename, chunk_size=1024*1024):  # 1MB chunks
    """
    分块处理大文件
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                # 处理数据块
                process_chunk(chunk)
                
    except Exception as e:
        print(f"处理大文件时出错: {e}")

def process_chunk(chunk):
    """
    处理数据块
    """
    # 在这里实现具体的处理逻辑
    pass
```

### 9.2 内存友好的行处理

```python
def count_lines_memory_efficient(filename):
    """
    内存友好的行计数
    """
    count = 0
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:  # 逐行读取，不会将整个文件加载到内存
                count += 1
        return count
    except Exception as e:
        print(f"计数行数时出错: {e}")
        return -1
```

## 10. 总结

文件操作是Python编程中的重要技能，掌握以下要点：

1. **使用with语句**：确保文件正确关闭
2. **指定编码**：避免编码问题，推荐使用UTF-8
3. **异常处理**：处理文件不存在、权限不足等异常
4. **路径处理**：使用pathlib模块进行现代化的路径操作
5. **性能考虑**：对于大文件，使用分块或逐行处理

## 下一步学习

- 学习更多文件格式处理（XML、Excel等）
- 了解文件压缩和解压缩
- 学习网络文件操作
- 掌握数据库文件操作

## 练习建议

1. 完成本课的所有练习题
2. 尝试处理不同格式的文件
3. 编写一个文件管理工具
4. 实践异常处理和错误恢复