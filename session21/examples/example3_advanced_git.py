#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session21 示例3：Git高级功能和最佳实践

本示例演示了Git的高级功能：
1. .gitignore的使用
2. Git stash（暂存工作）
3. 撤销操作
4. 标签管理
5. 远程仓库操作模拟

作者: Python教程团队
创建日期: 2024-01-20
"""

import os
import subprocess
from pathlib import Path
import shutil
import tempfile


def run_git_command(command, cwd=None, check=True):
    """
    执行Git命令并返回结果
    """
    try:
        result = subprocess.run(
            command.split() if isinstance(command, str) else command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check
        )
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        return None, e.stderr


def setup_advanced_demo():
    """
    设置高级演示仓库
    """
    demo_dir = Path("git_advanced_demo")
    if demo_dir.exists():
        shutil.rmtree(demo_dir)
    
    demo_dir.mkdir()
    os.chdir(demo_dir)
    
    # 初始化仓库
    run_git_command("git init")
    run_git_command("git config user.name 'Advanced User'")
    run_git_command("git config user.email 'advanced@example.com'")
    
    # 创建项目结构
    create_project_structure()
    
    return demo_dir


def create_project_structure():
    """
    创建项目结构
    """
    # 创建目录结构
    dirs = ['src', 'tests', 'docs', 'config', 'logs', 'temp']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    
    # 创建主要文件
    files_content = {
        'src/main.py': '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主应用程序
"""

import sys
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class Application:
    def __init__(self):
        self.name = "高级Git演示应用"
        self.version = "1.0.0"
        logger.info(f"初始化应用: {self.name} v{self.version}")
    
    def run(self):
        logger.info("应用开始运行")
        print(f"欢迎使用 {self.name}!")
        print(f"版本: {self.version}")
        logger.info("应用运行完成")

def main():
    app = Application()
    app.run()

if __name__ == "__main__":
    main()
''',
        'src/utils.py': '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
"""

import json
import hashlib
from datetime import datetime
from typing import Any, Dict, List

def hash_string(text: str) -> str:
    """计算字符串的SHA256哈希值"""
    return hashlib.sha256(text.encode()).hexdigest()

def save_json(data: Dict[str, Any], filepath: str) -> bool:
    """保存数据到JSON文件"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存JSON文件失败: {e}")
        return False

def load_json(filepath: str) -> Dict[str, Any]:
    """从JSON文件加载数据"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载JSON文件失败: {e}")
        return {}

def get_timestamp() -> str:
    """获取当前时间戳"""
    return datetime.now().isoformat()

def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"
''',
        'tests/test_utils.py': '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数测试
