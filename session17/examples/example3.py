"""
示例3：表单处理
演示Flask中各种表单处理方法
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash, make_response, session
import os
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-for-session'

# 配置文件上传
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 创建上传目录
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 模拟数据存储
users = []
feedback_list = []


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 1. 基本表单处理
@app.route('/', methods=['GET', 'POST'])
def basic_form():
    """基本表单处理示例"""
    if request.method == 'POST':
        # 获取表单数据
        username = request.form.get('username')
        email = request.form.get('email')
        age = request.form.get('age')
        
        # 简单验证
        if not username or not email:
            flash('用户名和邮箱是必填项！', 'error')
        else:
            flash(f'欢迎，{username}！您的信息已收到。', 'success')
            print(f"收到表单数据: 用户名={username}, 邮箱={email}, 年龄={age}")
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>基本表单示例</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            form { background: #f0f0f0; padding: 20px; border-radius: 5px; }
            label { display: block; margin-top: 10px; }
            input { width: 100%; padding: 5px; margin-top: 5px; }
            button { margin-top: 15px; padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .flash { padding: 10px; margin: 10px 0; border-radius: 3px; }
            .flash.success { background: #d4edda; color: #155724; }
            .flash.error { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <h1>基本表单示例</h1>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST">
            <label for="username">用户名（必填）：</label>
            <input type="text" id="username" name="username" required>
            
            <label for="email">邮箱（必填）：</label>
            <input type="email" id="email" name="email" required>
            
            <label for="age">年龄：</label>
            <input type="number" id="age" name="age" min="1" max="150">
            
            <button type="submit">提交</button>
        </form>
        
        <p><a href="/advanced">高级表单示例</a> | <a href="/upload">文件上传示例</a></p>
    </body>
    </html>
    '''
    
    return render_template_string(template)


# 2. 高级表单处理
@app.route('/advanced', methods=['GET', 'POST'])
def advanced_form():
    """高级表单处理示例"""
    if request.method == 'POST':
        # 获取各种类型的表单数据
        data = {
            'name': request.form.get('name'),
            'password': request.form.get('password'),
            'gender': request.form.get('gender'),
            'hobbies': request.form.getlist('hobbies'),  # 获取多选框数据
            'city': request.form.get('city'),
            'bio': request.form.get('bio'),
            'newsletter': 'newsletter' in request.form,
            'terms': 'terms' in request.form
        }
        
        # 验证
        if not data['name'] or not data['password']:
            flash('姓名和密码是必填项！', 'error')
        elif not data['terms']:
            flash('请同意服务条款！', 'error')
        else:
            # 保存数据
            users.append(data)
            flash('注册成功！', 'success')
            # 重定向到成功页面
            return redirect(url_for('registration_success'))
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>高级表单示例</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            form { background: #f0f0f0; padding: 20px; border-radius: 5px; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input[type="text"], input[type="password"], select, textarea {
                width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 3px;
            }
            input[type="radio"], input[type="checkbox"] { margin-right: 5px; }
            .radio-group, .checkbox-group { margin: 5px 0; }
            button { padding: 10px 20px; background: #28a745; color: white; border: none; border-radius: 3px; cursor: pointer; }
            button:hover { background: #218838; }
            .flash { padding: 10px; margin: 10px 0; border-radius: 3px; }
            .flash.success { background: #d4edda; color: #155724; }
            .flash.error { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <h1>高级表单示例</h1>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST">
            <div class="form-group">
                <label for="name">姓名：*</label>
                <input type="text" id="name" name="name" required>
            </div>
            
            <div class="form-group">
                <label for="password">密码：*</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <div class="form-group">
                <label>性别：</label>
                <div class="radio-group">
                    <label><input type="radio" name="gender" value="male"> 男</label>
                    <label><input type="radio" name="gender" value="female"> 女</label>
                    <label><input type="radio" name="gender" value="other"> 其他</label>
                </div>
            </div>
            
            <div class="form-group">
                <label>兴趣爱好：</label>
                <div class="checkbox-group">
                    <label><input type="checkbox" name="hobbies" value="reading"> 阅读</label>
                    <label><input type="checkbox" name="hobbies" value="sports"> 运动</label>
                    <label><input type="checkbox" name="hobbies" value="music"> 音乐</label>
                    <label><input type="checkbox" name="hobbies" value="travel"> 旅行</label>
                    <label><input type="checkbox" name="hobbies" value="coding"> 编程</label>
                </div>
            </div>
            
            <div class="form-group">
                <label for="city">城市：</label>
                <select id="city" name="city">
                    <option value="">请选择</option>
                    <option value="beijing">北京</option>
                    <option value="shanghai">上海</option>
                    <option value="guangzhou">广州</option>
                    <option value="shenzhen">深圳</option>
                    <option value="other">其他</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="bio">个人简介：</label>
                <textarea id="bio" name="bio" rows="4" placeholder="介绍一下自己..."></textarea>
            </div>
            
            <div class="form-group">
                <label><input type="checkbox" name="newsletter"> 订阅新闻通讯</label>
                <label><input type="checkbox" name="terms" required> 同意服务条款 *</label>
            </div>
            
            <button type="submit">注册</button>
        </form>
        
        <p><a href="/">基本表单示例</a> | <a href="/upload">文件上传示例</a> | <a href="/users">查看注册用户</a></p>
    </body>
    </html>
    '''
    
    return render_template_string(template)


# 3. 注册成功页面
@app.route('/success')
def registration_success():
    """注册成功页面"""
    return '''
    <h1>注册成功！</h1>
    <p>感谢您的注册。</p>
    <p><a href="/advanced">返回注册页面</a> | <a href="/users">查看所有用户</a></p>
    '''


# 4. 显示注册用户
@app.route('/users')
def show_users():
    """显示所有注册用户"""
    template = '''
    <h1>注册用户列表</h1>
    <table border="1" cellpadding="5">
        <tr>
            <th>姓名</th>
            <th>性别</th>
            <th>城市</th>
            <th>兴趣爱好</th>
            <th>订阅新闻</th>
        </tr>
        {% for user in users %}
        <tr>
            <td>{{ user.name }}</td>
            <td>{{ user.gender or '-' }}</td>
            <td>{{ user.city or '-' }}</td>
            <td>{{ ', '.join(user.hobbies) if user.hobbies else '-' }}</td>
            <td>{{ '是' if user.newsletter else '否' }}</td>
        </tr>
        {% endfor %}
    </table>
    <p>共 {{ users|length }} 位用户</p>
    <p><a href="/advanced">返回注册页面</a></p>
    '''
    
    return render_template_string(template, users=users)


# 5. 文件上传
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """文件上传示例"""
    uploaded_files = []
    
    if request.method == 'POST':
        # 检查是否有文件
        if 'file' not in request.files:
            flash('没有选择文件！', 'error')
        else:
            file = request.files['file']
            
            # 检查文件名
            if file.filename == '':
                flash('没有选择文件！', 'error')
            elif file and allowed_file(file.filename):
                # 安全的文件名
                filename = secure_filename(file.filename)
                # 添加时间戳避免重名
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                
                # 保存文件
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                flash(f'文件 {filename} 上传成功！', 'success')
                
                # 获取文件信息
                file_info = {
                    'name': filename,
                    'size': os.path.getsize(filepath),
                    'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                uploaded_files.append(file_info)
            else:
                flash('不允许的文件类型！', 'error')
    
    # 获取已上传的文件列表
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(filepath):
                uploaded_files.append({
                    'name': filename,
                    'size': os.path.getsize(filepath),
                    'upload_time': datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
                })
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>文件上传示例</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .upload-form { background: #f0f0f0; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
            .file-list { background: #f9f9f9; padding: 20px; border-radius: 5px; }
            button { padding: 10px 20px; background: #17a2b8; color: white; border: none; border-radius: 3px; cursor: pointer; }
            button:hover { background: #138496; }
            .flash { padding: 10px; margin: 10px 0; border-radius: 3px; }
            .flash.success { background: #d4edda; color: #155724; }
            .flash.error { background: #f8d7da; color: #721c24; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h1>文件上传示例</h1>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <div class="upload-form">
            <h2>上传文件</h2>
            <form method="POST" enctype="multipart/form-data">
                <p>允许的文件类型：{{ ', '.join(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx']) }}</p>
                <p>最大文件大小：16MB</p>
                <input type="file" name="file" required>
                <button type="submit">上传</button>
            </form>
        </div>
        
        <div class="file-list">
            <h2>已上传的文件</h2>
            {% if uploaded_files %}
                <table>
                    <tr>
                        <th>文件名</th>
                        <th>大小</th>
                        <th>上传时间</th>
                    </tr>
                    {% for file in uploaded_files %}
                    <tr>
                        <td>{{ file.name }}</td>
                        <td>{{ file.size }} 字节</td>
                        <td>{{ file.upload_time }}</td>
                    </tr>
                    {% endfor %}
                </table>
            {% else %}
                <p>还没有上传任何文件。</p>
            {% endif %}
        </div>
        
        <p><a href="/">基本表单示例</a> | <a href="/advanced">高级表单示例</a></p>
    </body>
    </html>
    '''
    
    return render_template_string(template, uploaded_files=uploaded_files)


# 6. AJAX表单处理
@app.route('/ajax-form')
def ajax_form():
    """AJAX表单示例"""
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AJAX表单示例</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .form-container { background: #f0f0f0; padding: 20px; border-radius: 5px; }
            input, textarea { width: 100%; padding: 8px; margin: 5px 0; }
            button { padding: 10px 20px; background: #ffc107; color: #000; border: none; border-radius: 3px; cursor: pointer; }
            button:hover { background: #e0a800; }
            #result { margin-top: 20px; padding: 15px; border-radius: 5px; display: none; }
            #result.success { background: #d4edda; color: #155724; }
            #result.error { background: #f8d7da; color: #721c24; }
            #loading { display: none; color: #666; }
        </style>
    </head>
    <body>
        <h1>AJAX表单示例</h1>
        
        <div class="form-container">
            <h2>反馈表单（无刷新提交）</h2>
            <form id="feedbackForm">
                <label for="name">姓名：</label>
                <input type="text" id="name" name="name" required>
                
                <label for="email">邮箱：</label>
                <input type="email" id="email" name="email" required>
                
                <label for="rating">评分：</label>
                <select id="rating" name="rating">
                    <option value="5">⭐⭐⭐⭐⭐ 非常满意</option>
                    <option value="4">⭐⭐⭐⭐ 满意</option>
                    <option value="3">⭐⭐⭐ 一般</option>
                    <option value="2">⭐⭐ 不满意</option>
                    <option value="1">⭐ 非常不满意</option>
                </select>
                
                <label for="feedback">反馈内容：</label>
                <textarea id="feedback" name="feedback" rows="4" required></textarea>
                
                <button type="submit">提交反馈</button>
                <span id="loading">提交中...</span>
            </form>
        </div>
        
        <div id="result"></div>
        
        <p><a href="/">返回首页</a> | <a href="/feedback-list">查看所有反馈</a></p>
        
        <script>
        document.getElementById('feedbackForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            // 显示加载状态
            document.getElementById('loading').style.display = 'inline';
            document.querySelector('button[type="submit"]').disabled = true;
            
            // 收集表单数据
            const formData = new FormData(this);
            const data = {};
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            
            // 发送AJAX请求
            fetch('/submit-feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                // 隐藏加载状态
                document.getElementById('loading').style.display = 'none';
                document.querySelector('button[type="submit"]').disabled = false;
                
                // 显示结果
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                resultDiv.className = result.status === 'success' ? 'success' : 'error';
                resultDiv.innerHTML = result.message;
                
                // 如果成功，清空表单
                if (result.status === 'success') {
                    document.getElementById('feedbackForm').reset();
                }
            })
            .catch(error => {
                document.getElementById('loading').style.display = 'none';
                document.querySelector('button[type="submit"]').disabled = false;
                
                const resultDiv = document.getElementById('result');
                resultDiv.style.display = 'block';
                resultDiv.className = 'error';
                resultDiv.innerHTML = '提交失败，请稍后重试。';
            });
        });
        </script>
    </body>
    </html>
    '''
    
    return render_template_string(template)


# 7. 处理AJAX提交
@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    """处理AJAX反馈表单提交"""
    data = request.get_json()
    
    # 验证数据
    if not data or not data.get('name') or not data.get('email') or not data.get('feedback'):
        return jsonify({
            'status': 'error',
            'message': '请填写所有必填项！'
        }), 400
    
    # 保存反馈
    feedback = {
        'id': len(feedback_list) + 1,
        'name': data.get('name'),
        'email': data.get('email'),
        'rating': int(data.get('rating', 5)),
        'feedback': data.get('feedback'),
        'submitted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    feedback_list.append(feedback)
    
    return jsonify({
        'status': 'success',
        'message': f'感谢您的反馈，{feedback["name"]}！我们已收到您的意见。',
        'feedback_id': feedback['id']
    })


# 8. 显示反馈列表
@app.route('/feedback-list')
def show_feedback():
    """显示所有反馈"""
    template = '''
    <h1>用户反馈列表</h1>
    <style>
        .feedback-item { background: #f9f9f9; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .rating { color: #ffc107; }
    </style>
    
    {% for feedback in feedback_list %}
    <div class="feedback-item">
        <h3>{{ feedback.name }} <span class="rating">{{ '⭐' * feedback.rating }}</span></h3>
        <p><small>{{ feedback.email }} - {{ feedback.submitted_at }}</small></p>
        <p>{{ feedback.feedback }}</p>
    </div>
    {% else %}
    <p>还没有收到任何反馈。</p>
    {% endfor %}
    
    <p><a href="/ajax-form">返回反馈表单</a></p>
    '''
    
    return render_template_string(template, feedback_list=feedback_list)


# 9. 表单验证示例
@app.route('/validation', methods=['GET', 'POST'])
def form_validation():
    """客户端和服务端表单验证示例"""
    errors = {}
    form_data = {}
    
    if request.method == 'POST':
        # 获取表单数据
        form_data = {
            'username': request.form.get('username', '').strip(),
            'email': request.form.get('email', '').strip(),
            'password': request.form.get('password', ''),
            'confirm_password': request.form.get('confirm_password', ''),
            'age': request.form.get('age', '').strip(),
            'website': request.form.get('website', '').strip()
        }
        
        # 服务端验证
        import re
        
        # 用户名验证
        if not form_data['username']:
            errors['username'] = '用户名不能为空'
        elif len(form_data['username']) < 3:
            errors['username'] = '用户名至少3个字符'
        elif not re.match(r'^[a-zA-Z0-9_]+$', form_data['username']):
            errors['username'] = '用户名只能包含字母、数字和下划线'
        
        # 邮箱验证
        if not form_data['email']:
            errors['email'] = '邮箱不能为空'
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', form_data['email']):
            errors['email'] = '邮箱格式不正确'
        
        # 密码验证
        if not form_data['password']:
            errors['password'] = '密码不能为空'
        elif len(form_data['password']) < 6:
            errors['password'] = '密码至少6个字符'
        elif form_data['password'] != form_data['confirm_password']:
            errors['confirm_password'] = '两次密码输入不一致'
        
        # 年龄验证
        if form_data['age']:
            try:
                age = int(form_data['age'])
                if age < 1 or age > 150:
                    errors['age'] = '年龄必须在1-150之间'
            except ValueError:
                errors['age'] = '年龄必须是数字'
        
        # 网址验证
        if form_data['website']:
            if not re.match(r'^https?://[\w\-\.]+\.[a-zA-Z]{2,}', form_data['website']):
                errors['website'] = '网址格式不正确'
        
        # 如果没有错误，处理表单
        if not errors:
            flash('表单验证通过！', 'success')
            # 这里可以保存数据到数据库
            return redirect(url_for('form_validation'))
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>表单验证示例</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .form-container { max-width: 500px; margin: 0 auto; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 3px; }
            input.error { border-color: #dc3545; }
            .error-message { color: #dc3545; font-size: 14px; margin-top: 5px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .flash { padding: 10px; margin: 10px 0; border-radius: 3px; }
            .flash.success { background: #d4edda; color: #155724; }
            .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h1>表单验证示例</h1>
            
            <div class="info">
                <strong>验证规则：</strong>
                <ul>
                    <li>用户名：3个字符以上，只能包含字母、数字和下划线</li>
                    <li>邮箱：有效的邮箱格式</li>
                    <li>密码：至少6个字符</li>
                    <li>年龄：1-150之间的数字（可选）</li>
                    <li>网址：有效的URL格式（可选）</li>
                </ul>
            </div>
            
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="flash {{ category }}">{{ message }}</div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
            
            <form method="POST" id="validationForm">
                <div class="form-group">
                    <label for="username">用户名：*</label>
                    <input type="text" id="username" name="username" value="{{ form_data.get('username', '') }}" 
                           class="{{ 'error' if errors.get('username') else '' }}" required>
                    {% if errors.get('username') %}
                        <div class="error-message">{{ errors.username }}</div>
                    {% endif %}
                </div>
                
                <div class="form-group">
                    <label for="email">邮箱：*</label>
                    <input type="email" id="email" name="email" value="{{ form_data.get('email', '') }}"
                           class="{{ 'error' if errors.get('email') else '' }}" required>
                    {% if errors.get('email') %}
                        <div class="error-message">{{ errors.email }}</div>
                    {% endif %}
                </div>
                
                <div class="form-group">
                    <label for="password">密码：*</label>
                    <input type="password" id="password" name="password"
                           class="{{ 'error' if errors.get('password') else '' }}" required>
                    {% if errors.get('password') %}
                        <div class="error-message">{{ errors.password }}</div>
                    {% endif %}
                </div>
                
                <div class="form-group">
                    <label for="confirm_password">确认密码：*</label>
                    <input type="password" id="confirm_password" name="confirm_password"
                           class="{{ 'error' if errors.get('confirm_password') else '' }}" required>
                    {% if errors.get('confirm_password') %}
                        <div class="error-message">{{ errors.confirm_password }}</div>
                    {% endif %}
                </div>
                
                <div class="form-group">
                    <label for="age">年龄：</label>
                    <input type="number" id="age" name="age" value="{{ form_data.get('age', '') }}"
                           class="{{ 'error' if errors.get('age') else '' }}" min="1" max="150">
                    {% if errors.get('age') %}
                        <div class="error-message">{{ errors.age }}</div>
                    {% endif %}
                </div>
                
                <div class="form-group">
                    <label for="website">个人网站：</label>
                    <input type="url" id="website" name="website" value="{{ form_data.get('website', '') }}"
                           class="{{ 'error' if errors.get('website') else '' }}" placeholder="https://example.com">
                    {% if errors.get('website') %}
                        <div class="error-message">{{ errors.website }}</div>
                    {% endif %}
                </div>
                
                <button type="submit">提交</button>
            </form>
            
            <p><a href="/">返回首页</a></p>
        </div>
        
        <script>
        // 客户端验证（可选，提供更好的用户体验）
        document.getElementById('validationForm').addEventListener('submit', function(e) {
            // 这里可以添加客户端验证逻辑
            // 但记住：永远不要只依赖客户端验证！
        });
        </script>
    </body>
    </html>
    '''
    
    return render_template_string(template, errors=errors, form_data=form_data)


if __name__ == '__main__':
    print("表单处理示例")
    print("访问以下路由查看不同的表单功能：")
    print("- / : 基本表单")
    print("- /advanced : 高级表单（各种输入类型）")
    print("- /upload : 文件上传")
    print("- /ajax-form : AJAX表单提交")
    print("- /validation : 表单验证")
    app.run(debug=True) 