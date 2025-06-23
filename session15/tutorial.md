# Session15: 数据库操作详细教程

## 引言：为什么需要数据库？

想象一下，你正在开发一个图书管理系统：
- 没有数据库：每次程序关闭，所有图书信息都会丢失
- 使用文件：可以保存数据，但查找、修改很麻烦
- 使用数据库：数据持久保存，查询快速，操作方便

数据库就像是一个**超级智能的文件柜**，不仅能存储数据，还能快速查找、排序、统计。

## 1. 数据库基础概念

### 1.1 什么是数据库？

```python
# 数据库类比：
# 数据库 = 图书馆
# 表 = 书架（按类别分）
# 行 = 一本书
# 列 = 书的属性（书名、作者、ISBN等）

# 例如：图书表
# | ID | 书名           | 作者   | 价格  | 库存 |
# |----|---------------|--------|-------|------|
# | 1  | Python编程    | 张三   | 59.00 | 10   |
# | 2  | 数据库入门    | 李四   | 49.00 | 5    |
# | 3  | Web开发实战   | 王五   | 69.00 | 8    |
```

### 1.2 为什么选择SQLite？

SQLite是最适合初学者的数据库：
1. **无需安装**：Python自带SQLite支持
2. **轻量级**：整个数据库就是一个文件
3. **功能完整**：支持标准SQL语法
4. **广泛应用**：手机APP、浏览器都在用

## 2. SQLite数据库基础操作

### 2.1 连接数据库

```python
import sqlite3

def connect_database():
    """连接到SQLite数据库"""
    # 连接到数据库（如果不存在会自动创建）
    conn = sqlite3.connect('library.db')
    
    # 创建游标对象（用于执行SQL命令）
    cursor = conn.cursor()
    
    print("成功连接到数据库！")
    
    return conn, cursor

# 使用示例
conn, cursor = connect_database()

# 记得关闭连接
conn.close()
```

### 2.2 创建表

```python
def create_books_table():
    """创建图书表"""
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # SQL语句：创建表
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        isbn TEXT UNIQUE,
        price REAL DEFAULT 0.0,
        stock INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''
    
    # 执行SQL语句
    cursor.execute(create_table_sql)
    
    # 提交更改
    conn.commit()
    
    print("图书表创建成功！")
    
    conn.close()

# 执行创建表
create_books_table()
```

## 3. CRUD操作（增删改查）

### 3.1 Create - 插入数据

```python
def add_book(title, author, isbn, price, stock):
    """添加新书"""
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # 使用参数化查询（防止SQL注入）
    insert_sql = '''
    INSERT INTO books (title, author, isbn, price, stock)
    VALUES (?, ?, ?, ?, ?)
    '''
    
    try:
        cursor.execute(insert_sql, (title, author, isbn, price, stock))
        conn.commit()
        print(f"成功添加图书：{title}")
        return cursor.lastrowid  # 返回新插入记录的ID
    except sqlite3.IntegrityError:
        print(f"添加失败：ISBN {isbn} 已存在")
        return None
    finally:
        conn.close()

# 添加几本书
add_book("Python编程：从入门到实践", "Eric Matthes", "978-7-115-42802-8", 89.00, 20)
add_book("流畅的Python", "Luciano Ramalho", "978-7-115-45415-7", 139.00, 15)
add_book("数据库系统概念", "Abraham Silberschatz", "978-7-111-37529-6", 99.00, 10)
```

### 3.2 Read - 查询数据

```python
def get_all_books():
    """获取所有图书"""
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    
    print("\n图书列表：")
    print("-" * 80)
    print(f"{'ID':<5} {'书名':<30} {'作者':<20} {'价格':<10} {'库存':<10}")
    print("-" * 80)
    
    for book in books:
        print(f"{book[0]:<5} {book[1]:<30} {book[2]:<20} ¥{book[4]:<10.2f} {book[5]:<10}")
    
    conn.close()
    return books

def search_books_by_author(author):
    """根据作者查找图书"""
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # 使用LIKE进行模糊查询
    cursor.execute("SELECT * FROM books WHERE author LIKE ?", (f'%{author}%',))
    books = cursor.fetchall()
    
    conn.close()
    return books

def get_book_by_id(book_id):
    """根据ID获取图书详情"""
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    
    conn.close()
    return book
```

### 3.3 Update - 更新数据