"""

import unittest
import tempfile
import os
from pathlib import Path

# 添加src目录到路径
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils import hash_string, save_json, load_json, format_file_size

class TestUtils(unittest.TestCase):
    
    def test_hash_string(self):
        """测试字符串哈希"""
        text = "Hello, World!"
        hash1 = hash_string(text)
        hash2 = hash_string(text)
        
        # 相同输入应该产生相同哈希
        self.assertEqual(hash1, hash2)
        
        # 哈希应该是64字符的十六进制字符串
        self.assertEqual(len(hash1), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in hash1))
    
    def test_json_operations(self):
        """测试JSON操作"""
        test_data = {
            "name": "测试",
            "version": "1.0.0",
            "features": ["功能1", "功能2"]
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # 测试保存
            result = save_json(test_data, temp_file)
            self.assertTrue(result)
            
            # 测试加载
            loaded_data = load_json(temp_file)
            self.assertEqual(test_data, loaded_data)
        
        finally:
            # 清理临时文件
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_format_file_size(self):
        """测试文件大小格式化"""
        self.assertEqual(format_file_size(0), "0B")
        self.assertEqual(format_file_size(1024), "1.0KB")
        self.assertEqual(format_file_size(1048576), "1.0MB")
        self.assertEqual(format_file_size(1073741824), "1.0GB")

if __name__ == '__main__':
    unittest.main()
''',
        'config/app.json': '''{
  "app": {
    "name": "高级Git演示应用",
    "version": "1.0.0",
    "debug": true
  },
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "demo_db"
  },
  "logging": {
    "level": "INFO",
    "file": "logs/app.log"
  }
}
''',
        'README.md': '''# 高级Git演示项目

这是一个用于演示Git高级功能的示例项目。

## 项目结构

```
├── src/           # 源代码
├── tests/         # 测试文件
├── docs/          # 文档
├── config/        # 配置文件
├── logs/          # 日志文件
└── temp/          # 临时文件
```

## 功能特性

- 模块化代码结构
- 完整的测试覆盖
- 配置文件管理
- 日志记录
- 工具函数库

## 使用方法

```bash
# 运行主程序
python src/main.py

# 运行测试
python -m unittest tests/test_utils.py
```

## 开发指南

1. 所有新功能都应该在独立分支上开发
2. 提交前请运行测试
3. 遵循代码规范
4. 更新相关文档
'''
    }
    
    # 写入文件
    for filepath, content in files_content.items():
        file_path = Path(filepath)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
    
    # 创建一些临时文件和日志文件
    Path('logs/app.log').write_text('2024-01-20 10:00:00 - INFO - 应用启动\n')
    Path('logs/debug.log').write_text('2024-01-20 10:00:01 - DEBUG - 调试信息\n')
    Path('temp/cache.tmp').write_text('临时缓存数据')
    Path('temp/session.tmp').write_text('会话临时数据')
    
    # 创建编译文件目录
    Path('src/__pycache__').mkdir(exist_ok=True)
    Path('src/__pycache__/main.cpython-39.pyc').write_text('编译后的Python字节码')
    Path('src/__pycache__/utils.cpython-39.pyc').write_text('编译后的Python字节码')


def demo_gitignore():
    """
    演示.gitignore的使用
    """
    print("\n=== .gitignore演示 ===")
    
    # 1. 查看当前状态（包含所有文件）
    print("\n1. 查看当前状态（包含临时文件）")
    print("$ git status")
    output, _ = run_git_command("git status")
    print(output)
    
    # 2. 创建.gitignore文件
    print("\n2. 创建.gitignore文件")
    gitignore_content = '''# Python编译文件
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.so

# 虚拟环境
venv/
env/
ENV/
.venv/

# IDE文件
.vscode/
.idea/
*.swp
*.swo
*~

# 操作系统文件
.DS_Store
Thumbs.db

# 日志文件
*.log
logs/

# 临时文件
*.tmp
*.temp
temp/

# 配置文件（包含敏感信息）
.env
*.secret
config/local.json

# 数据库文件
*.db
*.sqlite3

# 构建输出
build/
dist/
*.egg-info/

# 测试覆盖率报告
.coverage
htmlcov/
.pytest_cache/

# 文档构建
docs/_build/
'''
    
    Path('.gitignore').write_text(gitignore_content, encoding='utf-8')
    print("创建了 .gitignore 文件")
    
    # 3. 再次查看状态（临时文件被忽略）
    print("\n3. 查看状态（临时文件被忽略）")
    print("$ git status")
    output, _ = run_git_command("git status")
    print(output)
    
    # 4. 添加并提交项目文件
    print("\n4. 添加项目文件")
    print("$ git add .")
    run_git_command("git add .")
    
    print("$ git commit -m 'Initial project setup with .gitignore'")
    output, _ = run_git_command("git commit -m 'Initial project setup with .gitignore'")
    print(output)


def demo_stash():
    """
    演示Git stash功能
    """
    print("\n=== Git Stash演示 ===")
    
    # 1. 修改一些文件
    print("\n1. 修改文件（模拟正在进行的工作）")
    
    # 修改main.py
    main_content = Path('src/main.py').read_text()
    modified_content = main_content.replace(
        'self.version = "1.0.0"',
        'self.version = "1.1.0"  # 正在开发新版本'
    )
    Path('src/main.py').write_text(modified_content, encoding='utf-8')
    
    # 添加新文件
    Path('src/new_feature.py').write_text('''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新功能模块（开发中）
"""

def new_feature():
    """新功能函数"""
    print("这是一个正在开发的新功能")
    # TODO: 实现具体功能
    pass
