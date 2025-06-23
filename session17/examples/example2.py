"""
示例2：模板使用
演示Jinja2模板引擎的各种功能
"""

from flask import Flask, render_template_string, render_template
import os
from datetime import datetime

app = Flask(__name__)


# 1. 内联模板示例
@app.route('/')
def index():
    """使用render_template_string渲染内联模板"""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ title }}</title>
    </head>
    <body>
        <h1>{{ heading }}</h1>
        <p>当前时间：{{ current_time }}</p>
    </body>
    </html>
    '''
    
    return render_template_string(
        template,
        title='模板示例',
        heading='欢迎使用Jinja2模板',
        current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )


# 2. 变量和表达式
@app.route('/variables')
def variables():
    """演示模板变量和表达式"""
    template = '''
    <h1>变量和表达式示例</h1>
    
    <h2>基本变量</h2>
    <p>字符串：{{ name }}</p>
    <p>数字：{{ age }}</p>
    <p>列表第一项：{{ items[0] }}</p>
    <p>字典值：{{ user.username }}</p>
    
    <h2>表达式</h2>
    <p>数学运算：{{ 10 + 20 }}</p>
    <p>字符串连接：{{ "Hello " + name }}</p>
    <p>比较：{{ age > 18 }}</p>
    
    <h2>方法调用</h2>
    <p>大写：{{ name.upper() }}</p>
    <p>列表长度：{{ items|length }}</p>
    '''
    
    return render_template_string(
        template,
        name='张三',
        age=25,
        items=['Python', 'Flask', 'Jinja2'],
        user={'username': 'zhangsan', 'email': 'zhangsan@example.com'}
    )


# 3. 控制结构
@app.route('/control-structures')
def control_structures():
    """演示模板中的控制结构"""
    template = '''
    <h1>控制结构示例</h1>
    
    <h2>条件语句</h2>
    {% if user %}
        <p>欢迎，{{ user.name }}！</p>
        {% if user.is_admin %}
            <p>您是管理员。</p>
        {% else %}
            <p>您是普通用户。</p>
        {% endif %}
    {% else %}
        <p>请先登录。</p>
    {% endif %}
    
    <h2>循环语句</h2>
    <h3>产品列表：</h3>
    <ul>
    {% for product in products %}
        <li>
            {{ loop.index }}. {{ product.name }} - ¥{{ product.price }}
            {% if product.in_stock %}
                <span style="color: green;">有货</span>
            {% else %}
                <span style="color: red;">缺货</span>
            {% endif %}
        </li>
    {% endfor %}
    </ul>
    
    <h3>循环变量：</h3>
    <table border="1">
    {% for item in ['A', 'B', 'C', 'D'] %}
        <tr>
            <td>loop.index: {{ loop.index }}</td>
            <td>loop.index0: {{ loop.index0 }}</td>
            <td>loop.first: {{ loop.first }}</td>
            <td>loop.last: {{ loop.last }}</td>
            <td>loop.length: {{ loop.length }}</td>
        </tr>
    {% endfor %}
    </table>
    '''
    
    return render_template_string(
        template,
        user={'name': '李四', 'is_admin': False},
        products=[
            {'name': 'iPhone', 'price': 6999, 'in_stock': True},
            {'name': 'iPad', 'price': 3999, 'in_stock': True},
            {'name': 'MacBook', 'price': 9999, 'in_stock': False},
        ]
    )


# 4. 过滤器
@app.route('/filters')
def filters():
    """演示Jinja2过滤器"""
    template = '''
    <h1>过滤器示例</h1>
    
    <h2>字符串过滤器</h2>
    <p>原始：{{ text }}</p>
    <p>大写：{{ text|upper }}</p>
    <p>小写：{{ text|lower }}</p>
    <p>标题化：{{ text|title }}</p>
    <p>首字母大写：{{ text|capitalize }}</p>
    <p>去除空格：{{ "  hello world  "|trim }}</p>
    <p>替换：{{ text|replace("World", "Flask") }}</p>
    <p>截断：{{ long_text|truncate(20) }}</p>
    
    <h2>列表过滤器</h2>
    <p>原始列表：{{ numbers }}</p>
    <p>长度：{{ numbers|length }}</p>
    <p>第一个：{{ numbers|first }}</p>
    <p>最后一个：{{ numbers|last }}</p>
    <p>随机：{{ numbers|random }}</p>
    <p>求和：{{ numbers|sum }}</p>
    <p>排序：{{ numbers|sort }}</p>
    <p>反转：{{ numbers|reverse|list }}</p>
    <p>连接：{{ words|join(", ") }}</p>
    
    <h2>格式化过滤器</h2>
    <p>默认值：{{ undefined_var|default("默认值") }}</p>
    <p>浮点数格式化：{{ pi|round(2) }}</p>
    <p>整数格式化：{{ large_number|int }}</p>
    
    <h2>安全过滤器</h2>
    <p>转义HTML：{{ html_content }}</p>
    <p>不转义HTML：{{ html_content|safe }}</p>
    
    <h2>链式过滤器</h2>
    <p>{{ text|lower|replace(" ", "-") }}</p>
    '''
    
    return render_template_string(
        template,
        text="Hello World",
        long_text="这是一段很长很长的文本，需要被截断显示",
        numbers=[3, 1, 4, 1, 5, 9, 2, 6],
        words=['Python', 'Flask', 'Jinja2'],
        pi=3.14159265359,
        large_number=1234.5678,
        html_content='<strong>粗体文本</strong> <em>斜体文本</em>'
    )


# 5. 宏（Macro）
@app.route('/macros')
def macros():
    """演示Jinja2宏的使用"""
    template = '''
    {# 定义宏 #}
    {% macro render_product(product) %}
        <div class="product" style="border: 1px solid #ccc; padding: 10px; margin: 10px;">
            <h3>{{ product.name }}</h3>
            <p>价格：¥{{ product.price }}</p>
            <p>库存：{{ product.stock }}件</p>
            {% if product.stock > 0 %}
                <button>加入购物车</button>
            {% else %}
                <button disabled>已售罄</button>
            {% endif %}
        </div>
    {% endmacro %}
    
    {% macro render_user_card(user, show_email=True) %}
        <div class="user-card" style="background: #f0f0f0; padding: 10px; margin: 5px;">
            <strong>{{ user.name }}</strong>
            {% if show_email %}
                <br>邮箱：{{ user.email }}
            {% endif %}
        </div>
    {% endmacro %}
    
    <h1>宏（Macro）示例</h1>
    
    <h2>产品列表</h2>
    {% for product in products %}
        {{ render_product(product) }}
    {% endfor %}
    
    <h2>用户列表</h2>
    {% for user in users %}
        {{ render_user_card(user, show_email=loop.first) }}
    {% endfor %}
    '''
    
    return render_template_string(
        template,
        products=[
            {'name': '笔记本电脑', 'price': 4999, 'stock': 10},
            {'name': '无线鼠标', 'price': 99, 'stock': 0},
            {'name': '机械键盘', 'price': 399, 'stock': 5},
        ],
        users=[
            {'name': '张三', 'email': 'zhangsan@example.com'},
            {'name': '李四', 'email': 'lisi@example.com'},
            {'name': '王五', 'email': 'wangwu@example.com'},
        ]
    )


# 6. 模板继承
@app.route('/inheritance')
def inheritance():
    """演示模板继承"""
    # 创建模板目录
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(template_dir, exist_ok=True)
    
    # 基础模板
    base_template = '''<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}默认标题{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        header { background: #333; color: white; padding: 10px; }
        nav { background: #666; color: white; padding: 5px; }
        nav a { color: white; margin: 0 10px; }
        main { min-height: 300px; padding: 20px; }
        footer { background: #333; color: white; padding: 10px; text-align: center; }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        <h1>{% block header %}我的网站{% endblock %}</h1>
    </header>
    
    <nav>
        <a href="/">首页</a>
        <a href="/about">关于</a>
        <a href="/contact">联系</a>
    </nav>
    
    <main>
        {% block content %}
        <p>默认内容</p>
        {% endblock %}
    </main>
    
    <footer>
        {% block footer %}
        <p>&copy; 2024 我的网站</p>
        {% endblock %}
    </footer>
    
    {% block extra_js %}{% endblock %}
</body>
</html>'''
    
    # 子模板
    child_template = '''{% extends "base.html" %}

{% block title %}继承示例 - {{ super() }}{% endblock %}

{% block header %}{{ super() }} - 继承示例{% endblock %}

{% block content %}
    <h2>模板继承示例</h2>
    <p>这个页面继承自base.html模板。</p>
    <p>我们可以：</p>
    <ul>
        <li>覆盖父模板的块（block）</li>
        <li>使用super()调用父模板的内容</li>
        <li>添加新的内容</li>
    </ul>
    
    <h3>继承的优势</h3>
    <ol>
        <li>避免重复代码</li>
        <li>保持一致的布局</li>
        <li>易于维护和修改</li>
    </ol>
{% endblock %}

{% block extra_css %}
<style>
    h2 { color: #0066cc; }
    li { margin: 5px 0; }
</style>
{% endblock %}'''
    
    # 保存模板文件
    with open(os.path.join(template_dir, 'base.html'), 'w', encoding='utf-8') as f:
        f.write(base_template)
    
    with open(os.path.join(template_dir, 'inheritance_example.html'), 'w', encoding='utf-8') as f:
        f.write(child_template)
    
    return render_template('inheritance_example.html')


# 7. 包含（Include）
@app.route('/includes')
def includes():
    """演示模板包含"""
    template = '''
    <h1>模板包含示例</h1>
    
    {# 模拟包含头部 #}
    <div style="background: #f0f0f0; padding: 10px; margin: 10px 0;">
        <strong>头部内容（通常通过 {% raw %}{% include 'header.html' %}{% endraw %} 包含）</strong>
    </div>
    
    <main>
        <h2>主要内容</h2>
        <p>模板包含允许我们将常用的模板片段分离到单独的文件中。</p>
        
        {# 模拟包含侧边栏 #}
        <div style="float: right; width: 200px; background: #e0e0e0; padding: 10px;">
            <strong>侧边栏（通常通过 {% raw %}{% include 'sidebar.html' %}{% endraw %} 包含）</strong>
            <ul>
                <li>链接1</li>
                <li>链接2</li>
                <li>链接3</li>
            </ul>
        </div>
        
        <p>常见的包含场景：</p>
        <ul>
            <li>页头（header）</li>
            <li>页脚（footer）</li>
            <li>导航菜单</li>
            <li>侧边栏</li>
            <li>评论表单</li>
        </ul>
    </main>
    
    <div style="clear: both;"></div>
    
    {# 模拟包含页脚 #}
    <div style="background: #f0f0f0; padding: 10px; margin: 10px 0;">
        <strong>页脚内容（通常通过 {% raw %}{% include 'footer.html' %}{% endraw %} 包含）</strong>
    </div>
    '''
    
    return render_template_string(template)


# 8. 自定义过滤器
@app.template_filter('currency')
def currency_filter(value):
    """自定义货币格式化过滤器"""
    return f"¥{value:,.2f}"


@app.template_filter('timeago')
def timeago_filter(datetime_obj):
    """自定义时间差过滤器"""
    if isinstance(datetime_obj, str):
        datetime_obj = datetime.strptime(datetime_obj, '%Y-%m-%d %H:%M:%S')
    
    diff = datetime.now() - datetime_obj
    
    if diff.days > 0:
        return f"{diff.days}天前"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600}小时前"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60}分钟前"
    else:
        return "刚刚"


@app.route('/custom-filters')
def custom_filters():
    """演示自定义过滤器"""
    template = '''
    <h1>自定义过滤器示例</h1>
    
    <h2>货币格式化</h2>
    <p>原始值：{{ price }}</p>
    <p>格式化：{{ price|currency }}</p>
    <p>大额：{{ large_amount|currency }}</p>
    
    <h2>时间差显示</h2>
    {% for post in posts %}
    <p>{{ post.title }} - 发布于{{ post.created_at|timeago }}</p>
    {% endfor %}
    '''
    
    return render_template_string(
        template,
        price=99.5,
        large_amount=1234567.89,
        posts=[
            {'title': '文章1', 'created_at': datetime.now()},
            {'title': '文章2', 'created_at': datetime(2024, 1, 15, 10, 30, 0)},
            {'title': '文章3', 'created_at': datetime(2024, 1, 10, 8, 0, 0)},
        ]
    )


if __name__ == '__main__':
    print("模板使用示例")
    print("访问不同的路由查看各种模板功能：")
    print("- / : 内联模板")
    print("- /variables : 变量和表达式")
    print("- /control-structures : 控制结构")
    print("- /filters : 过滤器")
    print("- /macros : 宏")
    print("- /inheritance : 模板继承")
    print("- /includes : 模板包含")
    print("- /custom-filters : 自定义过滤器")
    app.run(debug=True) 