```python
def update_book_price(book_id, new_price):
    """更新图书价格"""
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    update_sql = "UPDATE books SET price = ? WHERE id = ?"
    cursor.execute(update_sql, (new_price, book_id))
    
    if cursor.rowcount > 0:
        conn.commit()
        print(f"成功更新图书ID {book_id} 的价格为 ¥{new_price}")
    else:
        print(f"未找到ID为 {book_id} 的图书")
    
    conn.close()

def update_stock(book_id, quantity_change):
    """更新库存（增加或减少）"""
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # 先获取当前库存
    cursor.execute("SELECT stock FROM books WHERE id = ?", (book_id,))
    result = cursor.fetchone()
    
    if result:
        current_stock = result[0]
        new_stock = current_stock + quantity_change
        
        if new_stock >= 0:
            cursor.execute("UPDATE books SET stock = ? WHERE id = ?", 
                         (new_stock, book_id))
            conn.commit()
            print(f"库存更新成功：{current_stock} → {new_stock}")
        else:
            print("错误：库存不能为负数")
    else:
        print(f"未找到ID为 {book_id} 的图书")
    
    conn.close()
```

### 3.4 Delete - 删除数据

```python
def delete_book(book_id):
    """删除图书"""
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # 先检查图书是否存在
    cursor.execute("SELECT title FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    
    if book:
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        print(f"成功删除图书：{book[0]}")
    else:
        print(f"未找到ID为 {book_id} 的图书")
    
    conn.close()
```

## 4. 高级查询技巧

### 4.1 条件查询

```python
def advanced_search():
    """高级查询示例"""
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # 1. 查询价格在50-100之间的图书
    print("\n价格在50-100元之间的图书：")
    cursor.execute("SELECT * FROM books WHERE price BETWEEN ? AND ?", (50, 100))
    for book in cursor.fetchall():
        print(f"- {book[1]}: ¥{book[4]}")
    
    # 2. 查询库存小于10的图书
    print("\n库存预警（少于10本）：")
    cursor.execute("SELECT * FROM books WHERE stock < ?", (10,))
    for book in cursor.fetchall():
        print(f"- {book[1]}: 剩余{book[5]}本")
    
    # 3. 按价格排序
    print("\n按价格从高到低排序：")
    cursor.execute("SELECT * FROM books ORDER BY price DESC")
    for book in cursor.fetchall():
        print(f"- {book[1]}: ¥{book[4]}")
    
    conn.close()
```

### 4.2 聚合函数

```python
def statistics():
    """统计信息"""
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # 总库存量
    cursor.execute("SELECT SUM(stock) FROM books")
    total_stock = cursor.fetchone()[0]
    print(f"图书总库存：{total_stock}本")
    
    # 平均价格
    cursor.execute("SELECT AVG(price) FROM books")
    avg_price = cursor.fetchone()[0]
    print(f"图书平均价格：¥{avg_price:.2f}")
    
    # 最贵的书
    cursor.execute("SELECT * FROM books ORDER BY price DESC LIMIT 1")
    expensive_book = cursor.fetchone()
    print(f"最贵的书：{expensive_book[1]} - ¥{expensive_book[4]}")
    
    # 图书总数
    cursor.execute("SELECT COUNT(*) FROM books")
    total_books = cursor.fetchone()[0]
    print(f"图书种类总数：{total_books}种")
    
    conn.close()
```

## 5. 事务处理

事务确保数据操作的完整性：

```python
def transfer_books(from_book_id, to_book_id, quantity):
    """图书调拨（事务示例）"""
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    try:
        # 开始事务
        conn.execute('BEGIN')
        
        # 减少源图书库存
        cursor.execute(
            "UPDATE books SET stock = stock - ? WHERE id = ? AND stock >= ?",
            (quantity, from_book_id, quantity)
        )
        
        if cursor.rowcount == 0:
            raise Exception("源图书库存不足")
        
        # 增加目标图书库存
        cursor.execute(
            "UPDATE books SET stock = stock + ? WHERE id = ?",
            (quantity, to_book_id)
        )
        
        if cursor.rowcount == 0:
            raise Exception("目标图书不存在")
        
        # 提交事务
        conn.commit()
        print(f"成功调拨{quantity}本图书")
        
    except Exception as e:
        # 回滚事务
        conn.rollback()
        print(f"调拨失败：{e}")
        
    finally:
        conn.close()
```

## 6. 使用上下文管理器

更优雅的数据库连接管理：

