# Session21: 版本控制 - Git 详细教程

## 1. 版本控制概述

### 1.1 什么是版本控制？

版本控制是一种记录一个或若干文件内容变化，以便将来查阅特定版本修订情况的系统。它可以帮助我们：

- **追踪文件变更**：记录每次修改的内容、时间和作者
- **版本管理**：保存文件的不同版本，可以随时回退
- **协作开发**：多人同时修改同一项目而不会冲突
- **备份恢复**：防止代码丢失，提供完整的历史记录

### 1.2 为什么需要版本控制？

想象一下没有版本控制的开发场景：

```
项目文件夹/
├── main.py
├── main_backup.py
├── main_final.py
├── main_final_v2.py
├── main_really_final.py
└── main_this_time_really_final.py
```

这种方式存在诸多问题：
- 文件命名混乱
- 无法知道具体修改了什么
- 多人协作时容易覆盖他人的工作
- 占用大量存储空间
- 难以追踪bug的引入时间

### 1.3 Git简介

Git是目前世界上最先进的分布式版本控制系统，具有以下特点：

- **分布式**：每个开发者都有完整的版本历史
- **高效**：处理大型项目时性能优异
- **安全**：使用SHA-1哈希确保数据完整性
- **灵活**：支持多种工作流程
- **开源**：免费且社区活跃

## 2. Git安装和配置

### 2.1 安装Git

**Windows用户：**
1. 访问 https://git-scm.com/download/win
2. 下载并安装Git for Windows
3. 安装过程中保持默认设置即可

**macOS用户：**
```bash
# 使用Homebrew安装
brew install git

# 或者从官网下载安装包
# https://git-scm.com/download/mac
```

**Linux用户：**
```bash
# Ubuntu/Debian
sudo apt-get install git

# CentOS/RHEL
sudo yum install git
```

### 2.2 验证安装

```bash
git --version
# 输出类似：git version 2.34.1
```

### 2.3 初始配置

安装Git后，需要设置用户信息：

```bash
# 设置用户名
git config --global user.name "你的姓名"

# 设置邮箱
git config --global user.email "your.email@example.com"

# 设置默认编辑器（可选）
git config --global core.editor "code --wait"  # VS Code

# 查看配置
git config --list
```

## 3. Git基础概念

### 3.1 三个工作区域

Git有三个主要的工作区域：

1. **工作目录（Working Directory）**：你当前正在编辑的文件
2. **暂存区（Staging Area）**：准备提交的文件快照
3. **Git仓库（Repository）**：存储项目历史的地方

```
工作目录 ──add──> 暂存区 ──commit──> Git仓库
    ↑                              ↓
    └──────────checkout──────────────┘
```

### 3.2 文件状态

Git中的文件有四种状态：

- **未跟踪（Untracked）**：新创建的文件，Git还不知道它的存在
- **已修改（Modified）**：文件已被修改但还没有暂存
- **已暂存（Staged）**：文件已被添加到暂存区
- **已提交（Committed）**：文件已安全地保存在Git仓库中

## 4. Git基本操作

### 4.1 创建仓库

#### 初始化新仓库

```bash
# 创建项目目录
mkdir my-project
cd my-project

# 初始化Git仓库
git init

# 查看仓库状态
git status
```

#### 克隆现有仓库

```bash
# 克隆远程仓库
git clone https://github.com/username/repository.git

# 克隆到指定目录
git clone https://github.com/username/repository.git my-folder
```

### 4.2 基本工作流程

#### 添加文件到暂存区

```bash
# 添加单个文件
git add filename.py

# 添加多个文件
git add file1.py file2.py

# 添加所有文件
git add .

# 添加所有Python文件
git add *.py
```

#### 查看状态

```bash
# 查看仓库状态
git status

# 简洁格式
git status -s
```

#### 提交更改

```bash
# 提交暂存区的文件
git commit -m "提交信息"

# 添加并提交（跳过暂存区）
git commit -am "提交信息"

# 修改最后一次提交
git commit --amend -m "新的提交信息"
```

#### 查看提交历史

```bash
# 查看提交历史
git log

# 简洁格式
git log --oneline

# 图形化显示
git log --graph --oneline

# 查看最近3次提交
git log -3
```

### 4.3 查看差异

```bash
# 查看工作目录和暂存区的差异
git diff

# 查看暂存区和最后一次提交的差异
git diff --staged

# 查看两次提交之间的差异
git diff commit1 commit2
```

### 4.4 撤销操作

```bash
# 撤销工作目录的修改
git checkout -- filename.py

# 撤销暂存区的文件
git reset HEAD filename.py

# 回退到上一次提交
git reset --hard HEAD~1

# 回退到指定提交
git reset --hard commit_hash
```

## 5. 分支管理

### 5.1 分支概念

分支是Git最强大的功能之一。它允许你：
- 并行开发不同功能
- 实验新想法而不影响主代码
- 为不同版本维护独立的代码线

### 5.2 分支操作

```bash
# 查看所有分支
git branch

# 创建新分支
git branch feature-login

# 切换分支
git checkout feature-login

# 创建并切换分支（推荐）
git checkout -b feature-login

# 新版本Git命令
git switch feature-login
git switch -c feature-login
```

### 5.3 合并分支

```bash
# 切换到主分支
git checkout main

# 合并功能分支
git merge feature-login

# 删除已合并的分支
git branch -d feature-login

# 强制删除分支
git branch -D feature-login
```

### 5.4 解决冲突

当合并分支时可能出现冲突：