''', encoding='utf-8')
    
    print("修改了 src/main.py")
    print("添加了 src/new_feature.py")
    
    # 2. 查看当前状态
    print("\n2. 查看当前工作状态")
    print("$ git status")
    output, _ = run_git_command("git status")
    print(output)
    
    # 3. 暂存当前工作
    print("\n3. 暂存当前工作（需要紧急修复bug）")
    print("$ git stash push -m '正在开发新功能v1.1.0'")
    output, _ = run_git_command("git stash push -m '正在开发新功能v1.1.0'")
    print(output)
    
    # 4. 查看暂存列表
    print("\n4. 查看暂存列表")
    print("$ git stash list")
    output, _ = run_git_command("git stash list")
    print(output)
    
    # 5. 查看工作目录（已恢复到干净状态）
    print("\n5. 查看工作目录状态")
    print("$ git status")
    output, _ = run_git_command("git status")
    print(output)
    
    # 6. 进行紧急修复
    print("\n6. 进行紧急bug修复")
    utils_content = Path('src/utils.py').read_text()
    fixed_content = utils_content.replace(
        'print(f"保存JSON文件失败: {e}")',
        'print(f"保存JSON文件失败: {e}")\n        # 修复：添加错误日志记录\n        import logging\n        logging.error(f"JSON保存失败: {e}")'
    )
    Path('src/utils.py').write_text(fixed_content, encoding='utf-8')
    
    print("$ git add src/utils.py")
    run_git_command("git add src/utils.py")
    
    print("$ git commit -m 'hotfix: 修复JSON保存错误处理'")
    output, _ = run_git_command("git commit -m 'hotfix: 修复JSON保存错误处理'")
    print(output)
    
    # 7. 恢复之前的工作
    print("\n7. 恢复之前暂存的工作")
    print("$ git stash pop")
    output, _ = run_git_command("git stash pop")
    print(output)
    
    # 8. 查看恢复后的状态
    print("\n8. 查看恢复后的工作状态")
    print("$ git status")
    output, _ = run_git_command("git status")
    print(output)


def demo_reset_and_revert():
    """
    演示撤销操作
    """
    print("\n=== 撤销操作演示 ===")
    
    # 1. 提交当前工作
    print("\n1. 提交当前开发工作")
    print("$ git add .")
    run_git_command("git add .")
    
    print("$ git commit -m 'WIP: 开发新功能v1.1.0'")
    output, _ = run_git_command("git commit -m 'WIP: 开发新功能v1.1.0'")
    print(output)
    
    # 2. 查看提交历史
    print("\n2. 查看提交历史")
    print("$ git log --oneline")
    output, _ = run_git_command("git log --oneline")
    print(output)
    
    # 3. 演示reset（撤销提交但保留更改）
    print("\n3. 撤销最后一次提交（保留更改）")
    print("$ git reset HEAD~1")
    output, _ = run_git_command("git reset HEAD~1")
    print(output)
    
    print("$ git status")
    output, _ = run_git_command("git status")
    print(output)
    
    # 4. 重新提交
    print("\n4. 重新提交（修改提交信息）")
    print("$ git add .")
    run_git_command("git add .")
    
    print("$ git commit -m 'feat: 添加新功能模块v1.1.0'")
    output, _ = run_git_command("git commit -m 'feat: 添加新功能模块v1.1.0'")
    print(output)
    
    # 5. 创建一个"错误"的提交
    print("\n5. 创建一个错误的提交（模拟）")
    Path('src/bug.py').write_text('''# 这是一个有bug的文件
def buggy_function():
    return 1/0  # 这会导致除零错误
