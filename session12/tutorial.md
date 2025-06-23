# Session12: 数据处理 - NumPy 详细教程

## 1. NumPy简介

### 什么是NumPy？

NumPy（Numerical Python）是Python中用于科学计算的基础库。它提供了高性能的多维数组对象和用于处理这些数组的工具。

### NumPy的优势

1. **高性能**：底层用C语言实现，比Python原生列表快10-100倍
2. **内存效率**：数组元素在内存中连续存储
3. **广播机制**：支持不同形状数组之间的运算
4. **丰富的函数库**：提供大量数学、统计、线性代数函数
5. **生态系统基础**：是Pandas、Matplotlib、Scikit-learn等库的基础

### 安装NumPy

```bash
# 使用uv安装
uv add numpy

# 或使用pip安装
pip install numpy
```

## 2. NumPy数组基础

### 2.1 导入NumPy

```python
import numpy as np

# 查看版本
print(f"NumPy版本: {np.__version__}")
```

### 2.2 创建数组

#### 从Python列表创建

```python
# 一维数组
arr1d = np.array([1, 2, 3, 4, 5])
print(f"一维数组: {arr1d}")
print(f"数据类型: {arr1d.dtype}")

# 二维数组
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print(f"二维数组:\n{arr2d}")

# 三维数组
arr3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print(f"三维数组:\n{arr3d}")
```

#### 使用NumPy函数创建

```python
# 创建零数组
zeros = np.zeros((3, 4))
print(f"零数组:\n{zeros}")

# 创建一数组
ones = np.ones((2, 3))
print(f"一数组:\n{ones}")

# 创建单位矩阵
eye = np.eye(3)
print(f"单位矩阵:\n{eye}")

# 创建等差数列
arange = np.arange(0, 10, 2)
print(f"等差数列: {arange}")

# 创建等间距数列
linspace = np.linspace(0, 1, 5)
print(f"等间距数列: {linspace}")

# 创建随机数组
random = np.random.random((2, 3))
print(f"随机数组:\n{random}")
```

### 2.3 数组属性

```python
arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])

print(f"数组形状: {arr.shape}")      # (2, 4)
print(f"数组维度: {arr.ndim}")       # 2
print(f"数组大小: {arr.size}")       # 8
print(f"数据类型: {arr.dtype}")      # int32 或 int64
print(f"每个元素字节数: {arr.itemsize}")  # 4 或 8
```

## 3. 数组索引和切片

### 3.1 一维数组索引

```python
arr = np.array([10, 20, 30, 40, 50])

# 正向索引
print(f"第一个元素: {arr[0]}")     # 10
print(f"第三个元素: {arr[2]}")     # 30

# 反向索引
print(f"最后一个元素: {arr[-1]}")   # 50
print(f"倒数第二个: {arr[-2]}")     # 40

# 切片操作
print(f"前三个元素: {arr[:3]}")     # [10 20 30]
print(f"后三个元素: {arr[-3:]}")    # [30 40 50]
print(f"步长为2: {arr[::2]}")      # [10 30 50]
```

### 3.2 二维数组索引

```python
arr2d = np.array([[1, 2, 3, 4],
                   [5, 6, 7, 8],
                   [9, 10, 11, 12]])

# 访问单个元素
print(f"第2行第3列: {arr2d[1, 2]}")  # 7

# 访问整行
print(f"第一行: {arr2d[0]}")        # [1 2 3 4]
print(f"第一行: {arr2d[0, :]}")     # [1 2 3 4]

# 访问整列
print(f"第二列: {arr2d[:, 1]}")     # [2 6 10]

# 切片操作
print(f"前两行前三列:\n{arr2d[:2, :3]}")
# [[1 2 3]
#  [5 6 7]]
```

### 3.3 布尔索引

```python
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# 创建布尔掩码
mask = arr > 5
print(f"大于5的掩码: {mask}")

# 使用布尔索引
result = arr[mask]
print(f"大于5的元素: {result}")     # [6 7 8 9 10]

# 直接使用条件
even_numbers = arr[arr % 2 == 0]
print(f"偶数: {even_numbers}")      # [2 4 6 8 10]
```

## 4. 数组形状操作

### 4.1 改变数组形状

```python
arr = np.arange(12)
print(f"原始数组: {arr}")

# reshape - 改变形状（不改变原数组）
reshaped = arr.reshape(3, 4)
print(f"重塑为3x4:\n{reshaped}")

# resize - 改变形状（改变原数组）
arr.resize(2, 6)
print(f"调整大小为2x6:\n{arr}")

# flatten - 展平为一维
flattened = reshaped.flatten()
print(f"展平: {flattened}")

# ravel - 展平为一维（返回视图）
raveled = reshaped.ravel()
print(f"展平视图: {raveled}")
```

