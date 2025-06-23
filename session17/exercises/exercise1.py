"""
练习1：路由练习
完成以下路由相关的练习
"""

from flask import Flask, url_for

app = Flask(__name__)


# 练习1：创建基本路由
# TODO: 创建一个路由 /welcome，返回 "欢迎来到Flask世界！"
# 你的代码：



# 练习2：动态路由
# TODO: 创建一个路由 /greet/<name>，返回 "你好，{name}！欢迎访问。"
# 你的代码：



# 练习3：多个参数的动态路由
# TODO: 创建一个路由 /calculate/<int:num1>/<operation>/<int:num2>
# 根据operation（add/subtract/multiply/divide）执行相应的计算并返回结果
# 例如：/calculate/10/add/5 应该返回 "10 + 5 = 15"
# 你的代码：



# 练习4：带默认值的路由
# TODO: 创建路由 /product 和 /product/<int:product_id>
# 如果没有提供product_id，显示所有产品列表
# 如果提供了product_id，显示该产品的详情
# 你的代码：



# 练习5：路径参数
# TODO: 创建一个路由 /files/<path:filepath>
# 显示文件路径信息，包括：完整路径、目录、文件名
# 例如：/files/documents/python/tutorial.pdf
# 你的代码：



# 练习6：URL构建
# TODO: 创建一个路由 /navigation
# 使用url_for生成指向上面所有路由的链接列表
# 你的代码：



# 练习7：限制HTTP方法
# TODO: 创建一个路由 /api/data
# GET请求：返回 "获取数据"
# POST请求：返回 "创建数据"
# 其他方法应该返回405错误
# 你的代码：



# 练习8：正则表达式路由（高级）
# TODO: 创建一个路由匹配电话号码格式
# 路由：/phone/<regex("\d{3}-\d{4}-\d{4}"):phone>
# 例如：/phone/138-1234-5678
# 提示：需要使用werkzeug.routing.BaseConverter
# 你的代码：



# 测试路由 - 不要修改
@app.route('/test')
def test():
    """测试路由是否正确实现"""
    results = []
    
    # 测试url_for
    with app.test_request_context():
        try:
            # 这里可以添加对你实现的路由的测试
            pass
        except Exception as e:
            results.append(f"错误：{str(e)}")
    
    if not results:
        results.append("请完成上面的练习！")
    
    return '<br>'.join(results)


if __name__ == '__main__':
    print("路由练习")
    print("请完成代码中的TODO部分")
    print("完成后访问 /test 查看测试结果")
    app.run(debug=True) 