''', encoding='utf-8')
    
    print("$ git add src/bug.py")
    run_git_command("git add src/bug.py")
    
    print("$ git commit -m 'add buggy code (mistake)'")
    output, _ = run_git_command("git commit -m 'add buggy code (mistake)'")
    print(output)
    
    # 6. 使用revert撤销错误提交
    print("\n6. 使用revert撤销错误提交")
    print("$ git log --oneline -3")
    output, _ = run_git_command("git log --oneline -3")
    print(output)
    
    # 获取最后一次提交的哈希
    last_commit = output.split('\n')[0].split()[0]
    
    print(f"$ git revert {last_commit} --no-edit")
    output, _ = run_git_command(f"git revert {last_commit} --no-edit")
    print(output)
    
    # 7. 查看最终状态
    print("\n7. 查看撤销后的状态")
    print("$ git log --oneline -5")
    output, _ = run_git_command("git log --oneline -5")
    print(output)


def demo_tags():
    """
    演示标签管理
    """
    print("\n=== 标签管理演示 ===")
    
    # 1. 创建轻量标签
    print("\n1. 创建轻量标签")
    print("$ git tag v1.0.0")
    output, _ = run_git_command("git tag v1.0.0")
    print("创建了轻量标签 v1.0.0")
    
    # 2. 创建附注标签
    print("\n2. 创建附注标签")
    print("$ git tag -a v1.1.0 -m 'Release version 1.1.0 with new features'")
    output, _ = run_git_command("git tag -a v1.1.0 -m 'Release version 1.1.0 with new features'")
    print("创建了附注标签 v1.1.0")
    
    # 3. 查看所有标签
    print("\n3. 查看所有标签")
    print("$ git tag")
    output, _ = run_git_command("git tag")
    print(output)
    
    # 4. 查看标签信息
    print("\n4. 查看标签详细信息")
    print("$ git show v1.1.0")
    output, _ = run_git_command("git show v1.1.0")
    print(output[:500] + "..." if len(output) > 500 else output)
    
    # 5. 列出标签（带模式匹配）
    print("\n5. 列出v1.*标签")
    print("$ git tag -l 'v1.*'")
    output, _ = run_git_command("git tag -l 'v1.*'")
    print(output)


def demo_remote_simulation():
    """
    模拟远程仓库操作
    """
    print("\n=== 远程仓库操作模拟 ===")
    
    # 1. 创建"远程"仓库（实际是本地的bare仓库）
    print("\n1. 创建模拟远程仓库")
    remote_dir = Path("../remote_repo.git")
    if remote_dir.exists():
        shutil.rmtree(remote_dir)
    
    print("$ git clone --bare . ../remote_repo.git")
    output, _ = run_git_command("git clone --bare . ../remote_repo.git")
    print("创建了模拟远程仓库")
    
    # 2. 添加远程仓库
    print("\n2. 添加远程仓库")
    print("$ git remote add origin ../remote_repo.git")
    output, _ = run_git_command("git remote add origin ../remote_repo.git")
    
    # 3. 查看远程仓库
    print("\n3. 查看远程仓库")
    print("$ git remote -v")
    output, _ = run_git_command("git remote -v")
    print(output)
    
    # 4. 推送到远程仓库
    print("\n4. 推送到远程仓库")
    print("$ git push -u origin main")
    output, _ = run_git_command("git push -u origin main")
    print("推送成功")
    
    # 5. 推送标签
    print("\n5. 推送标签")
    print("$ git push origin --tags")
    output, _ = run_git_command("git push origin --tags")
    print("标签推送成功")
    
    # 6. 模拟从远程拉取
    print("\n6. 从远程仓库获取更新")
    print("$ git fetch origin")
    output, _ = run_git_command("git fetch origin")
    print("获取远程更新完成")


def advanced_git_demo():
    """
    运行完整的高级Git演示
    """
    print("Git高级功能和最佳实践演示")
    print("=" * 60)
    
    try:
        # 设置演示环境
        demo_dir = setup_advanced_demo()
        
        # 运行各个演示
        demo_gitignore()
        demo_stash()
        demo_reset_and_revert()
        demo_tags()
        demo_remote_simulation()
        
        print("\n=== 演示完成 ===")
        print("\n掌握的高级Git技能:")
        print("1. .gitignore文件的正确使用")
        print("2. Git stash暂存工作")
        print("3. 撤销操作（reset vs revert）")
        print("4. 标签管理")
        print("5. 远程仓库操作")
        print("\n最佳实践建议:")
        print("- 经常提交，保持提交历史清晰")
        print("- 使用有意义的提交信息")
        print("- 合理使用分支进行功能开发")
        print("- 定期推送到远程仓库")
        print("- 使用标签标记重要版本")
        
    except Exception as e:
        print(f"演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 返回上级目录
        os.chdir("..")


if __name__ == "__main__":
    advanced_git_demo()