### 4.2 数组转置

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])
print(f"原数组:\n{arr}")

# 转置
transposed = arr.T
print(f"转置后:\n{transposed}")

# 或使用transpose方法
transposed2 = arr.transpose()
print(f"转置方法:\n{transposed2}")
```

### 4.3 数组拼接和分割

```python
# 数组拼接
arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])

# 垂直拼接
vstack_result = np.vstack((arr1, arr2))
print(f"垂直拼接:\n{vstack_result}")

# 水平拼接
hstack_result = np.hstack((arr1, arr2))
print(f"水平拼接:\n{hstack_result}")

# 数组分割
arr = np.arange(12).reshape(3, 4)
print(f"原数组:\n{arr}")

# 水平分割
hsplit_result = np.hsplit(arr, 2)
print(f"水平分割: {len(hsplit_result)}个数组")
for i, sub_arr in enumerate(hsplit_result):
    print(f"子数组{i+1}:\n{sub_arr}")
```

## 5. 数学运算

### 5.1 基本算术运算

```python
arr1 = np.array([1, 2, 3, 4])
arr2 = np.array([5, 6, 7, 8])

# 元素级运算
print(f"加法: {arr1 + arr2}")      # [6 8 10 12]
print(f"减法: {arr2 - arr1}")      # [4 4 4 4]
print(f"乘法: {arr1 * arr2}")      # [5 12 21 32]
print(f"除法: {arr2 / arr1}")      # [5. 3. 2.33 2.]
print(f"幂运算: {arr1 ** 2}")      # [1 4 9 16]

# 标量运算
print(f"数组+标量: {arr1 + 10}")   # [11 12 13 14]
print(f"数组*标量: {arr1 * 3}")    # [3 6 9 12]
```

### 5.2 数学函数

```python
arr = np.array([1, 4, 9, 16, 25])

# 平方根
sqrt_result = np.sqrt(arr)
print(f"平方根: {sqrt_result}")

# 对数
log_result = np.log(arr)
print(f"自然对数: {log_result}")

# 三角函数
angles = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
sin_result = np.sin(angles)
print(f"正弦值: {sin_result}")

# 指数函数
exp_result = np.exp([1, 2, 3])
print(f"指数: {exp_result}")
```

### 5.3 统计函数

```python
data = np.array([[1, 2, 3, 4],
                 [5, 6, 7, 8],
                 [9, 10, 11, 12]])

# 基本统计
print(f"最小值: {np.min(data)}")
print(f"最大值: {np.max(data)}")
print(f"平均值: {np.mean(data)}")
print(f"中位数: {np.median(data)}")
print(f"标准差: {np.std(data)}")
print(f"方差: {np.var(data)}")
print(f"总和: {np.sum(data)}")

# 按轴统计
print(f"按行求和: {np.sum(data, axis=1)}")
print(f"按列求和: {np.sum(data, axis=0)}")
print(f"按列平均: {np.mean(data, axis=0)}")
```

## 6. 广播机制

广播（Broadcasting）是NumPy中一个强大的特性，允许不同形状的数组进行运算。

```python
# 标量与数组
arr = np.array([[1, 2, 3], [4, 5, 6]])
result = arr + 10
print(f"数组+标量:\n{result}")

# 一维数组与二维数组
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
arr1d = np.array([10, 20, 30])
result = arr2d + arr1d
print(f"2D+1D广播:\n{result}")

# 不同形状的二维数组
arr1 = np.array([[1], [2], [3]])
arr2 = np.array([10, 20, 30])
result = arr1 + arr2
print(f"广播结果:\n{result}")
```

## 7. 线性代数

```python
# 矩阵乘法
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# 矩阵乘法
matrix_mult = np.dot(A, B)
print(f"矩阵乘法:\n{matrix_mult}")

# 或使用@操作符
matrix_mult2 = A @ B
print(f"@操作符:\n{matrix_mult2}")

# 矩阵的逆
inverse = np.linalg.inv(A)
print(f"矩阵的逆:\n{inverse}")

# 特征值和特征向量
eigenvalues, eigenvectors = np.linalg.eig(A)
print(f"特征值: {eigenvalues}")
print(f"特征向量:\n{eigenvectors}")

