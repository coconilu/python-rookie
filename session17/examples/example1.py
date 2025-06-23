"""
示例1：基础路由
演示Flask路由的基本用法
"""

from flask import Flask

# 创建Flask应用
app = Flask(__name__)


# 1. 基本路由
@app.route('/')
def index():
    """主页路由"""
    return '<h1>欢迎来到首页</h1><p>这是最基本的路由示例。</p>'


@app.route('/hello')
def hello():
    """简单的问候路由"""
    return '<h1>Hello, Flask!</h1>'


# 2. 多个URL指向同一个视图
@app.route('/about')
@app.route('/about-us')
@app.route('/info')
def about():
    """多个URL映射到同一个函数"""
    return '''
    <h1>关于我们</h1>
    <p>这个页面可以通过以下URL访问：</p>
    <ul>
        <li>/about</li>
        <li>/about-us</li>
        <li>/info</li>
    </ul>
    '''


# 3. 动态路由 - 字符串参数
@app.route('/user/<name>')
def user(name):
    """接收字符串参数的动态路由"""
    return f'<h1>欢迎，{name}！</h1><p>你的用户名是：{name}</p>'


# 4. 动态路由 - 整数参数
@app.route('/post/<int:post_id>')
def show_post(post_id):
    """接收整数参数的动态路由"""
    return f'''
    <h1>文章 #{post_id}</h1>
    <p>你正在查看ID为 {post_id} 的文章。</p>
    <p>参数类型：{type(post_id).__name__}</p>
    '''


# 5. 动态路由 - 浮点数参数
@app.route('/price/<float:amount>')
def show_price(amount):
    """接收浮点数参数的动态路由"""
    return f'''
    <h1>价格信息</h1>
    <p>价格：¥{amount:.2f}</p>
    <p>含税价格：¥{amount * 1.13:.2f}</p>
    '''


# 6. 动态路由 - 路径参数
@app.route('/path/<path:subpath>')
def show_path(subpath):
    """接收路径参数的动态路由"""
    segments = subpath.split('/')
    return f'''
    <h1>路径信息</h1>
    <p>完整路径：{subpath}</p>
    <p>路径段数：{len(segments)}</p>
    <p>路径段：{segments}</p>
    '''


# 7. UUID参数（需要导入uuid）
from uuid import UUID

@app.route('/item/<uuid:item_id>')
def show_item(item_id):
    """接收UUID参数的动态路由"""
    return f'''
    <h1>物品信息</h1>
    <p>物品ID：{item_id}</p>
    <p>类型：{type(item_id).__name__}</p>
    '''


# 8. 带默认值的路由
@app.route('/greet')
@app.route('/greet/<name>')
def greet(name='访客'):
    """带默认值的路由"""
    return f'<h1>你好，{name}！</h1>'


# 9. 尾部斜杠的处理
@app.route('/projects/')
def projects():
    """带尾部斜杠的路由（类似目录）"""
    return '''
    <h1>项目列表</h1>
    <p>访问 /projects 会自动重定向到 /projects/</p>
    '''


@app.route('/contact')
def contact():
    """不带尾部斜杠的路由（类似文件）"""
    return '''
    <h1>联系我们</h1>
    <p>访问 /contact/ 会返回404错误</p>
    '''


# 10. 构建URL
from flask import url_for

@app.route('/test-url-for')
def test_url_for():
    """演示url_for函数的使用"""
    # 需要在应用上下文中使用url_for
    with app.test_request_context():
        urls = {
            '首页': url_for('index'),
            '关于': url_for('about'),
            '用户页面': url_for('user', name='alice'),
            '文章页面': url_for('show_post', post_id=123),
            '价格页面': url_for('show_price', amount=99.99),
        }
    
    html = '<h1>URL构建示例</h1><ul>'
    for name, url in urls.items():
        html += f'<li>{name}: <a href="{url}">{url}</a></li>'
    html += '</ul>'
    
    return html


# 11. 路由列表
@app.route('/sitemap')
def sitemap():
    """显示所有可用的路由"""
    routes = []
    for rule in app.url_map.iter_rules():
        # 跳过静态文件路由
        if rule.endpoint != 'static':
            routes.append({
                'endpoint': rule.endpoint,
                'methods': ','.join(rule.methods),
                'url': rule.rule
            })
    
    html = '<h1>站点地图</h1><table border="1"><tr><th>URL</th><th>方法</th><th>端点</th></tr>'
    for route in sorted(routes, key=lambda x: x['url']):
        html += f"<tr><td>{route['url']}</td><td>{route['methods']}</td><td>{route['endpoint']}</td></tr>"
    html += '</table>'
    
    return html


if __name__ == '__main__':
    print("基础路由示例")
    print("访问 http://127.0.0.1:5000/sitemap 查看所有路由")
    app.run(debug=True) 