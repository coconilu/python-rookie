#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session30 示例2: CI/CD自动化部署管道

本示例演示如何构建完整的CI/CD自动化部署管道，包括：
- GitHub Actions工作流
- 自动化测试
- 代码质量检查
- 自动部署到云平台
- 部署状态监控

作者: Python教程团队
创建日期: 2024-01-20
"""

import os
import json
import yaml
import requests
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class CICDPipelineGenerator:
    """
    CI/CD管道生成器
    
    自动生成GitHub Actions工作流和相关配置文件
    """
    
    def __init__(self, project_name: str, repo_name: str):
        self.project_name = project_name
        self.repo_name = repo_name
        self.workflows_dir = Path(".github/workflows")
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_ci_workflow(self, 
                           python_versions: List[str] = None,
                           test_command: str = "pytest",
                           coverage_threshold: int = 80) -> str:
        """
        生成CI工作流
        
        Args:
            python_versions: Python版本列表
            test_command: 测试命令
            coverage_threshold: 代码覆盖率阈值
        
        Returns:
            str: CI工作流内容
        """
        if python_versions is None:
            python_versions = ["3.9", "3.10", "3.11"]
        
        workflow = {
            'name': 'CI Pipeline',
            'on': {
                'push': {
                    'branches': ['main', 'develop']
                },
                'pull_request': {
                    'branches': ['main']
                }
            },
            'jobs': {
                'test': {
                    'runs-on': 'ubuntu-latest',
                    'strategy': {
                        'matrix': {
                            'python-version': python_versions
                        }
                    },
                    'steps': [
                        {
                            'name': 'Checkout code',
                            'uses': 'actions/checkout@v4'
                        },
                        {
                            'name': 'Set up Python ${{ matrix.python-version }}',
                            'uses': 'actions/setup-python@v4',
                            'with': {
                                'python-version': '${{ matrix.python-version }}'
                            }
                        },
                        {
                            'name': 'Cache dependencies',
                            'uses': 'actions/cache@v3',
                            'with': {
                                'path': '~/.cache/pip',
                                'key': '${{ runner.os }}-pip-${{ hashFiles("**/requirements*.txt") }}',
                                'restore-keys': '${{ runner.os }}-pip-'
                            }
                        },
                        {
                            'name': 'Install dependencies',
                            'run': '\n'.join([
                                'python -m pip install --upgrade pip',
                                'pip install -r requirements.txt',
                                'pip install pytest pytest-cov flake8 black isort mypy'
                            ])
                        },
                        {
                            'name': 'Code formatting check',
                            'run': '\n'.join([
                                'black --check .',
                                'isort --check-only .'
                            ])
                        },
                        {
                            'name': 'Lint with flake8',
                            'run': '\n'.join([
                                'flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics',
                                'flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics'
                            ])
                        },
                        {
                            'name': 'Type checking with mypy',
                            'run': 'mypy . --ignore-missing-imports'
                        },
                        {
                            'name': 'Run tests with coverage',
                            'run': f'{test_command} --cov=. --cov-report=xml --cov-fail-under={coverage_threshold}'
                        },
                        {
                            'name': 'Upload coverage to Codecov',
                            'uses': 'codecov/codecov-action@v3',
                            'with': {
                                'file': './coverage.xml',
                                'flags': 'unittests',
                                'name': 'codecov-umbrella'
                            }
                        }
                    ]
                },
                'security-scan': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {
                            'name': 'Checkout code',
                            'uses': 'actions/checkout@v4'
                        },
                        {
                            'name': 'Run security scan',
                            'uses': 'securecodewarrior/github-action-add-sarif@v1',
                            'with': {
                                'sarif-file': 'security-scan-results.sarif'
                            }
                        },
                        {
                            'name': 'Check for vulnerabilities',
                            'run': '\n'.join([
                                'pip install safety bandit',
                                'safety check',
                                'bandit -r . -f json -o bandit-report.json'
                            ])
                        }
                    ]
                }
            }
        }
        
        workflow_content = yaml.dump(workflow, default_flow_style=False, sort_keys=False)
        
        ci_path = self.workflows_dir / "ci.yml"
        with open(ci_path, 'w', encoding='utf-8') as f:
            f.write(workflow_content)
        
        print(f"✅ CI工作流已生成: {ci_path}")
        return workflow_content
    
    def generate_cd_workflow(self, 
                           deployment_env: str = "production",
                           docker_registry: str = "ghcr.io",
                           k8s_cluster: Optional[str] = None) -> str:
        """
        生成CD工作流
        
        Args:
            deployment_env: 部署环境
            docker_registry: Docker镜像仓库
            k8s_cluster: Kubernetes集群名称
        
        Returns:
            str: CD工作流内容
        """
        workflow = {
            'name': 'CD Pipeline',
            'on': {
                'push': {
                    'branches': ['main']
                },
                'workflow_run': {
                    'workflows': ['CI Pipeline'],
                    'types': ['completed'],
                    'branches': ['main']
                }
            },
            'env': {
                'REGISTRY': docker_registry,
                'IMAGE_NAME': f'{self.repo_name}'
            },
            'jobs': {
                'build-and-push': {
                    'runs-on': 'ubuntu-latest',
                    'if': "${{ github.event.workflow_run.conclusion == 'success' }}",
                    'permissions': {
                        'contents': 'read',
                        'packages': 'write'
                    },
                    'steps': [
                        {
                            'name': 'Checkout code',
                            'uses': 'actions/checkout@v4'
                        },
                        {
                            'name': 'Set up Docker Buildx',
                            'uses': 'docker/setup-buildx-action@v3'
                        },
                        {
                            'name': 'Log in to Container Registry',
                            'uses': 'docker/login-action@v3',
                            'with': {
                                'registry': '${{ env.REGISTRY }}',
                                'username': '${{ github.actor }}',
                                'password': '${{ secrets.GITHUB_TOKEN }}'
                            }
                        },
                        {
                            'name': 'Extract metadata',
                            'id': 'meta',
                            'uses': 'docker/metadata-action@v5',
                            'with': {
                                'images': '${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}',
                                'tags': '\n'.join([
                                    'type=ref,event=branch',
                                    'type=ref,event=pr',
                                    'type=sha,prefix={{branch}}-',
                                    'type=raw,value=latest,enable={{is_default_branch}}'
                                ])
                            }
                        },
                        {
                            'name': 'Build and push Docker image',
                            'uses': 'docker/build-push-action@v5',
                            'with': {
                                'context': '.',
                                'push': True,
                                'tags': '${{ steps.meta.outputs.tags }}',
                                'labels': '${{ steps.meta.outputs.labels }}',
                                'cache-from': 'type=gha',
                                'cache-to': 'type=gha,mode=max'
                            }
                        }
                    ]
                },
                'deploy': {
                    'runs-on': 'ubuntu-latest',
                    'needs': 'build-and-push',
                    'environment': deployment_env,
                    'steps': [
                        {
                            'name': 'Checkout code',
                            'uses': 'actions/checkout@v4'
                        }
                    ]
                }
            }
        }
        
        # 根据部署目标添加不同的部署步骤
        if k8s_cluster:
            workflow['jobs']['deploy']['steps'].extend([
                {
                    'name': 'Set up kubectl',
                    'uses': 'azure/setup-kubectl@v3',
                    'with': {
                        'version': 'latest'
                    }
                },
                {
                    'name': 'Configure kubectl',
                    'run': '\n'.join([
                        'echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig',
                        'export KUBECONFIG=kubeconfig'
                    ])
                },
                {
                    'name': 'Deploy to Kubernetes',
                    'run': '\n'.join([
                        'kubectl set image deployment/app app=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}',
                        'kubectl rollout status deployment/app',
                        'kubectl get services -o wide'
                    ])
                }
            ])
        else:
            # Docker Compose部署
            workflow['jobs']['deploy']['steps'].extend([
                {
                    'name': 'Deploy to server',
                    'uses': 'appleboy/ssh-action@v1.0.0',
                    'with': {
                        'host': '${{ secrets.HOST }}',
                        'username': '${{ secrets.USERNAME }}',
                        'key': '${{ secrets.SSH_KEY }}',
                        'script': '\n'.join([
                            'cd /app',
                            'docker-compose pull',
                            'docker-compose up -d',
                            'docker system prune -f'
                        ])
                    }
                }
            ])
        
        # 添加部署后验证
        workflow['jobs']['deploy']['steps'].extend([
            {
                'name': 'Health check',
                'run': '\n'.join([
                    'sleep 30',
                    'curl -f ${{ secrets.APP_URL }}/health || exit 1'
                ])
            },
            {
                'name': 'Notify deployment',
                'if': 'always()',
                'uses': 'actions/github-script@v7',
                'with': {
                    'script': '\n'.join([
                        'const status = "${{ job.status }}";',
                        'const message = status === "success" ? "✅ 部署成功" : "❌ 部署失败";',
                        'github.rest.repos.createCommitComment({',
                        '  owner: context.repo.owner,',
                        '  repo: context.repo.repo,',
                        '  commit_sha: context.sha,',
                        '  body: `${message} - ${new Date().toISOString()}`',
                        '});'
                    ])
                }
            }
        ])
        
        workflow_content = yaml.dump(workflow, default_flow_style=False, sort_keys=False)
        
        cd_path = self.workflows_dir / "cd.yml"
        with open(cd_path, 'w', encoding='utf-8') as f:
            f.write(workflow_content)
        
        print(f"✅ CD工作流已生成: {cd_path}")
        return workflow_content
    
    def generate_release_workflow(self) -> str:
        """
        生成发布工作流
        
        Returns:
            str: 发布工作流内容
        """
        workflow = {
            'name': 'Release',
            'on': {
                'push': {
                    'tags': ['v*']
                }
            },
            'jobs': {
                'release': {
                    'runs-on': 'ubuntu-latest',
                    'permissions': {
                        'contents': 'write',
                        'packages': 'write'
                    },
                    'steps': [
                        {
                            'name': 'Checkout code',
                            'uses': 'actions/checkout@v4',
                            'with': {
                                'fetch-depth': 0
                            }
                        },
                        {
                            'name': 'Generate changelog',
                            'id': 'changelog',
                            'run': '\n'.join([
                                'PREVIOUS_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")',
                                'if [ -z "$PREVIOUS_TAG" ]; then',
                                '  CHANGELOG=$(git log --pretty=format:"- %s" --no-merges)',
                                'else',
                                '  CHANGELOG=$(git log $PREVIOUS_TAG..HEAD --pretty=format:"- %s" --no-merges)',
                                'fi',
                                'echo "changelog<<EOF" >> $GITHUB_OUTPUT',
                                'echo "$CHANGELOG" >> $GITHUB_OUTPUT',
                                'echo "EOF" >> $GITHUB_OUTPUT'
                            ])
                        },
                        {
                            'name': 'Create Release',
                            'uses': 'actions/create-release@v1',
                            'env': {
                                'GITHUB_TOKEN': '${{ secrets.GITHUB_TOKEN }}'
                            },
                            'with': {
                                'tag_name': '${{ github.ref }}',
                                'release_name': 'Release ${{ github.ref }}',
                                'body': '\n'.join([
                                    '## 🚀 新版本发布',
                                    '',
                                    '### 📝 更新日志',
                                    '${{ steps.changelog.outputs.changelog }}',
                                    '',
                                    '### 📦 部署说明',
                                    '1. 拉取最新镜像: `docker pull ghcr.io/${{ github.repository }}:${{ github.ref_name }}`',
                                    '2. 更新部署配置',
                                    '3. 重启服务',
                                    '',
                                    '### 🔗 相关链接',
                                    '- [文档](https://github.com/${{ github.repository }}/wiki)',
                                    '- [问题反馈](https://github.com/${{ github.repository }}/issues)'
                                ]),
                                'draft': False,
                                'prerelease': False
                            }
                        },
                        {
                            'name': 'Build and push release image',
                            'uses': 'docker/build-push-action@v5',
                            'with': {
                                'context': '.',
                                'push': True,
                                'tags': '\n'.join([
                                    'ghcr.io/${{ github.repository }}:${{ github.ref_name }}',
                                    'ghcr.io/${{ github.repository }}:latest'
                                ])
                            }
                        }
                    ]
                }
            }
        }
        
        workflow_content = yaml.dump(workflow, default_flow_style=False, sort_keys=False)
        
        release_path = self.workflows_dir / "release.yml"
        with open(release_path, 'w', encoding='utf-8') as f:
            f.write(workflow_content)
        
        print(f"✅ 发布工作流已生成: {release_path}")
        return workflow_content
    
    def generate_dependabot_config(self) -> str:
        """
        生成Dependabot配置
        
        Returns:
            str: Dependabot配置内容
        """
        config = {
            'version': 2,
            'updates': [
                {
                    'package-ecosystem': 'pip',
                    'directory': '/',
                    'schedule': {
                        'interval': 'weekly',
                        'day': 'monday',
                        'time': '09:00'
                    },
                    'open-pull-requests-limit': 5,
                    'reviewers': ['@' + self.repo_name.split('/')[0]],
                    'commit-message': {
                        'prefix': 'deps',
                        'include': 'scope'
                    }
                },
                {
                    'package-ecosystem': 'docker',
                    'directory': '/',
                    'schedule': {
                        'interval': 'weekly'
                    }
                },
                {
                    'package-ecosystem': 'github-actions',
                    'directory': '/',
                    'schedule': {
                        'interval': 'weekly'
                    }
                }
            ]
        }
        
        config_content = yaml.dump(config, default_flow_style=False, sort_keys=False)
        
        dependabot_dir = Path(".github")
        dependabot_dir.mkdir(exist_ok=True)
        dependabot_path = dependabot_dir / "dependabot.yml"
        
        with open(dependabot_path, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print(f"✅ Dependabot配置已生成: {dependabot_path}")
        return config_content
    
    def generate_all_workflows(self, 
                             python_versions: List[str] = None,
                             deployment_env: str = "production",
                             k8s_cluster: Optional[str] = None):
        """
        生成所有工作流文件
        
        Args:
            python_versions: Python版本列表
            deployment_env: 部署环境
            k8s_cluster: Kubernetes集群名称
        """
        print(f"🚀 开始为项目 '{self.project_name}' 生成CI/CD管道...")
        print(f"仓库: {self.repo_name}, 环境: {deployment_env}")
        print("-" * 60)
        
        # 生成所有工作流
        self.generate_ci_workflow(python_versions=python_versions)
        self.generate_cd_workflow(deployment_env=deployment_env, k8s_cluster=k8s_cluster)
        self.generate_release_workflow()
        self.generate_dependabot_config()
        
        # 生成配置文件
        self._generate_github_templates()
        self._generate_codecov_config()
        
        print("-" * 60)
        print(f"✅ 所有CI/CD配置已生成到目录: .github/")
        print("\n📋 下一步操作:")
        print("1. 提交配置文件到GitHub仓库")
        print("2. 在仓库设置中配置Secrets")
        print("3. 启用GitHub Actions")
        print("4. 配置部署环境保护规则")
    
    def _generate_github_templates(self):
        """生成GitHub模板文件"""
        # Issue模板
        issue_template_dir = Path(".github/ISSUE_TEMPLATE")
        issue_template_dir.mkdir(parents=True, exist_ok=True)
        
        bug_template = """---
