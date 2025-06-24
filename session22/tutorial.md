# Session22: 测试驱动开发(TDD)

## 1. 测试驱动开发简介

### 1.1 什么是TDD

测试驱动开发(Test-Driven Development, TDD)是一种软件开发方法论，其核心思想是：**先写测试，再写代码**。

TDD的基本流程遵循"红绿重构"循环：
1. **红(Red)**：编写一个失败的测试
2. **绿(Green)**：编写最少的代码使测试通过
3. **重构(Refactor)**：改进代码质量，保持测试通过

### 1.2 TDD的优势

- **更好的代码设计**：先写测试迫使你思考接口设计
- **更高的代码质量**：测试覆盖率高，bug更少
- **更快的反馈**：及时发现问题
- **更安全的重构**：有测试保护，重构更有信心
- **活文档**：测试用例就是最好的使用说明

## 2. Python测试框架

### 2.1 unittest框架

unittest是Python标准库中的测试框架，基于xUnit架构。

#### 基本结构

```python
import unittest

class TestCalculator(unittest.TestCase):
    def setUp(self):
        """每个测试方法执行前调用"""
        self.calc = Calculator()
    
    def tearDown(self):
        """每个测试方法执行后调用"""
        pass
    
    def test_add(self):
        """测试加法功能"""
        result = self.calc.add(2, 3)
        self.assertEqual(result, 5)
    
    def test_divide_by_zero(self):
        """测试除零异常"""
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)

if __name__ == '__main__':
    unittest.main()
```

#### 常用断言方法

```python
# 相等性断言
self.assertEqual(a, b)        # a == b
self.assertNotEqual(a, b)     # a != b
self.assertTrue(x)            # bool(x) is True
self.assertFalse(x)           # bool(x) is False
self.assertIs(a, b)           # a is b
self.assertIsNot(a, b)        # a is not b
self.assertIsNone(x)          # x is None
self.assertIsNotNone(x)       # x is not None

# 包含性断言
self.assertIn(a, b)           # a in b
self.assertNotIn(a, b)        # a not in b

# 类型断言
self.assertIsInstance(a, b)   # isinstance(a, b)
self.assertNotIsInstance(a, b) # not isinstance(a, b)

# 数值断言
self.assertAlmostEqual(a, b)  # 浮点数近似相等
self.assertGreater(a, b)      # a > b
self.assertLess(a, b)         # a < b

# 异常断言
self.assertRaises(exc, fun, *args, **kwds)
self.assertRaisesRegex(exc, r, fun, *args, **kwds)
```

### 2.2 pytest框架

pytest是一个更现代、更灵活的测试框架。

#### 安装pytest

```bash
uv add --dev pytest pytest-cov
```

#### 基本用法

```python
import pytest
from calculator import Calculator

@pytest.fixture
def calc():
    """测试夹具：为测试提供Calculator实例"""
    return Calculator()

def test_add(calc):
    """测试加法功能"""
    assert calc.add(2, 3) == 5

def test_subtract(calc):
    """测试减法功能"""
    assert calc.subtract(5, 3) == 2

def test_divide_by_zero(calc):
    """测试除零异常"""
    with pytest.raises(ZeroDivisionError):
        calc.divide(10, 0)

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (10, -5, 5)
])
def test_add_parametrized(calc, a, b, expected):
    """参数化测试"""
    assert calc.add(a, b) == expected
```

#### pytest特性

1. **简单的断言**：使用Python的assert语句
2. **自动发现测试**：自动找到test_*.py文件
3. **丰富的插件生态**：pytest-cov、pytest-mock等
4. **参数化测试**：@pytest.mark.parametrize
5. **测试夹具**：@pytest.fixture提供测试数据

## 3. TDD实践：开发计算器

让我们通过TDD方式开发一个计算器类。

### 3.1 第一个测试：加法

```python
# test_calculator.py
import pytest
from calculator import Calculator

def test_add_two_numbers():
    """测试两个数字相加"""
    calc = Calculator()
    result = calc.add(2, 3)
    assert result == 5
```

运行测试（会失败，因为Calculator类还不存在）：
```bash
pytest test_calculator.py::test_add_two_numbers -v
```

### 3.2 编写最少代码使测试通过

```python
# calculator.py
class Calculator:
    def add(self, a, b):
        return a + b
```

现在测试应该通过了。

### 3.3 添加更多测试

```python
# test_calculator.py
import pytest
from calculator import Calculator

class TestCalculator:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.calc = Calculator()
    
    def test_add_positive_numbers(self):
        assert self.calc.add(2, 3) == 5
    
    def test_add_negative_numbers(self):
        assert self.calc.add(-2, -3) == -5
    
    def test_add_zero(self):
        assert self.calc.add(5, 0) == 5
        assert self.calc.add(0, 5) == 5
    
    def test_subtract(self):
        assert self.calc.subtract(5, 3) == 2
        assert self.calc.subtract(3, 5) == -2
    
    def test_multiply(self):
        assert self.calc.multiply(3, 4) == 12
        assert self.calc.multiply(-2, 3) == -6
    
    def test_divide(self):
        assert self.calc.divide(10, 2) == 5
        assert self.calc.divide(7, 2) == 3.5
    
    def test_divide_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.divide(10, 0)
```

