"""
练习 14.1：基础HTTP请求练习

任务描述：
编写一个程序，从指定的API获取数据并进行简单处理。

要求：
1. 使用urllib或requests库发送GET请求到 http://httpbin.org/uuid
2. 该API会返回一个随机的UUID（通用唯一识别码）
3. 提取返回的UUID并显示出来
4. 连续获取5个UUID，并将它们存储在列表中
5. 统计这5个UUID中包含数字'0'的个数

示例输出：
获取的UUID列表：
1. 550e8400-e29b-41d4-a716-446655440000
2. 6ba7b810-9dad-11d1-80b4-00c04fd430c8
3. 6ba7b811-9dad-11d1-80b4-00c04fd430c8
4. 6ba7b812-9dad-11d1-80b4-00c04fd430c8
5. 6ba7b814-9dad-11d1-80b4-00c04fd430c8

包含数字'0'的UUID个数：5个

提示：
- UUID API返回的数据格式是JSON
- 可以使用json.loads()解析JSON数据
- UUID在返回的JSON中的键是'uuid'
- 使用循环来获取多个UUID
- 可以使用字符串的count()方法统计字符出现次数
"""

import json

# 尝试导入requests，如果没有则使用urllib
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    HAS_REQUESTS = False


def get_uuid():
    """
    从API获取一个UUID
    
    返回:
        str: UUID字符串，如果失败返回None
    """
    url = "http://httpbin.org/uuid"
    
    # TODO: 在这里实现获取UUID的代码
    # 提示：
    # 1. 发送GET请求到url
    # 2. 解析返回的JSON数据
    # 3. 提取uuid字段的值
    # 4. 处理可能的异常
    
    pass


def get_multiple_uuids(count):
    """
    获取多个UUID
    
    参数:
        count: 要获取的UUID数量
    
    返回:
        list: UUID列表
    """
    uuids = []
    
    # TODO: 在这里实现获取多个UUID的代码
    # 提示：
    # 1. 使用循环调用get_uuid()函数
    # 2. 将获取的UUID添加到列表中
    # 3. 处理可能的None值
    
    return uuids


def count_zeros_in_uuids(uuids):
    """
    统计UUID列表中包含数字'0'的UUID个数
    
    参数:
        uuids: UUID列表
    
    返回:
        int: 包含'0'的UUID个数
    """
    # TODO: 在这里实现统计功能
    # 提示：
    # 1. 遍历UUID列表
    # 2. 检查每个UUID是否包含'0'
    # 3. 统计包含'0'的UUID个数
    
    pass


def main():
    """主函数"""
    print("练习14.1：获取和处理UUID\n")
    
    # 获取5个UUID
    print("正在获取UUID...")
    uuids = get_multiple_uuids(5)
    
    if not uuids:
        print("获取UUID失败！")
        return
    
    # 显示获取的UUID
    print("\n获取的UUID列表：")
    for i, uuid in enumerate(uuids, 1):
        print(f"{i}. {uuid}")
    
    # 统计包含'0'的UUID个数
    zero_count = count_zeros_in_uuids(uuids)
    print(f"\n包含数字'0'的UUID个数：{zero_count}个")


# 测试代码
if __name__ == "__main__":
    main()
    
    # 额外测试：验证你的函数
    print("\n" + "="*50)
    print("函数单元测试：")
    
    # 测试get_uuid函数
    print("\n测试get_uuid()函数：")
    test_uuid = get_uuid()
    if test_uuid:
        print(f"✓ 成功获取UUID: {test_uuid}")
        print(f"  UUID长度: {len(test_uuid)}")
        print(f"  包含连字符: {'-' in test_uuid}")
    else:
        print("✗ 获取UUID失败")
    
    # 测试count_zeros_in_uuids函数
    print("\n测试count_zeros_in_uuids()函数：")
    test_list = [
        "550e8400-e29b-41d4-a716-446655440000",  # 包含'0'
        "6ba7b811-9dad-11d1-80b4-00c04fd430c8",  # 包含'0'
        "123e4567-e89b-12d3-a456-426614174111"   # 不包含'0'
    ]
    result = count_zeros_in_uuids(test_list)
    print(f"测试列表中包含'0'的UUID个数: {result}")
    print(f"✓ 预期结果: 2, 实际结果: {result}") 