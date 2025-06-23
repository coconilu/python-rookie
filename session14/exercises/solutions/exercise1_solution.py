"""
练习 14.1 参考答案：基础HTTP请求练习
"""

import json
import time

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
    
    try:
        if HAS_REQUESTS:
            # 使用requests库
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # 检查HTTP错误
            data = response.json()
        else:
            # 使用urllib库
            response = urllib.request.urlopen(url, timeout=5)
            content = response.read().decode('utf-8')
            data = json.loads(content)
        
        # 提取uuid字段
        uuid = data.get('uuid')
        return uuid
        
    except Exception as e:
        print(f"获取UUID失败: {e}")
        return None


def get_multiple_uuids(count):
    """
    获取多个UUID
    
    参数:
        count: 要获取的UUID数量
    
    返回:
        list: UUID列表
    """
    uuids = []
    
    for i in range(count):
        print(f"获取第 {i+1}/{count} 个UUID...")
        uuid = get_uuid()
        
        if uuid:
            uuids.append(uuid)
        else:
            print(f"警告：第 {i+1} 个UUID获取失败")
        
        # 避免请求过快
        if i < count - 1:  # 最后一个不需要等待
            time.sleep(0.5)
    
    return uuids


def count_zeros_in_uuids(uuids):
    """
    统计UUID列表中包含数字'0'的UUID个数
    
    参数:
        uuids: UUID列表
    
    返回:
        int: 包含'0'的UUID个数
    """
    count = 0
    
    for uuid in uuids:
        if '0' in uuid:
            count += 1
    
    return count


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
    
    # 额外统计信息
    print("\n额外统计：")
    for i, uuid in enumerate(uuids, 1):
        zero_count_in_uuid = uuid.count('0')
        print(f"UUID {i} 中'0'的个数: {zero_count_in_uuid}")


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