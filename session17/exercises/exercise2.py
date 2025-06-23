"""
练习2：模板练习
完成以下Jinja2模板相关的练习
"""

from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

# 示例数据
students = [
    {'id': 1, 'name': '张三', 'age': 20, 'grade': 85, 'passed': True},
    {'id': 2, 'name': '李四', 'age': 21, 'grade': 92, 'passed': True},
    {'id': 3, 'name': '王五', 'age': 19, 'grade': 58, 'passed': False},
    {'id': 4, 'name': '赵六', 'age': 22, 'grade': 76, 'passed': True},
    {'id': 5, 'name': '钱七', 'age': 20, 'grade': 45, 'passed': False},
]

products = [
    {'name': '笔记本电脑', 'price': 4999, 'discount': 0.1, 'in_stock': True},
    {'name': '智能手机', 'price': 2999, 'discount': 0.15, 'in_stock': True},
    {'name': '平板电脑', 'price': 1999, 'discount': 0, 'in_stock': False},
    {'name': '智能手表', 'price': 1299, 'discount': 0.2, 'in_stock': True},
]


# 练习1：变量和表达式
@app.route('/exercise1')
def exercise1():
    """
    TODO: 完成模板，显示：
    1. 当前日期和时间
    2. 学生总数
    3. 及格学生数量
    4. 及格率（百分比）
    """
    template = '''
    <h1>练习1：变量和表达式</h1>
    <!-- TODO: 在这里完成模板 -->
    <p>当前时间：</p>
    <p>学生总数：</p>
    <p>及格学生数：</p>
    <p>及格率：</p>
    '''
    
    current_time = datetime.now()
    passed_students = [s for s in students if s['passed']]
    
    return render_template_string(template, 
                                students=students,
                                current_time=current_time,
                                passed_students=passed_students)


# 练习2：条件语句
@app.route('/exercise2')
def exercise2():
    """
    TODO: 使用条件语句完成模板
    1. 如果所有学生都及格，显示"全部及格！"
    2. 如果有不及格的，显示不及格学生名单
    3. 根据不及格人数显示不同的提示信息
    """
    template = '''
    <h1>练习2：条件语句</h1>
    <!-- TODO: 在这里完成模板 -->
    
    '''
    
    return render_template_string(template, students=students)


# 练习3：循环和过滤器
@app.route('/exercise3')
def exercise3():
    """
    TODO: 使用循环显示学生表格
    1. 显示学生信息表格（ID、姓名、年龄、成绩）
    2. 及格的学生用绿色背景，不及格用红色背景
    3. 使用循环变量显示序号
    4. 成绩保留1位小数
    """
    template = '''
    <h1>练习3：循环和过滤器</h1>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        .passed { background-color: #d4edda; }
        .failed { background-color: #f8d7da; }
    </style>
    <!-- TODO: 在这里完成模板 -->
    
    '''
    
    return render_template_string(template, students=students)


# 练习4：宏的使用
@app.route('/exercise4')
def exercise4():
    """
    TODO: 创建一个宏来显示产品卡片
    1. 显示产品名称、原价、折后价
    2. 如果有折扣，显示折扣百分比
    3. 如果缺货，显示"已售罄"按钮
    4. 如果有货，显示"加入购物车"按钮
    """
    template = '''
    <h1>练习4：宏的使用</h1>
    
    <!-- TODO: 在这里定义产品卡片宏 -->
    
    
    <div style="display: flex; flex-wrap: wrap;">
        <!-- TODO: 使用宏显示所有产品 -->
        
    </div>
    '''
    
    return render_template_string(template, products=products)


# 练习5：自定义过滤器
# TODO: 创建以下自定义过滤器
# 1. grade_level：根据成绩返回等级（优秀90+、良好80-89、及格60-79、不及格<60）
# 2. discount_price：计算折后价格
# 3. format_currency：格式化货币（添加¥符号和千位分隔符）

# 你的代码：



