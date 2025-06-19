#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session01 示例1: Hello World的多种写法

这个示例展示了在Python中输出"Hello World"的不同方法
"""

# 方法1: 最简单的方式
print("Hello, World!")

# 方法2: 使用变量
message = "Hello, World!"
print(message)

# 方法3: 使用函数
def say_hello():
    return "Hello, World!"

print(say_hello())

# 方法4: 使用格式化字符串
greeting = "Hello"
target = "World"
print(f"{greeting}, {target}!")

# 方法5: 多语言版本
print("Hello, World!")  # 英语
print("你好，世界！")     # 中文
print("Hola, Mundo!")   # 西班牙语
print("Bonjour, Monde!") # 法语
print("こんにちは、世界！")  # 日语

# 方法6: 使用循环输出多次
for i in range(3):
    print(f"第{i+1}次: Hello, World!")

# 方法7: 带装饰的输出
print("*" * 30)
print("*" + " " * 28 + "*")
print("*" + "    Hello, World!    " + "*")
print("*" + " " * 28 + "*")
print("*" * 30)