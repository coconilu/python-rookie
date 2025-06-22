#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exercise 2: 自定义模块练习

练习目标：
1. 学会创建自定义模块
2. 理解模块的结构和组织
3. 掌握模块文档和测试
4. 练习模块的导入和使用

请完成以下练习题
"""

# 练习1：创建数学工具模块
def exercise_1_create_math_module():
    """
    练习1：创建数学工具模块
    
    任务：
    1. 在下面的MathTools类中实现各种数学函数
    2. 添加适当的文档字符串
    3. 实现错误处理
    4. 测试所有函数
    """
    print("=== 练习1：创建数学工具模块 ===")
    
    class MathTools:
        """
        数学工具模块
        提供常用的数学计算功能
        """
        
        # 模块信息
        __version__ = "1.0.0"
        __author__ = "你的姓名"
        
        @staticmethod
        def factorial(n):
            """
            计算阶乘
            
            Args:
                n (int): 非负整数
            
            Returns:
                int: n的阶乘
            
            Raises:
                ValueError: 当n为负数时
                TypeError: 当n不是整数时
            """
            # TODO: 实现阶乘计算
            # 1. 检查输入类型和值
            # 2. 实现阶乘计算
            # 3. 返回结果
            pass
        
        @staticmethod
        def gcd(a, b):
            """
            计算最大公约数（使用欧几里得算法）
            
            Args:
                a (int): 第一个整数
                b (int): 第二个整数
            
            Returns:
                int: a和b的最大公约数
            """
            # TODO: 实现最大公约数计算
            # 提示：使用欧几里得算法
            pass
        
        @staticmethod
        def lcm(a, b):
            """
            计算最小公倍数
            
            Args:
                a (int): 第一个整数
                b (int): 第二个整数
            
            Returns:
                int: a和b的最小公倍数
            """
            # TODO: 实现最小公倍数计算
            # 提示：lcm(a,b) = abs(a*b) / gcd(a,b)
            pass
        
        @staticmethod
        def is_prime(n):
            """
            判断是否为质数
            
            Args:
                n (int): 要检查的整数
            
            Returns:
                bool: 如果是质数返回True，否则返回False
            """
            # TODO: 实现质数判断
            # 1. 处理特殊情况（小于2的数）
            # 2. 检查是否能被2到sqrt(n)之间的数整除
            pass
        
        @staticmethod
        def prime_factors(n):
            """
            计算质因数分解
            
            Args:
                n (int): 要分解的正整数
            
            Returns:
                list: 质因数列表
            """
            # TODO: 实现质因数分解
            pass
        
        @staticmethod
        def fibonacci_sequence(n):
            """
            生成斐波那契数列
            
            Args:
                n (int): 数列长度
            
            Returns:
                list: 斐波那契数列
            """
            # TODO: 实现斐波那契数列生成
            pass
        
        @staticmethod
        def power_mod(base, exponent, modulus):
            """
            计算模幂运算：(base^exponent) % modulus
            使用快速幂算法提高效率
            
            Args:
                base (int): 底数
                exponent (int): 指数
                modulus (int): 模数
            
            Returns:
                int: 模幂运算结果
            """
            # TODO: 实现快速幂算法
            # 提示：可以使用Python内置的pow(base, exponent, modulus)
            # 或者自己实现快速幂算法
            pass
    
    # 测试数学工具模块
    print("测试MathTools模块:")
    
    # TODO: 测试所有函数
    # 测试阶乘
    # test_numbers = [0, 1, 5, 10]
    # print("阶乘测试:")
    # for num in test_numbers:
    #     try:
    #         result = MathTools.factorial(num)
    #         print(f"  {num}! = {result}")
    #     except Exception as e:
    #         print(f"  {num}!: 错误 - {e}")
    
    # 测试最大公约数和最小公倍数
    # test_pairs = [(12, 18), (15, 25), (7, 13)]
    # print("\n最大公约数和最小公倍数测试:")
    # for a, b in test_pairs:
    #     gcd_result = MathTools.gcd(a, b)
    #     lcm_result = MathTools.lcm(a, b)
    #     print(f"  gcd({a}, {b}) = {gcd_result}, lcm({a}, {b}) = {lcm_result}")
    
    # 测试质数判断
    # test_primes = [2, 3, 4, 17, 25, 29]
    # print("\n质数判断测试:")
    # for num in test_primes:
    #     is_prime = MathTools.is_prime(num)
    #     print(f"  {num}: {'是' if is_prime else '不是'}质数")
    
    print("练习1完成！\n")


# 练习2：创建字符串处理模块
def exercise_2_create_string_module():
    """
    练习2：创建字符串处理模块
    
    任务：
    1. 实现各种字符串处理功能
    2. 添加输入验证和错误处理
    3. 提供多种处理选项
    """
    print("=== 练习2：创建字符串处理模块 ===")
    
    class StringProcessor:
        """
        字符串处理模块
        提供各种字符串操作和分析功能
        """
        
        @staticmethod
        def word_count(text):
            """
            统计文本中的单词数量
            
            Args:
                text (str): 要分析的文本
            
            Returns:
                dict: 包含各种统计信息的字典
            """
            # TODO: 实现单词统计
            # 返回字典应包含：
            # - total_words: 总单词数
            # - unique_words: 唯一单词数
            # - word_frequency: 单词频率字典
            # - average_word_length: 平均单词长度
            pass
        
        @staticmethod
        def reverse_words(text, reverse_order=False):
            """
            反转单词
            
            Args:
                text (str): 输入文本
                reverse_order (bool): 是否反转单词顺序
            
            Returns:
                str: 处理后的文本
            """
            # TODO: 实现单词反转
            # 如果reverse_order为True，反转单词顺序
            # 否则，反转每个单词内的字符顺序
            pass
        
        @staticmethod
        def extract_numbers(text):
            """
            从文本中提取所有数字
            
            Args:
                text (str): 输入文本
            
            Returns:
                dict: 包含整数和浮点数列表的字典
            """
            # TODO: 实现数字提取
            # 使用正则表达式提取整数和浮点数
            # 返回格式：{'integers': [...], 'floats': [...]}
            pass
        
        @staticmethod
        def text_statistics(text):
            """
            计算文本统计信息
            
            Args:
                text (str): 输入文本
            
            Returns:
                dict: 详细的文本统计信息
            """
            # TODO: 实现文本统计
            # 统计信息应包括：
            # - 字符总数（包含空格）
            # - 字符总数（不含空格）
            # - 单词数
            # - 句子数
            # - 段落数
            # - 平均单词长度
            # - 平均句子长度
            pass
        
        @staticmethod
        def format_text(text, style='title'):
            """
            格式化文本
            
            Args:
                text (str): 输入文本
                style (str): 格式化样式
                    - 'title': 标题格式（每个单词首字母大写）
                    - 'sentence': 句子格式（每个句子首字母大写）
                    - 'camel': 驼峰格式
                    - 'snake': 下划线格式
                    - 'kebab': 短横线格式
            
            Returns:
                str: 格式化后的文本
            """
            # TODO: 实现文本格式化
            pass
        
        @staticmethod
        def similarity(text1, text2, method='jaccard'):
            """
            计算两个文本的相似度
            
            Args:
                text1 (str): 第一个文本
                text2 (str): 第二个文本
                method (str): 相似度计算方法
                    - 'jaccard': Jaccard相似度
                    - 'cosine': 余弦相似度（简化版）
            
            Returns:
                float: 相似度值（0-1之间）
            """
            # TODO: 实现相似度计算
            pass
    
    # 测试字符串处理模块
    print("测试StringProcessor模块:")
    
    # TODO: 测试所有函数
    # test_text = "Hello World! This is a test. Python is great for text processing."
    
    # 测试单词统计
    # word_stats = StringProcessor.word_count(test_text)
    # print(f"单词统计: {word_stats}")
    
    # 测试文本反转
    # reversed_chars = StringProcessor.reverse_words(test_text, reverse_order=False)
    # reversed_order = StringProcessor.reverse_words(test_text, reverse_order=True)
    # print(f"\n字符反转: {reversed_chars}")
    # print(f"顺序反转: {reversed_order}")
    
    print("练习2完成！\n")


# 练习3：创建文件工具模块
def exercise_3_create_file_module():
    """
    练习3：创建文件工具模块
    
    任务：
    1. 实现文件操作功能
    2. 添加安全检查
    3. 提供文件分析功能
    """
    print("=== 练习3：创建文件工具模块 ===")
    
    class FileTools:
        """
        文件工具模块
        提供安全的文件操作和分析功能
        """
        
        @staticmethod
        def safe_read(file_path, encoding='utf-8'):
            """
            安全地读取文件内容
            
            Args:
                file_path (str): 文件路径
                encoding (str): 文件编码
            
            Returns:
                dict: 包含内容和状态信息的字典
            """
            # TODO: 实现安全文件读取
            # 返回格式：
            # {
            #     'success': bool,
            #     'content': str or None,
            #     'error': str or None,
            #     'file_info': dict
            # }
            pass
        
        @staticmethod
        def analyze_file(file_path):
            """
            分析文件信息
            
            Args:
                file_path (str): 文件路径
            
            Returns:
                dict: 文件分析结果
            """
            # TODO: 实现文件分析
            # 分析信息应包括：
            # - 文件大小
            # - 创建时间
            # - 修改时间
            # - 文件类型
            # - 行数（如果是文本文件）
            # - 字符数（如果是文本文件）
            pass
        
        @staticmethod
        def backup_file(file_path, backup_dir=None):
            """
            备份文件
            
            Args:
                file_path (str): 要备份的文件路径
                backup_dir (str): 备份目录，如果为None则在原目录创建备份
            
            Returns:
                dict: 备份操作结果
            """
            # TODO: 实现文件备份
            # 备份文件名格式：原文件名_backup_时间戳.扩展名
            pass
        
        @staticmethod
        def find_files(directory, pattern='*', recursive=True):
            """
            查找文件
            
            Args:
                directory (str): 搜索目录
                pattern (str): 文件名模式
                recursive (bool): 是否递归搜索
            
            Returns:
                list: 找到的文件列表
            """
            # TODO: 实现文件查找
            # 使用glob模块进行模式匹配
            pass
        
        @staticmethod
        def compare_files(file1, file2):
            """
            比较两个文件
            
            Args:
                file1 (str): 第一个文件路径
                file2 (str): 第二个文件路径
            
            Returns:
                dict: 比较结果
            """
            # TODO: 实现文件比较
            # 比较内容：
            # - 文件大小是否相同
            # - 内容是否相同
            # - 如果不同，显示差异统计
            pass
    
    # 测试文件工具模块
    print("测试FileTools模块:")
    
    # TODO: 测试文件工具功能
    # 注意：这里只做演示，不实际操作文件
    
    print("文件工具模块功能演示（仅演示，不实际执行）:")
    print("1. 安全读取文件: FileTools.safe_read('example.txt')")
    print("2. 分析文件信息: FileTools.analyze_file('example.txt')")
    print("3. 备份文件: FileTools.backup_file('important.txt')")
    print("4. 查找文件: FileTools.find_files('.', '*.py')")
    print("5. 比较文件: FileTools.compare_files('file1.txt', 'file2.txt')")
    
    print("练习3完成！\n")


# 练习4：模块测试和文档
def exercise_4_module_testing():
    """
    练习4：模块测试和文档
    
    任务：
    1. 为模块编写测试函数
    2. 添加详细的文档字符串
    3. 实现模块的使用示例
    """
    print("=== 练习4：模块测试和文档 ===")
    
    # 简单的测试框架
    class SimpleTestFramework:
        """
        简单的测试框架
        """
        
        def __init__(self):
            self.tests_run = 0
            self.tests_passed = 0
            self.tests_failed = 0
        
        def assert_equal(self, actual, expected, message=""):
            """
            断言两个值相等
            """
            self.tests_run += 1
            if actual == expected:
                self.tests_passed += 1
                print(f"  ✓ 测试通过: {message}")
            else:
                self.tests_failed += 1
                print(f"  ✗ 测试失败: {message}")
                print(f"    期望: {expected}")
                print(f"    实际: {actual}")
        
        def assert_true(self, condition, message=""):
            """
            断言条件为真
            """
            self.assert_equal(condition, True, message)
        
        def assert_false(self, condition, message=""):
            """
            断言条件为假
            """
            self.assert_equal(condition, False, message)
        
        def run_test(self, test_func, test_name):
            """
            运行单个测试
            """
            print(f"\n运行测试: {test_name}")
            try:
                test_func(self)
            except Exception as e:
                self.tests_failed += 1
                print(f"  ✗ 测试异常: {e}")
        
        def summary(self):
            """
            打印测试摘要
            """
            print(f"\n=== 测试摘要 ===")
            print(f"总测试数: {self.tests_run}")
            print(f"通过: {self.tests_passed}")
            print(f"失败: {self.tests_failed}")
            print(f"成功率: {self.tests_passed/self.tests_run*100:.1f}%" if self.tests_run > 0 else "无测试")
    
    # TODO: 为之前创建的模块编写测试
    def test_math_tools(tester):
        """
        测试数学工具模块
        """
        # 这里应该测试MathTools类的各个方法
        # 例如：
        # tester.assert_equal(MathTools.factorial(5), 120, "5的阶乘应该是120")
        # tester.assert_equal(MathTools.gcd(12, 18), 6, "12和18的最大公约数应该是6")
        # tester.assert_true(MathTools.is_prime(17), "17应该是质数")
        # tester.assert_false(MathTools.is_prime(15), "15不应该是质数")
        
        print("  数学工具测试需要先完成练习1的实现")
    
    def test_string_processor(tester):
        """
        测试字符串处理模块
        """
        # 这里应该测试StringProcessor类的各个方法
        print("  字符串处理测试需要先完成练习2的实现")
    
    def test_file_tools(tester):
        """
        测试文件工具模块
        """
        # 这里应该测试FileTools类的各个方法
        print("  文件工具测试需要先完成练习3的实现")
    
    # 运行测试
    tester = SimpleTestFramework()
    
    tester.run_test(test_math_tools, "数学工具模块测试")
    tester.run_test(test_string_processor, "字符串处理模块测试")
    tester.run_test(test_file_tools, "文件工具模块测试")
    
    tester.summary()
    
    print("\n练习4完成！\n")


# 练习5：模块文档和帮助
def exercise_5_module_documentation():
    """
    练习5：模块文档和帮助
    
    任务：
    1. 学习如何编写好的模块文档
    2. 了解Python文档字符串的规范
    3. 实现帮助系统
    """
    print("=== 练习5：模块文档和帮助 ===")
    
    class DocumentedModule:
        """
        文档化模块示例
        
        这个模块演示了如何编写良好的文档字符串。
        
        Attributes:
            VERSION (str): 模块版本号
            AUTHOR (str): 模块作者
            DESCRIPTION (str): 模块描述
        
        Example:
            >>> dm = DocumentedModule()
            >>> result = dm.example_function("hello")
            >>> print(result)
            Hello, hello!
        """
        
        VERSION = "1.0.0"
        AUTHOR = "Python学习者"
        DESCRIPTION = "演示模块文档的示例模块"
        
        def __init__(self):
            """
            初始化文档化模块
            
            创建一个新的DocumentedModule实例。
            """
            self.initialized = True
        
        def example_function(self, text):
            """
            示例函数，演示函数文档的写法
            
            这个函数接受一个字符串参数，并返回格式化的问候语。
            
            Args:
                text (str): 要处理的文本字符串
            
            Returns:
                str: 格式化的问候语
            
            Raises:
                TypeError: 当text不是字符串时抛出
                ValueError: 当text为空字符串时抛出
            
            Example:
                >>> dm = DocumentedModule()
                >>> result = dm.example_function("world")
                >>> print(result)
                Hello, world!
                
                >>> dm.example_function("")
                Traceback (most recent call last):
                    ...
                ValueError: 文本不能为空
            
            Note:
                这个函数主要用于演示文档字符串的格式。
                在实际项目中，应该根据具体需求编写更有意义的函数。
            
            See Also:
                help_function: 获取模块帮助信息
            """
            # TODO: 实现函数逻辑
            # 1. 检查输入参数
            # 2. 处理文本
            # 3. 返回结果
            pass
        
        def help_function(self):
            """
            显示模块帮助信息
            
            Returns:
                str: 模块的帮助信息
            """
            help_text = f"""
{self.__class__.__name__} 帮助信息
{'=' * 40}

