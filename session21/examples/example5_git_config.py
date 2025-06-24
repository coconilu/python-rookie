#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session21 示例5：Git配置和最佳实践

本示例演示了Git的配置管理和最佳实践：
1. Git全局配置设置
2. 项目级配置管理
3. Git别名设置
4. .gitconfig文件管理
5. Git钩子(hooks)示例
6. 最佳实践建议

作者: Python教程团队
创建日期: 2024-01-20
"""

import os
import subprocess
from pathlib import Path
import json
from datetime import datetime
import platform


def run_command(command, cwd=None, check=True):
    """
    执行命令并返回结果
    """
    try:
        result = subprocess.run(
            command.split() if isinstance(command, str) else command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=check
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        return "", e.stderr, e.returncode
    except Exception as e:
        return "", str(e), 1


class GitConfigManager:
    """
    Git配置管理器
    """
    
    def __init__(self):
        self.system_info = self.get_system_info()
        
    def get_system_info(self):
        """
        获取系统信息
        """
        return {
            'platform': platform.system(),
            'python_version': platform.python_version(),
            'user': os.getenv('USERNAME') or os.getenv('USER', 'unknown'),
            'home': str(Path.home())
        }
    
    def check_git_installation(self):
        """
        检查Git是否已安装
        """
        print("=== 检查Git安装状态 ===")
        
        stdout, stderr, returncode = run_command("git --version", check=False)
        
        if returncode == 0:
            print(f"✓ Git已安装: {stdout}")
            return True
        else:
            print("✗ Git未安装或不在PATH中")
            print("请访问 https://git-scm.com/ 下载并安装Git")
            return False
    
    def show_current_config(self):
        """
        显示当前Git配置
        """
        print("\n=== 当前Git配置 ===")
        
        # 显示全局配置
        print("\n全局配置:")
        stdout, stderr, returncode = run_command("git config --global --list", check=False)
        
        if returncode == 0 and stdout:
            for line in stdout.split('\n'):
                if line:
                    print(f"  {line}")
        else:
            print("  未找到全局配置")
        
        # 显示系统配置
        print("\n系统配置:")
        stdout, stderr, returncode = run_command("git config --system --list", check=False)
        
        if returncode == 0 and stdout:
            for line in stdout.split('\n')[:5]:  # 只显示前5行
                if line:
                    print(f"  {line}")
            if len(stdout.split('\n')) > 5:
                print("  ...")
        else:
            print("  无法访问系统配置（可能需要管理员权限）")
    
    def setup_basic_config(self):
        """
        设置基本Git配置
        """
        print("\n=== 设置基本Git配置 ===")
        
        # 获取用户输入
        print("\n请输入您的Git配置信息:")
        
        # 用户名
        current_name, _, _ = run_command("git config --global user.name", check=False)
        default_name = current_name or self.system_info['user']
        
        name = input(f"用户名 [{default_name}]: ").strip()
        if not name:
            name = default_name
        
        # 邮箱
        current_email, _, _ = run_command("git config --global user.email", check=False)
        default_email = current_email or f"{self.system_info['user']}@example.com"
        
        email = input(f"邮箱 [{default_email}]: ").strip()
        if not email:
            email = default_email
        
        # 设置配置
        print("\n设置Git配置...")
        
        configs = [
            ("user.name", name),
            ("user.email", email),
            ("init.defaultBranch", "main"),
            ("core.autocrlf", "true" if self.system_info['platform'] == "Windows" else "input"),
            ("core.editor", "notepad" if self.system_info['platform'] == "Windows" else "nano"),
            ("pull.rebase", "false"),
            ("push.default", "simple")
        ]
        
        for key, value in configs:
            stdout, stderr, returncode = run_command(f"git config --global {key} '{value}'")
            if returncode == 0:
                print(f"✓ 设置 {key} = {value}")
            else:
                print(f"✗ 设置 {key} 失败: {stderr}")
    
    def setup_aliases(self):
        """
        设置Git别名
        """
        print("\n=== 设置Git别名 ===")
        
        aliases = {
            "st": "status",
            "co": "checkout",
            "br": "branch",
            "ci": "commit",
            "df": "diff",
            "lg": "log --oneline --graph --decorate --all",
            "last": "log -1 HEAD",
            "unstage": "reset HEAD --",
            "visual": "!gitk",
            "hist": "log --pretty=format:'%h %ad | %s%d [%an]' --graph --date=short",
            "type": "cat-file -t",
            "dump": "cat-file -p",
            "amend": "commit --amend",
            "undo": "reset --soft HEAD~1",
            "cleanup": "!git branch --merged | grep -v '\*\|main\|master' | xargs -n 1 git branch -d"
        }
        
        print("\n设置常用Git别名...")
        
        for alias, command in aliases.items():
            stdout, stderr, returncode = run_command(f"git config --global alias.{alias} '{command}'")
            if returncode == 0:
                print(f"✓ 别名 {alias} -> {command}")
            else:
                print(f"✗ 设置别名 {alias} 失败: {stderr}")
        
        print("\n现在您可以使用以下别名:")
        print("  git st     # git status")
        print("  git co     # git checkout")
        print("  git br     # git branch")
        print("  git ci     # git commit")
        print("  git lg     # 图形化日志")
        print("  git hist   # 格式化历史")
        print("  git amend  # 修改最后一次提交")
        print("  git undo   # 撤销最后一次提交（保留更改）")
    
    def create_gitignore_templates(self):
        """
        创建.gitignore模板
        """
        print("\n=== 创建.gitignore模板 ===")
        
        templates = {
            "python": '''
# Python编译文件
__pycache__/
*.py[cod]
*$py.class
*.so

# 分发/打包
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# 单元测试/覆盖率报告
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# 虚拟环境
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# 操作系统
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# 日志文件
*.log
logs/

# 数据库
*.db
*.sqlite3

# 配置文件
.env.local
.env.*.local
config/local.json
*.secret
''',
            "web": '''
# 依赖
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# 构建输出
/dist
/build

# 环境变量
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# 操作系统
.DS_Store
Thumbs.db

# 日志
*.log
logs/

# 缓存
.cache/
.parcel-cache/

# 测试覆盖率
coverage/
.nyc_output/
''',
            "general": '''
# 编译输出
*.com
*.class
*.dll
*.exe
*.o
*.so

# 包文件
*.7z
*.dmg
*.gz
*.iso
*.jar
*.rar
*.tar
*.zip

# 日志和数据库
*.log
*.sql
*.sqlite

# 操作系统生成的文件
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE和编辑器
.vscode/
.idea/
*.swp
*.swo
*~

# 临时文件
*.tmp
*.temp
temp/

# 环境配置
.env
.env.local
*.secret
'''
        }
        
        # 创建模板目录
        templates_dir = Path("gitignore_templates")
        templates_dir.mkdir(exist_ok=True)
        
        print(f"\n在 {templates_dir} 目录创建.gitignore模板...")
        
        for name, content in templates.items():
            template_file = templates_dir / f"{name}.gitignore"
            template_file.write_text(content.strip(), encoding='utf-8')
            print(f"✓ 创建 {template_file}")
        
        print("\n使用方法:")
        print(f"  复制相应的模板到您的项目根目录并重命名为 .gitignore")
        print(f"  例如: copy {templates_dir}/python.gitignore .gitignore")
    
    def create_git_hooks_examples(self):
        """
        创建Git钩子示例
        """
        print("\n=== 创建Git钩子示例 ===")
        
        hooks_dir = Path("git_hooks_examples")
        hooks_dir.mkdir(exist_ok=True)
        
        # pre-commit钩子示例
        pre_commit_hook = '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git pre-commit钩子示例

在提交前执行代码检查
"""

