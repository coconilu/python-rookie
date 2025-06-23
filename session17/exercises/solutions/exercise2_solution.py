"""
练习2参考答案：模板练习
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
    """完成模板，显示统计信息"""
    template = '''
    <h1>练习1：变量和表达式</h1>
    <p>当前时间：{{ current_time.strftime('%Y-%m-%d %H:%M:%S') }}</p>
    <p>学生总数：{{ students|length }}</p>
    <p>及格学生数：{{ passed_students|length }}</p>
    <p>及格率：{{ "%.1f"|format((passed_students|length / students|length * 100)) }}%</p>
    
    <h2>额外演示</h2>
    <p>数学运算：10 + 20 = {{ 10 + 20 }}</p>
    <p>字符串拼接：{{ "Hello " + "Flask" }}</p>
    <p>列表索引：第一个学生是 {{ students[0].name }}</p>
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
    """使用条件语句完成模板"""
    template = '''
    <h1>练习2：条件语句</h1>
    
    {% set failed_students = students|selectattr('passed', 'equalto', False)|list %}
    
    {% if failed_students|length == 0 %}
        <p style="color: green; font-size: 20px;">🎉 全部及格！</p>
    {% else %}
        <h2>不及格学生名单</h2>
        <ul style="color: red;">
        {% for student in failed_students %}
            <li>{{ student.name }} - {{ student.grade }}分</li>
        {% endfor %}
        </ul>
        
        {% if failed_students|length == 1 %}
            <p>有 1 名学生需要补考。</p>
        {% elif failed_students|length < 3 %}
            <p>有 {{ failed_students|length }} 名学生需要补考，情况还好。</p>
        {% else %}
            <p style="color: red;">有 {{ failed_students|length }} 名学生不及格，需要加强辅导！</p>
        {% endif %}
    {% endif %}
    '''
    
    return render_template_string(template, students=students)


# 练习3：循环和过滤器
@app.route('/exercise3')
def exercise3():
    """使用循环显示学生表格"""
    template = '''
    <h1>练习3：循环和过滤器</h1>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        .passed { background-color: #d4edda; }
        .failed { background-color: #f8d7da; }
        tr:hover { background-color: #f5f5f5; }
    </style>
    
    <table>
        <thead>
            <tr>
                <th>序号</th>
                <th>ID</th>
                <th>姓名</th>
                <th>年龄</th>
                <th>成绩</th>
                <th>状态</th>
            </tr>
        </thead>
        <tbody>
        {% for student in students %}
            <tr class="{{ 'passed' if student.passed else 'failed' }}">
                <td>{{ loop.index }}</td>
                <td>{{ student.id }}</td>
                <td>{{ student.name }}</td>
                <td>{{ student.age }}</td>
                <td>{{ "%.1f"|format(student.grade) }}</td>
                <td>{{ '及格' if student.passed else '不及格' }}</td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
    
    <h3>循环变量演示</h3>
    <p>学生总数：{{ loop.length if students else 0 }}</p>
    '''
    
    return render_template_string(template, students=students)


# 练习4：宏的使用
@app.route('/exercise4')
def exercise4():
    """创建产品卡片宏"""
    template = '''
    <h1>练习4：宏的使用</h1>
    
    {% macro product_card(product) %}
        <div style="border: 1px solid #ddd; padding: 15px; margin: 10px; width: 200px; float: left; border-radius: 5px;">
            <h3>{{ product.name }}</h3>
            <p>原价：<span style="text-decoration: line-through;">¥{{ product.price }}</span></p>
            
            {% if product.discount > 0 %}
                <p>折扣：{{ (product.discount * 100)|int }}% OFF</p>
                <p style="color: red; font-size: 18px;">
                    现价：¥{{ "%.2f"|format(product.price * (1 - product.discount)) }}
                </p>
            {% else %}
                <p style="font-size: 18px;">价格：¥{{ product.price }}</p>
            {% endif %}
            
            {% if product.in_stock %}
                <button style="background: #28a745; color: white; padding: 5px 10px; border: none; border-radius: 3px;">
                    加入购物车
                </button>
            {% else %}
                <button style="background: #dc3545; color: white; padding: 5px 10px; border: none; border-radius: 3px;" disabled>
                    已售罄
                </button>
            {% endif %}
        </div>
    {% endmacro %}
    
    <div style="overflow: auto;">
        {% for product in products %}
            {{ product_card(product) }}
        {% endfor %}
    </div>
    <div style="clear: both;"></div>
    '''
    
    return render_template_string(template, products=products)


# 练习5：自定义过滤器
@app.template_filter('grade_level')
def grade_level_filter(grade):
    """根据成绩返回等级"""
    if grade >= 90:
        return '优秀'
    elif grade >= 80:
        return '良好'
    elif grade >= 60:
        return '及格'
    else:
        return '不及格'


@app.template_filter('discount_price')
def discount_price_filter(product):
    """计算折后价格"""
    return product['price'] * (1 - product.get('discount', 0))


@app.template_filter('format_currency')
def format_currency_filter(amount):
    """格式化货币"""
    return f"¥{amount:,.2f}"


@app.route('/exercise5')
def exercise5():
    """使用自定义过滤器"""
    template = '''
    <h1>练习5：自定义过滤器</h1>
    
    <h2>学生成绩等级</h2>
    <table border="1" style="border-collapse: collapse;">
        <tr>
            <th>姓名</th>
            <th>成绩</th>
            <th>等级</th>
        </tr>
    {% for student in students %}
        <tr>
            <td>{{ student.name }}</td>
            <td>{{ student.grade }} 分</td>
            <td style="color: {% if student.grade >= 90 %}green{% elif student.grade >= 60 %}blue{% else %}red{% endif %};">
                {{ student.grade|grade_level }}
            </td>
        </tr>
    {% endfor %}
    </table>
    
    <h2>产品价格</h2>
    <ul>
    {% for product in products %}
        <li>
            {{ product.name }}：
            原价 {{ product.price|format_currency }}
            {% if product.discount > 0 %}
                → 现价 {{ product|discount_price|format_currency }}
                <span style="color: red;">(省 {{ ((product.price * product.discount)|format_currency) }})</span>
            {% endif %}
        </li>
    {% endfor %}
    </ul>
    '''
    
    return render_template_string(template, students=students, products=products)


# 练习6：模板继承（模拟）
@app.route('/exercise6')
def exercise6():
    """模拟模板继承"""
    # 注意：render_template_string不支持真正的模板继承
    # 这里只是展示概念
    base_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{% block title %}默认标题{% endblock %}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; }
            nav { background: #333; color: white; padding: 10px; }
            nav a { color: white; text-decoration: none; margin: 0 10px; }
            main { padding: 20px; min-height: 400px; }
            footer { background: #f0f0f0; padding: 10px; text-align: center; }
        </style>
    </head>
    <body>
        <nav>
            <a href="/">首页</a>
            <a href="/about">关于</a>
            <a href="/contact">联系我们</a>
        </nav>
        
        <main>
            {% block content %}
            <p>这是默认内容。</p>
            {% endblock %}
        </main>
        
        <footer>
            <p>&copy; 2024 Flask学习网站</p>
        </footer>
    </body>
    </html>
    '''
    
    # 子模板的内容
    child_content = '''
    <h1>练习6：模板继承演示</h1>
    <p>在实际项目中，我们会使用真正的模板文件来实现继承。</p>
    <p>子模板可以：</p>
    <ul>
        <li>继承基础模板的布局</li>
        <li>覆盖特定的块（block）</li>
        <li>使用super()调用父模板的内容</li>
    </ul>
    
    <h2>示例代码</h2>
    <pre style="background: #f0f0f0; padding: 10px;">
{%- raw %}
<!-- base.html -->
{% block content %}
    默认内容
{% endblock %}

<!-- child.html -->
{% extends "base.html" %}
{% block content %}
    {{ super() }}
    子模板的额外内容
{% endblock %}
{% endraw -%}
    </pre>
    '''
    
    # 模拟继承效果
    final_html = base_template.replace(
        '{% block content %}\n            <p>这是默认内容。</p>\n            {% endblock %}',
        child_content
    ).replace(
        '{% block title %}默认标题{% endblock %}',
        '模板继承演示'
    )
    
    return final_html


# 练习7：综合练习
@app.route('/exercise7')
def exercise7():
    """学生成绩报告页面"""
    template = '''
    <h1>练习7：综合练习 - 学生成绩报告</h1>
    
    <style>
        .report-container { max-width: 800px; margin: 0 auto; }
        .stats-box { background: #f0f0f0; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .stat-item { background: white; padding: 15px; text-align: center; border-radius: 5px; }
        .stat-value { font-size: 24px; font-weight: bold; color: #007bff; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #007bff; color: white; }
        .grade-bar { background: #e0e0e0; height: 20px; border-radius: 3px; overflow: hidden; }
        .grade-fill { height: 100%; background: #28a745; }
        .excellent { background: #ffd700; padding: 10px; margin: 10px 0; border-radius: 5px; }
    </style>
    
    <div class="report-container">
        <p><strong>报告生成时间：</strong>{{ datetime.now().strftime('%Y年%m月%d日 %H:%M:%S') }}</p>
        
        <div class="stats-box">
            <h2>📊 成绩统计</h2>
            <div class="stats-grid">
                <div class="stat-item">
                    <div>平均分</div>
                    <div class="stat-value">{{ "%.1f"|format(stats.average) }}</div>
                </div>
                <div class="stat-item">
                    <div>最高分</div>
                    <div class="stat-value">{{ stats.max }}</div>
                </div>
                <div class="stat-item">
                    <div>最低分</div>
                    <div class="stat-value">{{ stats.min }}</div>
                </div>
            </div>
        </div>
        
        <h2>📋 学生成绩表</h2>
        <table>
            <thead>
                <tr>
                    <th>排名</th>
                    <th>姓名</th>
                    <th>成绩</th>
                    <th>等级</th>
                    <th>可视化</th>
                </tr>
            </thead>
            <tbody>
            {% for student in students|sort(attribute='grade', reverse=True) %}
                <tr style="background-color: {% if student.grade >= 90 %}#fffacd{% elif student.grade < 60 %}#ffebee{% else %}white{% endif %};">
                    <td>{{ loop.index }}</td>
                    <td>{{ student.name }}</td>
                    <td>{{ student.grade }}</td>
                    <td>{{ student.grade|grade_level }}</td>
                    <td>
                        <div class="grade-bar">
                            <div class="grade-fill" style="width: {{ student.grade }}%; 
                                background: {% if student.grade >= 90 %}#ffd700{% elif student.grade >= 60 %}#28a745{% else %}#dc3545{% endif %};">
                            </div>
                        </div>
                    </td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
        
        <h2>📈 成绩分布</h2>
        {% set grade_ranges = {
            '90-100分 (优秀)': students|selectattr('grade', '>=', 90)|list|length,
            '80-89分 (良好)': students|select('lambda x: 80 <= x.grade < 90')|list|length,
            '60-79分 (及格)': students|select('lambda x: 60 <= x.grade < 80')|list|length,
            '60分以下 (不及格)': students|selectattr('grade', '<', 60)|list|length
        } %}
        
        <!-- 使用更简单的方法计算分布 -->
        {% set excellent_count = 0 %}
        {% set good_count = 0 %}
        {% set pass_count = 0 %}
        {% set fail_count = 0 %}
        
        {% for student in students %}
            {% if student.grade >= 90 %}
                {% set excellent_count = excellent_count + 1 %}
            {% elif student.grade >= 80 %}
                {% set good_count = good_count + 1 %}
            {% elif student.grade >= 60 %}
                {% set pass_count = pass_count + 1 %}
            {% else %}
                {% set fail_count = fail_count + 1 %}
            {% endif %}
        {% endfor %}
        
        <div style="margin: 20px 0;">
            <div style="margin: 5px 0;">
                <span style="display: inline-block; width: 150px;">优秀 (90-100):</span>
                <span style="display: inline-block; background: #ffd700; height: 20px; width: {{ excellent_count * 50 }}px;"></span>
                <span>{{ excellent_count }}人</span>
            </div>
            <div style="margin: 5px 0;">
                <span style="display: inline-block; width: 150px;">良好 (80-89):</span>
                <span style="display: inline-block; background: #87ceeb; height: 20px; width: {{ good_count * 50 }}px;"></span>
                <span>{{ good_count }}人</span>
            </div>
            <div style="margin: 5px 0;">
                <span style="display: inline-block; width: 150px;">及格 (60-79):</span>
                <span style="display: inline-block; background: #90ee90; height: 20px; width: {{ pass_count * 50 }}px;"></span>
                <span>{{ pass_count }}人</span>
            </div>
            <div style="margin: 5px 0;">
                <span style="display: inline-block; width: 150px;">不及格 (<60):</span>
                <span style="display: inline-block; background: #ffb6c1; height: 20px; width: {{ fail_count * 50 }}px;"></span>
                <span>{{ fail_count }}人</span>
            </div>
        </div>
        
        {% if stats.excellent %}
        <div class="excellent">
            <h2>🏆 优秀学生名单</h2>
            <p>以下学生成绩达到90分以上：</p>
            <ul>
            {% for student in stats.excellent %}
                <li><strong>{{ student.name }}</strong> - {{ student.grade }}分</li>
            {% endfor %}
            </ul>
        </div>
        {% endif %}
    </div>
    '''
    
    # 计算统计数据
    grades = [s['grade'] for s in students]
    stats = {
        'average': sum(grades) / len(grades),
        'max': max(grades),
        'min': min(grades),
        'excellent': [s for s in students if s['grade'] >= 90]
    }
    
    return render_template_string(template, students=students, stats=stats, datetime=datetime)


# 主页
@app.route('/')
def index():
    """练习列表"""
    exercises = [
        {'url': '/exercise1', 'title': '练习1：变量和表达式', 'desc': '学习模板变量和表达式的使用'},
        {'url': '/exercise2', 'title': '练习2：条件语句', 'desc': '掌握if/else条件判断'},
        {'url': '/exercise3', 'title': '练习3：循环和过滤器', 'desc': '使用for循环和内置过滤器'},
        {'url': '/exercise4', 'title': '练习4：宏的使用', 'desc': '创建可重用的模板宏'},
        {'url': '/exercise5', 'title': '练习5：自定义过滤器', 'desc': '编写自定义过滤器函数'},
        {'url': '/exercise6', 'title': '练习6：模板继承', 'desc': '理解模板继承机制'},
        {'url': '/exercise7', 'title': '练习7：综合练习', 'desc': '综合运用所有模板技术'},
    ]
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Jinja2模板练习参考答案</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .exercise-list { list-style: none; padding: 0; }
            .exercise-item { 
                background: #f0f0f0; 
                padding: 15px; 
                margin: 10px 0; 
                border-radius: 5px;
                transition: background 0.3s;
            }
            .exercise-item:hover { background: #e0e0e0; }
            .exercise-item a { 
                text-decoration: none; 
                color: #007bff; 
                font-size: 18px; 
                font-weight: bold; 
            }
            .exercise-desc { color: #666; margin-top: 5px; }
        </style>
    </head>
    <body>
        <h1>Jinja2模板练习参考答案</h1>
        <p>以下是所有练习的参考答案，点击查看每个练习的实现：</p>
        
        <ul class="exercise-list">
        {% for exercise in exercises %}
            <li class="exercise-item">
                <a href="{{ exercise.url }}">{{ exercise.title }}</a>
                <div class="exercise-desc">{{ exercise.desc }}</div>
            </li>
        {% endfor %}
        </ul>
        
        <hr>
        <p><strong>学习提示：</strong></p>
        <ul>
            <li>仔细观察每个练习的实现方式</li>
            <li>理解Jinja2的语法和特性</li>
            <li>尝试修改代码，看看效果</li>
            <li>思考还有哪些实现方式</li>
        </ul>
    </body>
    </html>
    '''
    
    return render_template_string(template, exercises=exercises)


if __name__ == '__main__':
    print("模板练习参考答案")
    print("访问 http://127.0.0.1:5000 查看所有练习答案")
    app.run(debug=True) 