# 行列式
det = np.linalg.det(A)
print(f"行列式: {det}")
```

## 8. 实际应用示例

### 8.1 股票数据分析

```python
# 模拟股票价格数据
np.random.seed(42)
days = 30
prices = 100 + np.cumsum(np.random.randn(days) * 2)

print(f"股票价格前10天: {prices[:10]}")

# 计算日收益率
returns = (prices[1:] - prices[:-1]) / prices[:-1] * 100
print(f"日收益率前5天: {returns[:5]}")

# 计算移动平均线
window = 5
moving_avg = np.convolve(prices, np.ones(window)/window, mode='valid')
print(f"5日移动平均线前5个值: {moving_avg[:5]}")

# 统计分析
print(f"平均价格: {np.mean(prices):.2f}")
print(f"价格标准差: {np.std(prices):.2f}")
print(f"最高价: {np.max(prices):.2f}")
print(f"最低价: {np.min(prices):.2f}")
print(f"平均日收益率: {np.mean(returns):.2f}%")
print(f"收益率波动率: {np.std(returns):.2f}%")
```

### 8.2 图像处理基础

```python
# 创建一个简单的"图像"（二维数组）
image = np.random.randint(0, 256, (10, 10))
print(f"原始图像:\n{image}")

# 图像亮度调整
brighter = np.clip(image + 50, 0, 255)
print(f"增加亮度后:\n{brighter}")

# 图像对比度调整
contrast = np.clip(image * 1.5, 0, 255)
print(f"增加对比度后:\n{contrast}")

# 图像翻转
flipped = np.flipud(image)  # 上下翻转
print(f"上下翻转:\n{flipped}")
```

## 9. 性能优化技巧

### 9.1 向量化操作

```python
import time

# 比较Python循环和NumPy向量化的性能
size = 1000000

# Python循环方式
start_time = time.time()
result_loop = []
for i in range(size):
    result_loop.append(i ** 2)
loop_time = time.time() - start_time

# NumPy向量化方式
start_time = time.time()
arr = np.arange(size)
result_numpy = arr ** 2
numpy_time = time.time() - start_time

print(f"Python循环时间: {loop_time:.4f}秒")
print(f"NumPy向量化时间: {numpy_time:.4f}秒")
print(f"NumPy快了: {loop_time/numpy_time:.1f}倍")
```

### 9.2 内存使用优化

```python
# 使用视图而不是副本
arr = np.arange(1000000)

# 创建视图（不复制数据）
view = arr[::2]
print(f"视图与原数组共享内存: {np.shares_memory(arr, view)}")

# 创建副本（复制数据）
copy = arr[::2].copy()
print(f"副本与原数组共享内存: {np.shares_memory(arr, copy)}")

# 就地操作
arr += 1  # 就地加法，不创建新数组
```

## 10. 常见错误和注意事项

### 10.1 数组维度错误

```python
# 错误示例：维度不匹配
try:
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([1, 2, 3])
    result = arr1 + arr2  # 这会引发错误
except ValueError as e:
    print(f"维度错误: {e}")

# 正确做法：确保维度兼容
arr2_correct = np.array([1, 2])
result = arr1 + arr2_correct
print(f"正确的广播:\n{result}")
```

### 10.2 数据类型问题

```python
# 整数除法可能导致精度丢失
int_arr = np.array([1, 2, 3], dtype=int)
result_int = int_arr / 2
print(f"整数数组除法: {result_int}, 类型: {result_int.dtype}")

# 显式指定浮点类型
float_arr = np.array([1, 2, 3], dtype=float)
result_float = float_arr / 2
print(f"浮点数组除法: {result_float}, 类型: {result_float.dtype}")
```

## 11. 总结

NumPy是Python数据科学的基石，掌握以下核心概念：

1. **数组创建**：使用各种方法创建不同类型的数组
2. **索引切片**：灵活访问和修改数组元素
3. **形状操作**：改变数组形状、拼接和分割
4. **数学运算**：向量化的高效计算
5. **广播机制**：不同形状数组间的运算
6. **统计分析**：各种统计函数的使用

### 学习建议

1. **多练习**：NumPy的精髓在于实践
2. **理解广播**：这是NumPy最强大的特性之一
3. **关注性能**：学会使用向量化操作
4. **阅读文档**：NumPy文档非常详细
5. **结合应用**：在实际项目中使用NumPy

### 下一步学习

完成NumPy学习后，建议继续学习：
- **Pandas**：数据分析和处理
- **Matplotlib**：数据可视化
- **Scikit-learn**：机器学习

这些库都建立在NumPy的基础之上，掌握NumPy将为后续学习打下坚实基础。