import sys
import subprocess
import os
from pathlib import Path

def run_command(command):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_python_syntax():
    """检查Python语法"""
    print("检查Python语法...")
    
    # 获取暂存的Python文件
    success, output = run_command("git diff --cached --name-only --diff-filter=ACM")
    if not success:
        return False
    
    python_files = [f for f in output.split('\n') if f.endswith('.py') and f]
    
    if not python_files:
        print("没有Python文件需要检查")
        return True
    
    # 检查每个文件的语法
    for file_path in python_files:
        if Path(file_path).exists():
            success, output = run_command(f"python -m py_compile {file_path}")
            if not success:
                print(f"语法错误在文件 {file_path}:")
                print(output)
                return False
            print(f"✓ {file_path}")
    
    return True

def check_commit_message():
    """检查提交消息格式（如果有的话）"""
    # 这里可以添加提交消息格式检查
    return True

def main():
    """主函数"""
    print("运行pre-commit检查...")
    
    # 检查Python语法
    if not check_python_syntax():
        print("❌ Python语法检查失败")
        sys.exit(1)
    
    # 检查提交消息
    if not check_commit_message():
        print("❌ 提交消息格式检查失败")
        sys.exit(1)
    
    print("✅ 所有检查通过")
    sys.exit(0)

if __name__ == "__main__":
    main()
