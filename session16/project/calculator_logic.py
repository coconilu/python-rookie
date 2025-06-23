#!/usr/bin/env python3
"""
计算器逻辑模块
负责计算逻辑和状态管理
"""


class CalculatorLogic:
    """计算器逻辑类"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """重置计算器状态"""
        self.current_number = "0"
        self.first_number = None
        self.operation = None
        self.new_number = True
        self.result = None
    
    def get_display(self):
        """获取显示内容"""
        return self.current_number
    
    def set_display(self, value):
        """设置显示内容"""
        self.current_number = value
    
    def clear(self):
        """清除所有"""
        self.reset()
    
    def set_operator(self, operator):
        """设置运算符"""
        current = float(self.current_number)
        
        if self.first_number is None:
            self.first_number = current
        else:
            # 如果已有运算符，先计算之前的结果
            if not self.new_number:
                self.calculate()
        
        self.operation = operator
        self.new_number = True
    
    def calculate(self):
        """执行计算"""
        if self.first_number is None or self.operation is None:
            return None
        
        try:
            second_number = float(self.current_number)
            
            # 执行运算
            if self.operation == '+':
                result = self.first_number + second_number
            elif self.operation == '-':
                result = self.first_number - second_number
            elif self.operation == '*':
                result = self.first_number * second_number
            elif self.operation == '/':
                if second_number == 0:
                    raise ValueError("除数不能为零")
                result = self.first_number / second_number
            else:
                raise ValueError(f"未知运算符: {self.operation}")
            
            # 格式化结果
            if result == int(result):
                self.current_number = str(int(result))
            else:
                # 限制小数位数
                self.current_number = f"{result:.10g}"
            
            self.result = result
            self.first_number = result
            self.new_number = True
            
            return self.current_number
            
        except Exception as e:
            self.reset()
            raise e
    
    def negate(self):
        """切换正负号"""
        if self.current_number != "0":
            if self.current_number[0] == '-':
                self.current_number = self.current_number[1:]
            else:
                self.current_number = '-' + self.current_number
    
    def percent(self):
        """百分比计算"""
        try:
            value = float(self.current_number)
            value = value / 100
            
            # 格式化结果
            if value == int(value):
                self.current_number = str(int(value))
            else:
                self.current_number = f"{value:.10g}"
            
            self.new_number = True
        except:
            pass
    
    def validate_number(self, number_str):
        """验证数字格式"""
        try:
            float(number_str)
            return True
        except:
            return False 