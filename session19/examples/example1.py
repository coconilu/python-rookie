#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session19 示例1：HTML基础示例

本示例演示了HTML5语义化标签的使用，包括表单元素、
语义化结构和基本的页面布局。

作者: Python教程团队
创建日期: 2024-12-24
"""

from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'html-example-key'

# HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML5语义化标签示例</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        nav ul {
            list-style: none;
            padding: 0;
            display: flex;
            gap: 20px;
        }
        nav a {
            color: white;
            text-decoration: none;
            padding: 5px 10px;
            border-radius: 4px;
            transition: background-color 0.3s;
        }
        nav a:hover {
            background-color: rgba(255,255,255,0.2);
        }
        section {
            margin: 20px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        input, select, textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        button {
            background: #667eea;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }
        button:hover {
            background: #5a6fd8;
        }
        .info-box {
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 15px;
            margin: 15px 0;
        }
        .success-box {
            background: #e8f5e8;
            border-left: 4px solid #4caf50;
            padding: 15px;
            margin: 15px 0;
        }
        footer {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            margin-top: 20px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- 页面头部 -->
        <header>
            <h1>HTML5语义化标签示例</h1>
            <nav>
                <ul>
                    <li><a href="#forms">表单示例</a></li>
                    <li><a href="#semantic">语义化标签</a></li>
                    <li><a href="#multimedia">多媒体元素</a></li>
                </ul>
            </nav>
        </header>
        
        <!-- 主要内容区域 -->
        <main>
            <!-- 表单示例部分 -->
            <section id="forms">
                <h2>表单元素示例</h2>
                <div class="info-box">
                    <strong>说明：</strong>这个表单展示了HTML5中常用的表单元素和验证属性。
                </div>
                
                <form id="demo-form" method="POST" action="/submit">
                    <div class="form-group">
                        <label for="username">用户名 *</label>
                        <input type="text" 
                               id="username" 
                               name="username" 
                               required 
                               minlength="3" 
                               maxlength="20"
                               placeholder="请输入用户名（3-20字符）">
                    </div>
                    
                    <div class="form-group">
                        <label for="email">邮箱地址 *</label>
                        <input type="email" 
                               id="email" 
                               name="email" 
                               required 
                               placeholder="请输入有效的邮箱地址">
                    </div>
                    
                    <div class="form-group">
                        <label for="age">年龄</label>
                        <input type="number" 
                               id="age" 
                               name="age" 
                               min="1" 
                               max="120" 
                               placeholder="请输入年龄">
                    </div>
                    
                    <div class="form-group">
                        <label for="birthday">生日</label>
                        <input type="date" id="birthday" name="birthday">
                    </div>
                    
                    <div class="form-group">
                        <label for="website">个人网站</label>
                        <input type="url" 
                               id="website" 
                               name="website" 
                               placeholder="https://example.com">
                    </div>
                    
                    <div class="form-group">
                        <label for="phone">手机号码</label>
                        <input type="tel" 
                               id="phone" 
                               name="phone" 
                               pattern="[0-9]{11}" 
                               placeholder="请输入11位手机号码">
                    </div>
                    
                    <div class="form-group">
                        <label for="gender">性别</label>
                        <select id="gender" name="gender">
                            <option value="">请选择</option>
                            <option value="male">男</option>
                            <option value="female">女</option>
                            <option value="other">其他</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="bio">个人简介</label>
                        <textarea id="bio" 
                                  name="bio" 
                                  rows="4" 
                                  maxlength="500" 
                                  placeholder="请简单介绍一下自己（最多500字符）"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label>
                            <input type="checkbox" name="agree" required>
                            我同意用户协议和隐私政策 *
                        </label>
                    </div>
                    
                    <button type="submit">提交表单</button>
                    <button type="reset">重置表单</button>
                </form>
            </section>
            
            <!-- 语义化标签示例 -->
            <section id="semantic">
                <h2>语义化标签示例</h2>
                
                <article>
                    <header>
                        <h3>文章标题：HTML5语义化的重要性</h3>
                        <p><time datetime="2024-12-24">发布时间：2024年12月24日</time></p>
                    </header>
                    
                    <p>HTML5引入了许多语义化标签，这些标签不仅让代码更易读，
                    还提高了网页的可访问性和SEO效果。</p>
                    
                    <aside>
                        <h4>相关链接</h4>
                        <ul>
                            <li><a href="#">HTML5规范文档</a></li>
                            <li><a href="#">Web可访问性指南</a></li>
                            <li><a href="#">SEO最佳实践</a></li>
                        </ul>
                    </aside>
                    
                    <footer>
                        <p>作者：Python教程团队</p>
                    </footer>
                </article>
                
                <details>
                    <summary>点击查看更多语义化标签说明</summary>
                    <div class="info-box">
                        <h4>常用语义化标签：</h4>
                        <ul>
                            <li><code>&lt;header&gt;</code> - 页面或区块的头部</li>
                            <li><code>&lt;nav&gt;</code> - 导航链接</li>
                            <li><code>&lt;main&gt;</code> - 主要内容</li>
                            <li><code>&lt;article&gt;</code> - 独立的文章内容</li>
                            <li><code>&lt;section&gt;</code> - 文档中的区块</li>
                            <li><code>&lt;aside&gt;</code> - 侧边栏内容</li>
                            <li><code>&lt;footer&gt;</code> - 页面或区块的底部</li>
                            <li><code>&lt;time&gt;</code> - 时间和日期</li>
                            <li><code>&lt;mark&gt;</code> - 高亮文本</li>
                            <li><code>&lt;progress&gt;</code> - 进度条</li>
                        </ul>
                    </div>
                </details>
            </section>
            
            <!-- 多媒体元素示例 -->
            <section id="multimedia">
                <h2>多媒体元素示例</h2>
                
                <h3>进度条示例</h3>
                <p>任务完成进度：</p>
                <progress value="70" max="100">70%</progress>
                <span>70%</span>
                
                <h3>高亮文本示例</h3>
                <p>这是一段普通文本，其中<mark>这部分内容被高亮显示</mark>，用于强调重要信息。</p>
                
                <h3>键盘按键示例</h3>
                <p>使用快捷键 <kbd>Ctrl</kbd> + <kbd>S</kbd> 保存文档。</p>
                
                <h3>代码示例</h3>
                <p>在JavaScript中，可以使用 <code>console.log()</code> 输出调试信息。</p>
                
                <pre><code>function greet(name) {
    console.log('Hello, ' + name + '!');
}

greet('World');</code></pre>
            </section>
        </main>
        
        <!-- 页面底部 -->
        <footer>
            <p>&copy; 2024 Python教程团队 | Session19 HTML基础示例</p>
        </footer>
    </div>
    
    <script>
        // 表单提交处理
        document.getElementById('demo-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            // 获取表单数据
            const formData = new FormData(this);
            const data = {};
            
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            
            // 显示提交的数据
            alert('表单数据：\n' + JSON.stringify(data, null, 2));
            
            // 在实际应用中，这里会发送AJAX请求到服务器
            console.log('提交的表单数据:', data);
        });
        
        // 表单验证增强
        const inputs = document.querySelectorAll('input[required]');
        inputs.forEach(input => {
            input.addEventListener('invalid', function(e) {
                e.target.setCustomValidity('');
                if (!e.target.validity.valid) {
                    switch(e.target.type) {
                        case 'email':
                            e.target.setCustomValidity('请输入有效的邮箱地址');
                            break;
                        case 'text':
                            if (e.target.validity.tooShort) {
                                e.target.setCustomValidity('输入内容太短');
                            } else if (e.target.validity.tooLong) {
                                e.target.setCustomValidity('输入内容太长');
                            } else {
                                e.target.setCustomValidity('请填写此字段');
                            }
                            break;
                        default:
                            e.target.setCustomValidity('请填写此字段');
                    }
                }
            });
            
            input.addEventListener('input', function(e) {
                e.target.setCustomValidity('');
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """
    显示HTML基础示例页面
    """
    return render_template_string(HTML_TEMPLATE)

@app.route('/submit', methods=['POST'])
def submit_form():
    """
    处理表单提交
    """
    form_data = request.form.to_dict()
    
    # 在实际应用中，这里会处理表单数据
    print("收到表单数据:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")
    
    return jsonify({
        'success': True,
        'message': '表单提交成功！',
        'data': form_data
    })

def main():
    """
    主函数
    """
    print("Session19 示例1：HTML基础示例")
    print("=" * 40)
    print("\n本示例展示了：")
    print("1. HTML5语义化标签的使用")
    print("2. 表单元素和验证属性")
    print("3. 多媒体元素的应用")
    print("4. 基本的JavaScript交互")
    print("\n访问 http://127.0.0.1:5000 查看示例")
    print("按 Ctrl+C 停止服务器")
    
    app.run(debug=True, host='127.0.0.1', port=5000)

if __name__ == '__main__':
    main()