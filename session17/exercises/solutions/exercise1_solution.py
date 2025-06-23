"""
练习1参考答案：路由练习
"""

from flask import Flask, url_for, request
from werkzeug.routing import BaseConverter
import re

app = Flask(__name__)


# 练习1：创建基本路由
@app.route('/welcome')
def welcome():
    return "欢迎来到Flask世界！"


# 练习2：动态路由
@app.route('/greet/<name>')
def greet(name):
    return f"你好，{name}！欢迎访问。"


# 练习3：多个参数的动态路由
@app.route('/calculate/<int:num1>/<operation>/<int:num2>')
def calculate(num1, operation, num2):
    if operation == 'add':
        result = num1 + num2
        symbol = '+'
    elif operation == 'subtract':
        result = num1 - num2
        symbol = '-'
    elif operation == 'multiply':
        result = num1 * num2
        symbol = '*'
    elif operation == 'divide':
        if num2 == 0:
            return "错误：除数不能为0"
        result = num1 / num2
        symbol = '/'
    else:
        return f"不支持的操作：{operation}"
    
    return f"{num1} {symbol} {num2} = {result}"


# 练习4：带默认值的路由
@app.route('/product')
@app.route('/product/<int:product_id>')
def product(product_id=None):
    if product_id is None:
        # 显示所有产品列表
        products = [
            {'id': 1, 'name': '笔记本电脑'},
            {'id': 2, 'name': '智能手机'},
            {'id': 3, 'name': '平板电脑'}
        ]
        html = '<h1>产品列表</h1><ul>'
        for p in products:
            html += f'<li><a href="/product/{p["id"]}">{p["name"]}</a></li>'
        html += '</ul>'
        return html
    else:
        # 显示特定产品详情
        return f'<h1>产品详情</h1><p>产品ID: {product_id}</p><p><a href="/product">返回列表</a></p>'


# 练习5：路径参数
@app.route('/files/<path:filepath>')
def files(filepath):
    # 分析文件路径
    parts = filepath.split('/')
    directory = '/'.join(parts[:-1]) if len(parts) > 1 else '根目录'
    filename = parts[-1]
    
    return f'''
    <h1>文件路径信息</h1>
    <p><strong>完整路径：</strong>{filepath}</p>
    <p><strong>目录：</strong>{directory}</p>
    <p><strong>文件名：</strong>{filename}</p>
    <p><strong>路径深度：</strong>{len(parts)}层</p>
    '''


# 练习6：URL构建
@app.route('/navigation')
def navigation():
    with app.test_request_context():
        links = [
            ('欢迎页面', url_for('welcome')),
            ('问候页面', url_for('greet', name='访客')),
            ('计算器', url_for('calculate', num1=10, operation='add', num2=5)),
            ('产品列表', url_for('product')),
            ('产品详情', url_for('product', product_id=1)),
            ('文件浏览', url_for('files', filepath='docs/python/tutorial.pdf')),
        ]
    
    html = '<h1>网站导航</h1><ul>'
    for title, url in links:
        html += f'<li><a href="{url}">{title}</a> - {url}</li>'
    html += '</ul>'
    
    return html


# 练习7：限制HTTP方法
@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    if request.method == 'GET':
        return "获取数据"
    elif request.method == 'POST':
        return "创建数据"
    # Flask会自动处理不允许的方法，返回405


# 练习8：正则表达式路由（高级）
class PhoneConverter(BaseConverter):
    """自定义路由转换器，用于匹配电话号码"""
    regex = r'\d{3}-\d{4}-\d{4}'

# 注册转换器
app.url_map.converters['phone'] = PhoneConverter

@app.route('/phone/<phone:phone_number>')
def phone(phone_number):
    # 解析电话号码
    parts = phone_number.split('-')
    return f'''
    <h1>电话号码信息</h1>
    <p>完整号码：{phone_number}</p>
    <p>区号：{parts[0]}</p>
    <p>前缀：{parts[1]}</p>
    <p>后缀：{parts[2]}</p>
    '''


# 测试路由
@app.route('/test')
def test():
    """测试路由是否正确实现"""
    results = ['<h1>路由测试结果</h1>']
    
    # 测试url_for
    with app.test_request_context():
        try:
            # 测试基本路由
            results.append(f"✓ /welcome 路由: {url_for('welcome')}")
            
            # 测试动态路由
            results.append(f"✓ /greet 路由: {url_for('greet', name='测试用户')}")
            
            # 测试计算路由
            results.append(f"✓ /calculate 路由: {url_for('calculate', num1=10, operation='add', num2=5)}")
            
            # 测试产品路由
            results.append(f"✓ /product 路由: {url_for('product')}")
            results.append(f"✓ /product/1 路由: {url_for('product', product_id=1)}")
            
            # 测试文件路由
            results.append(f"✓ /files 路由: {url_for('files', filepath='test/file.txt')}")
            
            # 测试导航路由
            results.append(f"✓ /navigation 路由: {url_for('navigation')}")
            
            # 测试API路由
            results.append(f"✓ /api/data 路由: {url_for('api_data')}")
            
            # 测试电话路由
            results.append(f"✓ /phone 路由: {url_for('phone', phone_number='138-1234-5678')}")
            
            results.append('<hr><p style="color: green;">所有路由测试通过！</p>')
            
        except Exception as e:
            results.append(f'<p style="color: red;">错误：{str(e)}</p>')
    
    # 添加测试链接
    results.append('<h2>快速测试链接</h2><ul>')
    test_links = [
        ('/welcome', '基本路由'),
        ('/greet/张三', '动态路由'),
        ('/calculate/20/multiply/5', '计算器'),
        ('/product', '产品列表'),
        ('/files/documents/report.pdf', '文件路径'),
        ('/phone/138-1234-5678', '电话号码'),
    ]
    
    for url, desc in test_links:
        results.append(f'<li><a href="{url}">{desc}</a></li>')
    
    results.append('</ul>')
    
    return '\n'.join(results)


# 添加首页
@app.route('/')
def index():
    return '''
    <h1>路由练习参考答案</h1>
    <p>这是练习1的参考答案，展示了Flask路由的各种用法。</p>
    <ul>
        <li><a href="/test">查看测试结果</a></li>
        <li><a href="/navigation">查看导航页面</a></li>
    </ul>
    '''


if __name__ == '__main__':
    print("路由练习参考答案")
    print("访问 http://127.0.0.1:5000/test 查看测试结果")
    app.run(debug=True) 