@app.route('/exercise5')
def exercise5():
    """使用自定义过滤器"""
    template = '''
    <h1>练习5：自定义过滤器</h1>
    
    <h2>学生成绩等级</h2>
    <ul>
    {% for student in students %}
        <!-- TODO: 使用grade_level过滤器显示成绩等级 -->
        <li>{{ student.name }}：{{ student.grade }} 分</li>
    {% endfor %}
    </ul>
    
    <h2>产品价格</h2>
    <ul>
    {% for product in products %}
        <!-- TODO: 使用discount_price和format_currency过滤器显示价格 -->
        <li>{{ product.name }}：原价 {{ product.price }} 元</li>
    {% endfor %}
    </ul>
    '''
    
    return render_template_string(template, students=students, products=products)


# 练习6：模板继承
@app.route('/exercise6')
def exercise6():
    """
    TODO: 创建一个包含模板继承的页面
    1. 创建base_template基础模板，包含：标题、导航、内容区、页脚
    2. 创建child_template子模板，继承基础模板
    3. 在子模板中覆盖标题和内容区块
    """
    base_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{% block title %}默认标题{% endblock %}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; }
            nav { background: #333; color: white; padding: 10px; }
            main { padding: 20px; }
            footer { background: #f0f0f0; padding: 10px; text-align: center; }
        </style>
    </head>
    <body>
        <nav>
            <!-- TODO: 添加导航内容 -->
        </nav>
        
        <main>
            {% block content %}
            <!-- TODO: 默认内容 -->
            {% endblock %}
        </main>
        
        <footer>
            <!-- TODO: 添加页脚内容 -->
        </footer>
    </body>
    </html>
    '''
    
    child_template = '''
    <!-- TODO: 继承base_template并覆盖相应的块 -->
    
    '''
    
    # 这里需要特殊处理，因为render_template_string不支持模板继承
    # 实际项目中应该使用文件模板
    return child_template


# 练习7：综合练习
@app.route('/exercise7')
def exercise7():
    """
    TODO: 创建一个学生成绩报告页面，包含：
    1. 页面标题和说明
    2. 成绩统计信息（平均分、最高分、最低分）
    3. 学生成绩表格（使用适当的样式）
    4. 成绩分布图表（使用文字表示）
    5. 优秀学生名单（90分以上）
    """
    template = '''
    <h1>练习7：综合练习 - 学生成绩报告</h1>
    <!-- TODO: 在这里完成完整的成绩报告页面 -->
    
    '''
    
    # 计算统计数据
    grades = [s['grade'] for s in students]
    stats = {
        'average': sum(grades) / len(grades),
        'max': max(grades),
        'min': min(grades),
        'excellent': [s for s in students if s['grade'] >= 90]
    }
    
    return render_template_string(template, students=students, stats=stats)


# 主页
@app.route('/')
def index():
    """练习列表"""
    exercises = [
        {'url': '/exercise1', 'title': '练习1：变量和表达式'},
        {'url': '/exercise2', 'title': '练习2：条件语句'},
        {'url': '/exercise3', 'title': '练习3：循环和过滤器'},
        {'url': '/exercise4', 'title': '练习4：宏的使用'},
        {'url': '/exercise5', 'title': '练习5：自定义过滤器'},
        {'url': '/exercise6', 'title': '练习6：模板继承'},
        {'url': '/exercise7', 'title': '练习7：综合练习'},
    ]
    
    template = '''
    <h1>Jinja2模板练习</h1>
    <p>请完成以下练习：</p>
    <ol>
    {% for exercise in exercises %}
        <li><a href="{{ exercise.url }}">{{ exercise.title }}</a></li>
    {% endfor %}
    </ol>
    '''
    
    return render_template_string(template, exercises=exercises)


if __name__ == '__main__':
    print("模板练习")
    print("请完成每个练习中的TODO部分")
    print("访问 http://127.0.0.1:5000 查看练习列表")
    app.run(debug=True) 