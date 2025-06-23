# 个人博客系统

一个基于Flask框架的简单个人博客系统，适合初学者学习和使用。

## 功能特性

- 📝 文章管理（创建、编辑、删除）
- 🏷️ 标签系统
- 🔍 全文搜索
- 📊 浏览统计
- 🔐 简单的认证系统
- 📱 响应式设计

## 技术栈

- **后端**: Flask (Python)
- **模板引擎**: Jinja2
- **数据存储**: JSON文件
- **前端**: HTML5 + CSS3 + JavaScript
- **样式**: 自定义CSS（无需框架）

## 项目结构

```
blog/
├── app.py              # 主应用文件
├── templates/          # 模板文件
│   ├── base.html      # 基础模板
│   ├── index.html     # 首页
│   ├── post.html      # 文章详情
│   ├── new_post.html  # 新建文章
│   ├── edit_post.html # 编辑文章
│   ├── admin.html     # 管理页面
│   ├── about.html     # 关于页面
│   ├── 404.html       # 404错误页
│   └── 500.html       # 500错误页
├── static/            # 静态文件
│   ├── css/
│   │   └── style.css  # 样式文件
│   └── js/
│       └── script.js  # JavaScript文件
├── data/              # 数据存储
│   └── posts.json     # 文章数据
└── README.md          # 本文件
```

## 安装和运行

### 1. 安装依赖

```bash
# 确保已安装Python 3.7+
# 安装Flask
pip install flask

# 或使用uv
uv add flask
```

### 2. 运行应用

```bash
python app.py

# 或使用uv
uv run python app.py
```

### 3. 访问应用

在浏览器中打开 http://127.0.0.1:5000

## 使用说明

### 管理员账号

- 用户名: `admin`
- 密码: `password`

### 写文章

1. 点击"写新文章"或访问 `/new`
2. 需要管理员认证
3. 填写标题、内容和标签
4. 支持Markdown语法

### 管理文章

1. 访问 `/admin` 进入管理页面
2. 可以查看、编辑、删除所有文章
3. 查看文章统计信息

### 搜索功能

在导航栏的搜索框中输入关键词，可以搜索文章标题、内容和标签。

## 数据存储

本系统使用JSON文件存储数据，适合小型个人博客使用。数据文件位于 `data/posts.json`。

每篇文章包含以下字段：
- `id`: 文章ID
- `title`: 标题
- `content`: 内容
- `author`: 作者
- `created_at`: 创建时间
- `updated_at`: 更新时间
- `tags`: 标签列表
- `views`: 浏览次数

## 自定义配置

### 修改站点名称

在 `app.py` 中修改：

```python
@app.context_processor
def inject_globals():
    return {
        'site_name': '我的个人博客',  # 修改这里
        ...
    }
```

### 修改管理员密码

在 `app.py` 中修改 `require_auth` 装饰器：

```python
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != 'admin' or auth.password != 'password':  # 修改这里
            ...
```

## 部署建议

### 开发环境

当前配置适合开发环境使用。

### 生产环境

1. 关闭调试模式：`app.run(debug=False)`
2. 使用生产级WSGI服务器（如Gunicorn）
3. 配置反向代理（如Nginx）
4. 使用环境变量管理敏感信息
5. 考虑使用真实数据库（如SQLite、PostgreSQL）

## 扩展功能建议

- 评论系统
- 分类功能
- 文章草稿
- RSS订阅
- 社交分享
- 更完善的用户系统
- 图片上传
- Markdown实时预览

## 常见问题

### Q: 如何备份数据？
A: 直接备份 `data/posts.json` 文件即可。

### Q: 如何迁移到数据库？
A: 可以编写脚本读取JSON文件，然后插入到数据库中。

### Q: 如何添加新的页面？
A: 1. 在 `app.py` 中添加新路由
   2. 创建对应的模板文件
   3. 在导航栏中添加链接

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 作者

Flask学习者

---

Happy Blogging! 🎉 