'''
        
        # commit-msg钩子示例
        commit_msg_hook = '''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git commit-msg钩子示例

检查提交消息格式
"""

import sys
import re
from pathlib import Path

def check_commit_message(message):
    """检查提交消息格式"""
    
    # 基本长度检查
    if len(message) < 10:
        return False, "提交消息太短（至少10个字符）"
    
    if len(message) > 72:
        return False, "提交消息太长（最多72个字符）"
    
    # 检查是否以大写字母开头
    if not message[0].isupper():
        return False, "提交消息应以大写字母开头"
    
    # 检查是否以句号结尾
    if message.endswith('.'):
        return False, "提交消息不应以句号结尾"
    
    # 可选：检查特定格式（如Conventional Commits）
    conventional_pattern = r'^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+'
    if re.match(conventional_pattern, message):
        return True, "符合Conventional Commits格式"
    
    # 检查常见的好的提交消息模式
    good_patterns = [
        r'^Add .+',
        r'^Update .+',
        r'^Fix .+',
        r'^Remove .+',
        r'^Refactor .+',
        r'^Improve .+'
    ]
    
    for pattern in good_patterns:
        if re.match(pattern, message):
            return True, "提交消息格式良好"
    
    return True, "提交消息格式可接受"

def main():
    """主函数"""
    if len(sys.argv) != 2:
        print("用法: commit-msg <commit-message-file>")
        sys.exit(1)
    
    commit_msg_file = Path(sys.argv[1])
    
    if not commit_msg_file.exists():
        print(f"提交消息文件不存在: {commit_msg_file}")
        sys.exit(1)
    
    # 读取提交消息
    message = commit_msg_file.read_text(encoding='utf-8').strip()
    
    # 忽略注释行
    lines = [line for line in message.split('\n') if not line.startswith('#')]
    if not lines:
        print("提交消息为空")
        sys.exit(1)
    
    first_line = lines[0].strip()
    
    # 检查提交消息
    is_valid, reason = check_commit_message(first_line)
    
    if is_valid:
        print(f"✅ 提交消息检查通过: {reason}")
        sys.exit(0)
    else:
        print(f"❌ 提交消息检查失败: {reason}")
        print(f"当前消息: {first_line}")
        print("\n提交消息建议:")
        print("- 使用祈使语气（如'Add feature'而不是'Added feature'）")
        print("- 首字母大写")
        print("- 不要以句号结尾")
        print("- 保持在50个字符以内")
        print("- 清楚描述做了什么")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
        
        # 创建钩子文件
        hooks = {
            "pre-commit": pre_commit_hook,
            "commit-msg": commit_msg_hook
        }
        
        print(f"\n在 {hooks_dir} 目录创建Git钩子示例...")
        
        for name, content in hooks.items():
            hook_file = hooks_dir / f"{name}.py"
            hook_file.write_text(content.strip(), encoding='utf-8')
            print(f"✓ 创建 {hook_file}")
        
        # 创建安装说明
        install_instructions = '''
# Git钩子安装说明

## 什么是Git钩子？

Git钩子是在Git执行特定操作时自动运行的脚本。它们可以用于：
- 代码质量检查
- 自动化测试
- 提交消息格式验证
- 自动部署

## 如何安装钩子？

1. 进入您的Git仓库
2. 复制钩子文件到 .git/hooks/ 目录
3. 重命名文件（去掉.py扩展名）
4. 设置执行权限（Linux/Mac）

### Windows示例：
```cmd
copy pre-commit.py .git\\hooks\\pre-commit
copy commit-msg.py .git\\hooks\\commit-msg
```

### Linux/Mac示例：
```bash
cp pre-commit.py .git/hooks/pre-commit
cp commit-msg.py .git/hooks/commit-msg
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/commit-msg
```

## 常用钩子类型：

- **pre-commit**: 提交前执行，用于代码检查
- **commit-msg**: 检查提交消息格式
- **pre-push**: 推送前执行，用于测试
- **post-commit**: 提交后执行，用于通知
- **pre-receive**: 服务器端，接收前执行
- **post-receive**: 服务器端，接收后执行

## 注意事项：

1. 钩子文件必须是可执行的
2. 钩子返回非零值会阻止操作继续
3. 钩子不会被Git跟踪，需要手动分发
4. 可以使用任何编程语言编写钩子
'''
        
        readme_file = hooks_dir / "README.md"
        readme_file.write_text(install_instructions.strip(), encoding='utf-8')
        print(f"✓ 创建 {readme_file}")
        
        print("\n钩子示例创建完成！")
        print(f"请查看 {hooks_dir}/README.md 了解安装方法")
    
    def show_best_practices(self):
        """
        显示Git最佳实践
        """
        print("\n=== Git最佳实践建议 ===")
        
        practices = [
            {
                "category": "提交实践",
                "items": [
                    "经常提交，保持提交粒度小",
                    "写清楚的提交消息",
                    "一次提交只做一件事",
                    "提交前检查代码",
                    "使用祈使语气写提交消息"
                ]
            },
            {
                "category": "分支管理",
                "items": [
                    "使用功能分支进行开发",
                    "保持主分支稳定",
                    "及时删除已合并的分支",
                    "使用有意义的分支名称",
                    "定期同步远程分支"
                ]
            },
            {
                "category": "协作开发",
                "items": [
                    "使用Pull Request进行代码审查",
                    "遵循团队的Git工作流",
                    "及时解决合并冲突",
                    "保持本地仓库更新",
                    "不要强制推送到共享分支"
                ]
            },
            {
                "category": "安全实践",
                "items": [
                    "不要提交敏感信息",
                    "使用.gitignore忽略不必要的文件",
                    "定期备份重要仓库",
                    "使用SSH密钥进行身份验证",
                    "启用两因素认证"
                ]
            }
        ]
        
        for practice in practices:
            print(f"\n{practice['category']}:")
            for item in practice['items']:
                print(f"  • {item}")
        
        print("\n常用Git命令速查:")
        commands = [
            ("git status", "查看工作区状态"),
            ("git add .", "添加所有更改到暂存区"),
            ("git commit -m 'message'", "提交更改"),
            ("git push origin main", "推送到远程仓库"),
            ("git pull origin main", "从远程仓库拉取更新"),
            ("git checkout -b feature", "创建并切换到新分支"),
            ("git merge feature", "合并分支"),
            ("git log --oneline", "查看提交历史"),
            ("git diff", "查看更改差异"),
            ("git reset HEAD~1", "撤销最后一次提交")
        ]
        
        for command, description in commands:
            print(f"  {command:<25} # {description}")
    
    def export_config_backup(self):
        """
        导出Git配置备份
        """
        print("\n=== 导出Git配置备份 ===")
        
        backup_data = {
            "timestamp": datetime.now().isoformat(),
            "system_info": self.system_info,
            "global_config": {},
            "aliases": {}
        }
        
        # 获取全局配置
        stdout, stderr, returncode = run_command("git config --global --list", check=False)
        
        if returncode == 0 and stdout:
            for line in stdout.split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    if key.startswith('alias.'):
                        backup_data['aliases'][key[6:]] = value
                    else:
                        backup_data['global_config'][key] = value
        
        # 保存备份文件
        backup_file = Path(f"git_config_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ 配置备份已保存到: {backup_file}")
        print(f"  包含 {len(backup_data['global_config'])} 个配置项")
        print(f"  包含 {len(backup_data['aliases'])} 个别名")
        
        return backup_file


def main():
    """
    主函数
    """
    print("Git配置和最佳实践工具")
    print("=" * 50)
    
    config_manager = GitConfigManager()
    
    # 检查Git安装
    if not config_manager.check_git_installation():
        return
    
    # 显示当前配置
    config_manager.show_current_config()
    
    # 交互式菜单
    while True:
        print("\n=== 选择操作 ===")
        print("1. 设置基本Git配置")
        print("2. 设置Git别名")
        print("3. 创建.gitignore模板")
        print("4. 创建Git钩子示例")
        print("5. 查看最佳实践建议")
        print("6. 导出配置备份")
        print("7. 显示当前配置")
        print("0. 退出")
        
        choice = input("\n请选择操作 [0-7]: ").strip()
        
        if choice == '1':
            config_manager.setup_basic_config()
        elif choice == '2':
            config_manager.setup_aliases()
        elif choice == '3':
            config_manager.create_gitignore_templates()
        elif choice == '4':
            config_manager.create_git_hooks_examples()
        elif choice == '5':
            config_manager.show_best_practices()
        elif choice == '6':
            config_manager.export_config_backup()
        elif choice == '7':
            config_manager.show_current_config()
        elif choice == '0':
            print("\n感谢使用Git配置工具！")
            break
        else:
            print("无效选择，请重试")


if __name__ == "__main__":
    main()