name: Bug报告
about: 创建一个Bug报告来帮助我们改进
title: '[BUG] '
labels: 'bug'
assignees: ''

---

**Bug描述**
简洁明了地描述这个Bug。

**复现步骤**
复现该行为的步骤：
1. 进入 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

**期望行为**
简洁明了地描述你期望发生的事情。

**截图**
如果适用，添加截图来帮助解释你的问题。

**环境信息：**
 - 操作系统: [例如 iOS]
 - 浏览器 [例如 chrome, safari]
 - 版本 [例如 22]

**附加信息**
在此添加关于问题的任何其他信息。
"""
        
        with open(issue_template_dir / "bug_report.md", 'w', encoding='utf-8') as f:
            f.write(bug_template)
        
        # PR模板
        pr_template = """## 📝 变更描述

简要描述此PR的变更内容。

## 🔧 变更类型

- [ ] Bug修复
- [ ] 新功能
- [ ] 重构
- [ ] 文档更新
- [ ] 性能优化
- [ ] 其他

## ✅ 测试

- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动测试完成
- [ ] 代码覆盖率满足要求

## 📋 检查清单

- [ ] 代码遵循项目规范
- [ ] 自我审查了代码
- [ ] 添加了必要的注释
- [ ] 更新了相关文档
- [ ] 没有引入新的警告

