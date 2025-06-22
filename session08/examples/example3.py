#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session08 示例3：特殊方法（魔法方法）

本示例演示了：
- __str__ 和 __repr__ 方法
- 比较运算符重载（__eq__, __lt__, __gt__ 等）
- 算术运算符重载（__add__, __sub__, __mul__ 等）
- 其他常用特殊方法
"""

import math


class Vector2D:
    """二维向量类 - 演示特殊方法的使用"""
    
    def __init__(self, x, y):
        """初始化向量"""
        self.x = x
        self.y = y
    
    def __str__(self):
        """用户友好的字符串表示"""
        return f"向量({self.x}, {self.y})"
    
    def __repr__(self):
        """开发者友好的字符串表示"""
        return f"Vector2D({self.x}, {self.y})"
    
    def __eq__(self, other):
        """相等比较 =="""
        if isinstance(other, Vector2D):
            return self.x == other.x and self.y == other.y
        return False
    
    def __ne__(self, other):
        """不等比较 !="""
        return not self.__eq__(other)
    
    def __lt__(self, other):
        """小于比较 < （按向量长度比较）"""
        if isinstance(other, Vector2D):
            return self.magnitude() < other.magnitude()
        return NotImplemented
    
    def __le__(self, other):
        """小于等于比较 <="""
        if isinstance(other, Vector2D):
            return self.magnitude() <= other.magnitude()
        return NotImplemented
    
    def __gt__(self, other):
        """大于比较 >"""
        if isinstance(other, Vector2D):
            return self.magnitude() > other.magnitude()
        return NotImplemented
    
    def __ge__(self, other):
        """大于等于比较 >="""
        if isinstance(other, Vector2D):
            return self.magnitude() >= other.magnitude()
        return NotImplemented
    
    def __add__(self, other):
        """向量加法 +"""
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __sub__(self, other):
        """向量减法 -"""
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    def __mul__(self, scalar):
        """向量数乘 *"""
        if isinstance(scalar, (int, float)):
            return Vector2D(self.x * scalar, self.y * scalar)
        return NotImplemented
    
    def __rmul__(self, scalar):
        """右乘法（支持 scalar * vector）"""
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar):
        """向量除法 /"""
        if isinstance(scalar, (int, float)) and scalar != 0:
            return Vector2D(self.x / scalar, self.y / scalar)
        return NotImplemented
    
    def __neg__(self):
        """取负 -vector"""
        return Vector2D(-self.x, -self.y)
    
    def __abs__(self):
        """绝对值（向量长度）"""
        return self.magnitude()
    
    def __bool__(self):
        """布尔值（零向量为False，其他为True）"""
        return self.x != 0 or self.y != 0
    
    def __len__(self):
        """长度（维度数）"""
        return 2
    
    def __getitem__(self, index):
        """索引访问 vector[0] 或 vector[1]"""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("向量索引超出范围")
    
    def __setitem__(self, index, value):
        """索引赋值 vector[0] = value"""
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("向量索引超出范围")
    
    def __iter__(self):
        """迭代器支持"""
        yield self.x
        yield self.y
    
    def __contains__(self, value):
        """成员测试 value in vector"""
        return value == self.x or value == self.y
    
    def magnitude(self):
        """计算向量长度"""
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    def normalize(self):
        """归一化向量"""
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)
    
    def dot_product(self, other):
        """点积"""
        if isinstance(other, Vector2D):
            return self.x * other.x + self.y * other.y
        return NotImplemented
    
    def angle_with(self, other):
        """与另一个向量的夹角（弧度）"""
        if isinstance(other, Vector2D):
            dot = self.dot_product(other)
            mag_product = self.magnitude() * other.magnitude()
            if mag_product == 0:
                return 0
            return math.acos(max(-1, min(1, dot / mag_product)))
        return NotImplemented


class BankAccount:
    """银行账户类 - 演示更多特殊方法"""
    
    def __init__(self, account_number, owner, balance=0):
        """初始化账户"""
        self.account_number = account_number
        self.owner = owner
        self.balance = balance
        self.transaction_history = []
    
    def __str__(self):
        """字符串表示"""
        return f"账户{self.account_number}（{self.owner}）：余额 ¥{self.balance:.2f}"
    
    def __repr__(self):
        """开发者字符串表示"""
        return f"BankAccount('{self.account_number}', '{self.owner}', {self.balance})"
    
    def __eq__(self, other):
        """账户相等比较（按账户号）"""
        if isinstance(other, BankAccount):
            return self.account_number == other.account_number
        return False
    
    def __lt__(self, other):
        """账户比较（按余额）"""
        if isinstance(other, BankAccount):
            return self.balance < other.balance
        return NotImplemented
    
    def __add__(self, amount):
        """存款操作 account + amount"""
        if isinstance(amount, (int, float)) and amount > 0:
            new_account = BankAccount(self.account_number, self.owner, self.balance + amount)
            new_account.transaction_history = self.transaction_history.copy()
            new_account.transaction_history.append(f"存款 ¥{amount:.2f}")
            return new_account
        return NotImplemented
    
    def __sub__(self, amount):
        """取款操作 account - amount"""
        if isinstance(amount, (int, float)) and amount > 0:
            if self.balance >= amount:
                new_account = BankAccount(self.account_number, self.owner, self.balance - amount)
                new_account.transaction_history = self.transaction_history.copy()
                new_account.transaction_history.append(f"取款 ¥{amount:.2f}")
                return new_account
            else:
                raise ValueError("余额不足")
        return NotImplemented
    
    def __iadd__(self, amount):
        """原地存款 account += amount"""
        if isinstance(amount, (int, float)) and amount > 0:
            self.balance += amount
            self.transaction_history.append(f"存款 ¥{amount:.2f}")
            return self
        return NotImplemented
    
    def __isub__(self, amount):
        """原地取款 account -= amount"""
        if isinstance(amount, (int, float)) and amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                self.transaction_history.append(f"取款 ¥{amount:.2f}")
                return self
            else:
                raise ValueError("余额不足")
        return NotImplemented
    
    def __bool__(self):
        """布尔值（有余额为True）"""
        return self.balance > 0
    
    def __len__(self):
        """交易记录数量"""
        return len(self.transaction_history)
    
    def __getitem__(self, index):
        """获取交易记录"""
        return self.transaction_history[index]
    
    def __contains__(self, transaction):
        """检查是否包含某个交易"""
        return transaction in self.transaction_history


def main():
    """主函数"""
    print("示例3：特殊方法（魔法方法）")
    print("=" * 40)
    
    # 1. 向量类演示
    print("\n1. 向量类演示：")
    print("-" * 20)
    
    # 创建向量
    v1 = Vector2D(3, 4)
    v2 = Vector2D(1, 2)
    v3 = Vector2D(3, 4)
    
    print(f"v1 = {v1}")  # 调用 __str__
    print(f"v2 = {v2}")
    print(f"repr(v1) = {repr(v1)}")  # 调用 __repr__
    
    # 比较操作
    print(f"\nv1 == v3: {v1 == v3}")  # True
    print(f"v1 == v2: {v1 == v2}")  # False
    print(f"v1 != v2: {v1 != v2}")  # True
    print(f"v1 > v2: {v1 > v2}")   # True (按长度比较)
    print(f"v1 < v2: {v1 < v2}")   # False
    
    # 算术操作
    print(f"\nv1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 2 = {v1 * 2}")
    print(f"3 * v2 = {3 * v2}")  # 调用 __rmul__
    print(f"v1 / 2 = {v1 / 2}")
    print(f"-v1 = {-v1}")  # 调用 __neg__
    
    # 其他操作
    print(f"\nabs(v1) = {abs(v1):.2f}")  # 向量长度
    print(f"bool(v1) = {bool(v1)}")  # True
    print(f"bool(Vector2D(0, 0)) = {bool(Vector2D(0, 0))}")  # False
    print(f"len(v1) = {len(v1)}")  # 维度数
    
    # 索引访问
    print(f"\nv1[0] = {v1[0]}")  # x坐标
    print(f"v1[1] = {v1[1]}")  # y坐标
    v1[0] = 5  # 修改x坐标
    print(f"修改后 v1 = {v1}")
    
    # 迭代和成员测试
    print(f"\n遍历v2: {list(v2)}")
    print(f"4 in v1: {4 in v1}")
    print(f"10 in v1: {10 in v1}")
    
    # 向量运算
    print(f"\nv1长度: {v1.magnitude():.2f}")
    print(f"v1归一化: {v1.normalize()}")
    print(f"v1·v2 = {v1.dot_product(v2):.2f}")
    print(f"v1与v2夹角: {math.degrees(v1.angle_with(v2)):.2f}度")
    
    # 2. 银行账户类演示
    print("\n\n2. 银行账户类演示：")
    print("-" * 20)
    
    # 创建账户
    account1 = BankAccount("123456", "张三", 1000)
    account2 = BankAccount("789012", "李四", 500)
    account3 = BankAccount("123456", "张三", 2000)  # 同一账户号
    
    print(f"account1: {account1}")
    print(f"account2: {account2}")
    print(f"repr(account1): {repr(account1)}")
    
    # 比较操作
    print(f"\naccount1 == account3: {account1 == account3}")  # True（同账户号）
    print(f"account1 < account2: {account1 < account2}")   # False（按余额比较）
    print(f"account2 < account1: {account2 < account1}")   # True
    
    # 存取款操作（返回新对象）
    print(f"\n存取款操作（返回新对象）：")
    new_account1 = account1 + 200  # 存款
    print(f"account1 + 200: {new_account1}")
    
    new_account2 = account1 - 100  # 取款
    print(f"account1 - 100: {new_account2}")
    
    print(f"原account1未变: {account1}")
    
    # 原地存取款操作
    print(f"\n原地存取款操作：")
    print(f"操作前: {account2}")
    account2 += 300  # 原地存款
    print(f"account2 += 300: {account2}")
    account2 -= 150  # 原地取款
    print(f"account2 -= 150: {account2}")
    
    # 其他操作
    print(f"\nbool(account1): {bool(account1)}")  # True（有余额）
    print(f"len(account2): {len(account2)}")  # 交易记录数
    
    # 交易记录
    print(f"\n交易记录：")
    for i in range(len(account2)):
        print(f"  {i}: {account2[i]}")
    
    print(f"\n'存款 ¥300.00' in account2: {'存款 ¥300.00' in account2}")
    
    # 异常处理
    print(f"\n异常处理演示：")
    try:
        account1 - 2000  # 余额不足
    except ValueError as e:
        print(f"取款失败: {e}")
    
    try:
        print(v1[5])  # 索引超出范围
    except IndexError as e:
        print(f"索引错误: {e}")


if __name__ == "__main__":
    main()