```bash
# 合并时出现冲突
git merge feature-branch
# Auto-merging file.py
# CONFLICT (content): Merge conflict in file.py
# Automatic merge failed; fix conflicts and then commit the result.

# 查看冲突文件
git status

# 手动编辑冲突文件，解决冲突后
git add file.py
git commit -m "解决合并冲突"
```

冲突文件的格式：
```python
<<<<<<< HEAD
# 当前分支的代码
print("Hello from main branch")
=======
# 要合并分支的代码
print("Hello from feature branch")
>>>>>>> feature-branch
```

## 6. 远程仓库

### 6.1 添加远程仓库

```bash
# 添加远程仓库
git remote add origin https://github.com/username/repository.git

# 查看远程仓库
git remote -v

# 查看远程仓库详细信息
git remote show origin
```

### 6.2 推送和拉取

```bash
# 推送到远程仓库
git push origin main

# 首次推送并设置上游分支
git push -u origin main

# 拉取远程更新
git pull origin main

# 获取远程更新但不合并
git fetch origin
```

### 6.3 协作工作流程

典型的团队协作流程：

1. **克隆仓库**
```bash
git clone https://github.com/team/project.git
cd project
```

2. **创建功能分支**
```bash
git checkout -b feature/user-authentication
```

3. **开发和提交**
```bash
# 编写代码
git add .
git commit -m "实现用户认证功能"
```

4. **推送分支**
```bash
git push origin feature/user-authentication
```

5. **创建Pull Request**（在GitHub/GitLab等平台）

6. **代码审查和合并**

7. **同步主分支**
```bash
git checkout main
git pull origin main
git branch -d feature/user-authentication
```

## 7. Git最佳实践

### 7.1 提交信息规范

好的提交信息应该：
- 简洁明了，描述做了什么
- 使用现在时态
- 首行不超过50字符
- 如需详细说明，空一行后添加

```bash
# 好的提交信息
git commit -m "添加用户登录功能"
git commit -m "修复密码验证bug"
git commit -m "重构数据库连接模块"

# 不好的提交信息
git commit -m "修改"
git commit -m "bug fix"
git commit -m "更新代码"
```

### 7.2 .gitignore文件

创建`.gitignore`文件来忽略不需要版本控制的文件：

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
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
*.egg-info/
.installed.cfg
*.egg

# 虚拟环境
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# 操作系统
.DS_Store
Thumbs.db

# 日志文件
*.log

# 数据库
*.db
*.sqlite3

# 配置文件（包含敏感信息）
.env
config.ini
```

### 7.3 分支策略

**Git Flow策略：**
- `main`：生产环境代码
- `develop`：开发环境代码
- `feature/*`：功能开发分支
- `release/*`：发布准备分支
- `hotfix/*`：紧急修复分支

**GitHub Flow策略（推荐）：**
- `main`：主分支，始终可部署
- `feature/*`：功能分支，从main创建，完成后合并回main

### 7.4 常用Git别名

设置Git别名提高效率：

```bash
# 设置别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.unstage 'reset HEAD --'
git config --global alias.last 'log -1 HEAD'
git config --global alias.visual '!gitk'

# 使用别名
git st  # 等同于 git status
git co main  # 等同于 git checkout main
```

## 8. 常见问题和解决方案

### 8.1 忘记添加文件到.gitignore

```bash
# 如果文件已经被跟踪，需要先移除
git rm --cached filename
# 然后添加到.gitignore
echo "filename" >> .gitignore
git add .gitignore
git commit -m "添加.gitignore规则"
```

### 8.2 撤销已推送的提交

```bash
# 创建一个新提交来撤销之前的提交
git revert commit_hash

# 注意：不要使用reset来撤销已推送的提交
# 这会导致其他开发者的仓库出现问题
```

### 8.3 修改提交历史

```bash
# 交互式重写最近3次提交
git rebase -i HEAD~3

# 在编辑器中可以：
# pick：保持提交
# reword：修改提交信息
# edit：修改提交内容
# squash：合并到上一个提交
# drop：删除提交
```

### 8.4 暂存当前工作

```bash
# 暂存当前修改
git stash

# 查看暂存列表
git stash list

# 恢复最近的暂存
git stash pop

# 恢复指定的暂存
git stash apply stash@{0}

# 删除暂存
git stash drop stash@{0}
```

## 9. Git图形化工具

虽然命令行是最强大的方式，但图形化工具可以帮助理解Git的工作原理：

- **内置工具**：`gitk`、`git gui`
- **第三方工具**：
  - SourceTree（免费）
  - GitKraken（部分免费）
  - GitHub Desktop（免费）
  - VS Code Git插件

## 10. 总结

Git是现代软件开发不可或缺的工具。通过本课程的学习，你应该掌握：

1. **基础概念**：工作区、暂存区、仓库的关系
2. **基本操作**：add、commit、push、pull等命令
3. **分支管理**：创建、切换、合并分支
4. **协作开发**：与团队成员协作的工作流程
5. **最佳实践**：提交规范、分支策略等

记住，Git的学习是一个渐进的过程。开始时可能觉得复杂，但随着实践的增加，你会发现Git是一个非常强大和灵活的工具。

## 11. 扩展阅读

- [Pro Git Book](https://git-scm.com/book/zh/v2)（官方文档，中文版）
- [Git教程 - 廖雪峰](https://www.liaoxuefeng.com/wiki/896043488029600)
- [GitHub官方Git手册](https://guides.github.com/)
- [Atlassian Git教程](https://www.atlassian.com/git/tutorials)

## 12. 下节预告

下一课我们将学习**测试驱动开发（TDD）**，了解如何编写测试用例来确保代码质量，以及如何使用Python的unittest和pytest框架进行自动化测试。