版本: {self.VERSION}
作者: {self.AUTHOR}
描述: {self.DESCRIPTION}

可用方法:
- example_function(text): 示例函数
- help_function(): 显示帮助信息
- get_module_info(): 获取模块信息

使用示例:
    >>> dm = DocumentedModule()
    >>> dm.example_function("Python")
    >>> dm.help_function()

更多信息请使用 help(DocumentedModule) 查看详细文档。
            """
            return help_text
        
        def get_module_info(self):
            """
            获取模块信息
            
            Returns:
                dict: 包含模块信息的字典
            """
            return {
                'name': self.__class__.__name__,
                'version': self.VERSION,
                'author': self.AUTHOR,
                'description': self.DESCRIPTION,
                'methods': [method for method in dir(self) if not method.startswith('_')]
            }
    
    # 演示文档功能
    print("文档化模块演示:")
    
    # 创建模块实例
    dm = DocumentedModule()
    
    # 显示模块信息
    info = dm.get_module_info()
    print(f"模块名称: {info['name']}")
    print(f"版本: {info['version']}")
    print(f"作者: {info['author']}")
    print(f"可用方法: {', '.join(info['methods'])}")
    
    # 显示帮助信息
    print("\n" + dm.help_function())
    
    # TODO: 演示如何使用Python内置的help()函数
    print("\n使用内置help()函数的示例:")
    print("help(DocumentedModule)  # 显示类的完整文档")
    print("help(DocumentedModule.example_function)  # 显示方法文档")
    
    print("练习5完成！\n")


def main():
    """
    主函数 - 运行所有练习
    """
    print("Session10 - Exercise2: 自定义模块练习")
    print("=" * 60)
    
    # 运行所有练习
    exercise_1_create_math_module()
    exercise_2_create_string_module()
    exercise_3_create_file_module()
    exercise_4_module_testing()
    exercise_5_module_documentation()
    
    print("=" * 60)
    print("所有练习完成！")
    print("\n自定义模块开发要点:")
    print("1. 模块应该有明确的功能和职责")
    print("2. 函数和类应该有详细的文档字符串")
    print("3. 添加适当的错误处理和输入验证")
    print("4. 为模块编写测试用例")
    print("5. 遵循Python编码规范（PEP 8）")
    print("6. 提供使用示例和帮助信息")
    
    print("\n下一步建议:")
    print("- 完成所有TODO标记的代码实现")
    print("- 为每个函数编写完整的测试用例")
    print("- 尝试将模块保存为独立的.py文件")
    print("- 在其他脚本中导入和使用你的模块")


if __name__ == "__main__":
    main()