## 🔗 相关Issue

关闭 #(issue编号)

## 📸 截图（如适用）

## 📝 额外说明

"""
        
        github_dir = Path(".github")
        with open(github_dir / "pull_request_template.md", 'w', encoding='utf-8') as f:
            f.write(pr_template)
        
        print("✅ GitHub模板文件已生成")
    
    def _generate_codecov_config(self):
        """生成Codecov配置"""
        codecov_config = {
            'coverage': {
                'status': {
                    'project': {
                        'default': {
                            'target': '80%',
                            'threshold': '1%'
                        }
                    },
                    'patch': {
                        'default': {
                            'target': '70%'
                        }
                    }
                }
            },
            'comment': {
                'layout': 'reach,diff,flags,tree',
                'behavior': 'default',
                'require_changes': False
            }
        }
        
        codecov_content = yaml.dump(codecov_config, default_flow_style=False)
        
        with open("codecov.yml", 'w', encoding='utf-8') as f:
            f.write(codecov_content)
        
        print("✅ Codecov配置已生成: codecov.yml")


class DeploymentMonitor:
    """
    部署监控器
    
    监控部署状态和应用健康状况
    """
    
    def __init__(self, app_url: str, webhook_url: Optional[str] = None):
        self.app_url = app_url
        self.webhook_url = webhook_url
    
    def check_health(self) -> Dict:
        """
        检查应用健康状态
        
        Returns:
            Dict: 健康检查结果
        """
        try:
            response = requests.get(f"{self.app_url}/health", timeout=10)
            
            result = {
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'timestamp': datetime.now().isoformat(),
                'details': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
            }
            
            print(f"🏥 健康检查: {result['status']} (响应时间: {result['response_time']:.2f}s)")
            return result
            
        except requests.RequestException as e:
            result = {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            print(f"❌ 健康检查失败: {e}")
            return result
    
    def check_deployment_status(self, deployment_id: str) -> Dict:
        """
        检查部署状态
        
        Args:
            deployment_id: 部署ID
        
        Returns:
            Dict: 部署状态
        """
        # 模拟部署状态检查
        import random
        import time
        
        statuses = ['pending', 'in_progress', 'success', 'failed']
        
        # 模拟部署过程
        for i, status in enumerate(['pending', 'in_progress']):
            print(f"📦 部署状态: {status}")
            time.sleep(2)  # 模拟等待时间
        
        # 随机决定最终状态
        final_status = random.choice(['success', 'failed'])
        
        result = {
            'deployment_id': deployment_id,
            'status': final_status,
            'timestamp': datetime.now().isoformat(),
            'duration': '2m 30s'
        }
        
        if final_status == 'success':
            print(f"✅ 部署成功: {deployment_id}")
            # 部署成功后进行健康检查
            health_result = self.check_health()
            result['health_check'] = health_result
        else:
            print(f"❌ 部署失败: {deployment_id}")
            result['error'] = "部署过程中发生错误"
        
        # 发送通知
        if self.webhook_url:
            self._send_notification(result)
        
        return result
    
    def _send_notification(self, result: Dict):
        """
        发送部署通知
        
        Args:
            result: 部署结果
        """
        try:
            status_emoji = "✅" if result['status'] == 'success' else "❌"
            message = f"{status_emoji} 部署{result['status']}: {result['deployment_id']}"
            
            payload = {
                'text': message,
                'attachments': [{
                    'color': 'good' if result['status'] == 'success' else 'danger',
                    'fields': [
                        {'title': '部署ID', 'value': result['deployment_id'], 'short': True},
                        {'title': '状态', 'value': result['status'], 'short': True},
                        {'title': '时间', 'value': result['timestamp'], 'short': True}
                    ]
                }]
            }
            
            # 模拟发送通知
            print(f"📢 发送通知: {message}")
            
        except Exception as e:
            print(f"⚠️ 通知发送失败: {e}")


def main():
    """
    主函数：演示CI/CD管道生成器的使用
    """
    print("Session30 示例2: CI/CD自动化部署管道")
    print("=" * 60)
    
    # 创建CI/CD管道生成器
    pipeline = CICDPipelineGenerator(
        project_name="my-web-app",
        repo_name="username/my-web-app"
    )
    
    # 生成所有工作流
    pipeline.generate_all_workflows(
        python_versions=["3.9", "3.10", "3.11"],
        deployment_env="production",
        k8s_cluster=None  # 使用Docker Compose部署
    )
    
    print("\n" + "=" * 60)
    print("🔍 演示部署监控")
    
    # 创建部署监控器
    monitor = DeploymentMonitor(
        app_url="http://localhost:8000",
        webhook_url="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
    )
    
    # 模拟部署监控
    deployment_id = f"deploy-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    deployment_result = monitor.check_deployment_status(deployment_id)
    
    print("\n📊 部署结果:")
    print(json.dumps(deployment_result, indent=2, ensure_ascii=False))
    
    print("\n📚 CI/CD最佳实践:")
    print("1. 🔄 自动化测试：确保代码质量")
    print("2. 🛡️ 安全扫描：检查漏洞和依赖")
    print("3. 📦 容器化：统一部署环境")
    print("4. 🚀 渐进式部署：降低风险")
    print("5. 📈 监控告警：及时发现问题")
    print("6. 🔙 快速回滚：故障恢复")
    
    print("\n🔧 配置说明:")
    print("- ci.yml: 持续集成工作流")
    print("- cd.yml: 持续部署工作流")
    print("- release.yml: 版本发布工作流")
    print("- dependabot.yml: 依赖更新配置")
    print("- codecov.yml: 代码覆盖率配置")
    print("- GitHub模板: Issue和PR模板")


if __name__ == "__main__":
    main()