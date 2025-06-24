# Session25: 部署与运维 - 练习题

本目录包含与部署与运维相关的练习题，帮助你巩固所学知识并应用到实际场景中。

## 练习内容

### 基础练习

1. **虚拟环境管理**：创建并配置一个虚拟环境，安装指定的依赖包，并编写脚本验证环境配置。

2. **依赖管理**：为一个现有项目创建pyproject.toml文件，并使用uv管理依赖。

### 应用练习

3. **部署配置生成**：编写一个脚本，自动生成Gunicorn配置文件、Nginx配置文件和systemd服务文件。

4. **Docker容器化**：为一个Flask应用创建Dockerfile和docker-compose.yml，实现容器化部署。

### 挑战练习

5. **CI/CD流水线**：使用GitHub Actions为一个Python项目创建完整的CI/CD流水线，包括测试、构建和部署步骤。

## 提交要求

1. 每个练习题的解答应放在单独的Python文件中
2. 文件命名格式：`exercise<题号>.py`（例如：`exercise1.py`）
3. 每个文件顶部应包含题目描述和解题思路
4. 代码应包含详细注释
5. 解答应放在`solutions`目录下

## 评分标准

- **功能完整性**：代码能够正确实现要求的功能
- **代码质量**：遵循PEP 8规范，代码结构清晰
- **错误处理**：包含适当的错误处理和日志记录
- **文档质量**：注释和文档清晰易懂
- **创新性**：在挑战练习中展示创新思维

## 参考资源

- [uv文档](https://github.com/astral-sh/uv)
- [Gunicorn配置文档](https://docs.gunicorn.org/en/stable/configure.html)
- [Docker官方文档](https://docs.docker.com/)
- [GitHub Actions文档](https://docs.github.com/en/actions)