```python
class DatabaseConnection:
    """数据库连接上下文管理器"""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        # 设置行工厂，使结果可以像字典一样访问
        self.conn.row_factory = sqlite3.Row
        return self.conn
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

# 使用示例
def get_books_with_context():
    """使用上下文管理器查询"""
    with DatabaseConnection('library.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        
        for row in cursor.fetchall():
            # 可以像字典一样访问
            print(f"{row['title']} by {row['author']}")
```

## 7. 数据库设计最佳实践

### 7.1 创建多个相关表

```python
def create_complete_library_schema():
    """创建完整的图书馆数据库架构"""
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    
    # 用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 借阅记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS borrowings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        borrow_date DATE DEFAULT CURRENT_DATE,
        return_date DATE,
        status TEXT DEFAULT 'borrowed',
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (book_id) REFERENCES books(id)
    )
    ''')
    
    # 创建索引提高查询性能
    cursor.execute('CREATE INDEX idx_borrowings_user ON borrowings(user_id)')
    cursor.execute('CREATE INDEX idx_borrowings_book ON borrowings(book_id)')
    
    conn.commit()
    conn.close()
    print("完整的数据库架构创建成功！")
```

### 7.2 数据验证

```python
def validate_book_data(title, author, isbn, price, stock):
    """验证图书数据"""
    errors = []
    
    if not title or len(title.strip()) == 0:
        errors.append("书名不能为空")
    
    if not author or len(author.strip()) == 0:
        errors.append("作者不能为空")
    
    if isbn and not isbn.replace('-', '').isdigit():
        errors.append("ISBN格式不正确")
    
    if price < 0:
        errors.append("价格不能为负数")
    
    if stock < 0:
        errors.append("库存不能为负数")
    
    return errors
```

## 8. 完整的图书管理系统示例

```python
class BookManager:
    """图书管理器类"""
    
    def __init__(self, db_name='library.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                price REAL DEFAULT 0.0,
                stock INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
    
    def add_book(self, title, author, isbn, price, stock):
        """添加图书"""
        errors = validate_book_data(title, author, isbn, price, stock)
        if errors:
            print("数据验证失败：")
            for error in errors:
                print(f"- {error}")
            return False
        
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO books (title, author, isbn, price, stock) VALUES (?, ?, ?, ?, ?)",
                    (title, author, isbn, price, stock)
                )
                print(f"成功添加图书：{title}")
                return True
            except sqlite3.IntegrityError:
                print(f"添加失败：ISBN {isbn} 已存在")
                return False
    
    def search_books(self, keyword):
        """搜索图书"""
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM books WHERE title LIKE ? OR author LIKE ?",
                (f'%{keyword}%', f'%{keyword}%')
            )
            return cursor.fetchall()
    
    def display_inventory(self):
        """显示库存清单"""
        with DatabaseConnection(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books ORDER BY title")
            books = cursor.fetchall()
            
            if not books:
                print("图书库是空的")
                return
            
            print("\n" + "="*100)
            print(f"{'ID':<5} {'书名':<30} {'作者':<20} {'ISBN':<20} {'价格':<10} {'库存':<10}")
            print("="*100)
            
            for book in books:
                print(f"{book['id']:<5} {book['title']:<30} {book['author']:<20} "
                      f"{book['isbn']:<20} ¥{book['price']:<10.2f} {book['stock']:<10}")
            
            # 统计信息
            cursor.execute("SELECT COUNT(*), SUM(stock), AVG(price) FROM books")
            count, total_stock, avg_price = cursor.fetchone()
            print("="*100)
            print(f"总计：{count}种图书，{total_stock}本，平均价格：¥{avg_price:.2f}")
```

## 总结

本课我们学习了：
1. 数据库的基本概念
2. SQLite的连接和基本操作
3. CRUD操作的实现
4. 高级查询技巧
5. 事务处理
6. 数据库设计最佳实践
7. 完整的图书管理系统实现

记住：
- 始终使用参数化查询防止SQL注入
- 记得关闭数据库连接或使用上下文管理器
- 合理设计表结构，使用外键保证数据完整性
- 为常用查询字段创建索引提高性能

## 练习建议

1. 扩展图书管理系统，添加用户管理和借阅功能
2. 实现图书分类功能
3. 添加数据导入导出功能（CSV/JSON）
4. 创建简单的统计报表
5. 尝试使用SQLAlchemy ORM简化数据库操作

继续加油！掌握数据库操作是成为全栈开发者的重要一步！ 