### 3.4 完善Calculator类

```python
# calculator.py
class Calculator:
    def add(self, a, b):
        """加法运算"""
        return a + b
    
    def subtract(self, a, b):
        """减法运算"""
        return a - b
    
    def multiply(self, a, b):
        """乘法运算"""
        return a * b
    
    def divide(self, a, b):
        """除法运算"""
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b
```

## 4. Mock和测试替身

在测试中，我们经常需要隔离外部依赖，这时就需要使用Mock对象。

### 4.1 什么是Mock

Mock是一种测试替身，用来模拟真实对象的行为。

```python
from unittest.mock import Mock, patch
import requests

# 被测试的类
class WeatherService:
    def get_temperature(self, city):
        response = requests.get(f"http://api.weather.com/{city}")
        return response.json()['temperature']

# 测试代码
def test_get_temperature():
    with patch('requests.get') as mock_get:
        # 设置Mock的返回值
        mock_get.return_value.json.return_value = {'temperature': 25}
        
        service = WeatherService()
        temp = service.get_temperature('Beijing')
        
        assert temp == 25
        mock_get.assert_called_once_with('http://api.weather.com/Beijing')
```

### 4.2 pytest-mock插件

```bash
uv add --dev pytest-mock
```

```python
def test_get_temperature_with_mocker(mocker):
    # 使用mocker fixture
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.json.return_value = {'temperature': 25}
    
    service = WeatherService()
    temp = service.get_temperature('Beijing')
    
    assert temp == 25
```

## 5. 测试覆盖率

测试覆盖率衡量代码被测试覆盖的程度。

### 5.1 使用pytest-cov

```bash
# 运行测试并生成覆盖率报告
pytest --cov=calculator --cov-report=html

# 查看覆盖率
pytest --cov=calculator --cov-report=term-missing
```

### 5.2 覆盖率配置

创建`.coveragerc`文件：
```ini
[run]
source = .
omit = 
    */tests/*
    */test_*
    */__pycache__/*
    */venv/*
    */.venv/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## 6. 高级测试技巧

### 6.1 参数化测试

```python
@pytest.mark.parametrize("operation,a,b,expected", [
    ('add', 2, 3, 5),
    ('subtract', 5, 3, 2),
    ('multiply', 3, 4, 12),
    ('divide', 10, 2, 5),
])
def test_calculator_operations(operation, a, b, expected):
    calc = Calculator()
    result = getattr(calc, operation)(a, b)
    assert result == expected
```

### 6.2 测试夹具

```python
@pytest.fixture(scope="session")
def database():
    """会话级别的数据库连接"""
    db = create_test_database()
    yield db
    db.close()

@pytest.fixture
def user(database):
    """创建测试用户"""
    user = database.create_user("test@example.com")
    yield user
    database.delete_user(user.id)
```

### 6.3 异常测试

```python
def test_invalid_input():
    calc = Calculator()
    
    # 测试类型错误
    with pytest.raises(TypeError):
        calc.add("2", 3)
    
    # 测试异常消息
    with pytest.raises(ValueError, match="Invalid input"):
        calc.sqrt(-1)
```

## 7. 持续集成中的测试

### 7.1 GitHub Actions配置

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

## 8. 最佳实践

### 8.1 测试命名规范

- 测试文件：`test_*.py`或`*_test.py`
- 测试类：`TestXxx`
- 测试方法：`test_xxx`
- 描述性命名：`test_should_return_error_when_divide_by_zero`

### 8.2 测试组织

```python
class TestCalculatorBasicOperations:
    """基本运算测试"""
    
    def test_addition(self):
        pass
    
    def test_subtraction(self):
        pass

class TestCalculatorAdvancedOperations:
    """高级运算测试"""
    
    def test_power(self):
        pass
    
    def test_square_root(self):
        pass
```

### 8.3 测试数据管理

```python
# conftest.py
import pytest

@pytest.fixture
def sample_data():
    return {
        'users': [
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'}
        ]
    }
```

## 9. 常见问题和解决方案

### 9.1 测试运行缓慢

- 使用Mock隔离外部依赖
- 并行运行测试：`pytest -n auto`
- 只运行相关测试：`pytest -k "test_add"`

### 9.2 测试不稳定

- 避免依赖系统时间
- 使用固定的随机种子
- 清理测试数据

### 9.3 难以测试的代码

- 重构代码提高可测试性
- 使用依赖注入
- 分离业务逻辑和基础设施

## 10. 总结

TDD是一种强大的开发方法论，它能够：

1. **提高代码质量**：通过测试驱动设计
2. **增强信心**：重构和修改代码更安全
3. **改善设计**：迫使思考接口和职责
4. **提供文档**：测试用例就是活文档
5. **快速反馈**：及时发现问题

记住TDD的核心：**红绿重构**循环，先写测试，再写代码，最后重构优化。

## 扩展阅读

- [pytest官方文档](https://docs.pytest.org/)
- [unittest官方文档](https://docs.python.org/3/library/unittest.html)
- [《测试驱动开发》- Kent Beck](https://book.douban.com/subject/1230036/)
- [《单元测试的艺术》](https://book.douban.com/subject/25934516/)