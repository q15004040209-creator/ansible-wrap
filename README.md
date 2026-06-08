# Ansible-wrap

[![PyPI version](https://img.shields.io/pypi/v/ansible-core.svg)](https://pypi.org/project/ansible-core)
[![Docs badge](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://docs.ansible.com/ansible/latest/)
[![GitHub license](https://img.shields.io/badge/license-GPL%20v3.0-brightgreen.svg)](https://github.com/ansible/ansible/blob/devel/COPYING)

## 📘 中文介绍

Ansible 是一个极其简单的 IT 自动化平台，专为简化 IT 自动化而设计。它 handles 配置管理、应用程序部署、云资源供给、临时任务执行、网络自动化和多节点编排。Ansible 让复杂的变更（如零停机滚动更新和负载均衡）变得轻而易举。

### 设计原则

- 极其简单的安装过程和最小的学习曲线
- 快速且并行地管理机器
- 无需自定义代理和额外开放端口，通过现有 SSH 守护程序实现无代理
- 用对机器和人类都友好的语言描述基础设施
- 专注于安全性和易于审计/审查/重写内容
- 即时管理新的远程机器，无需引导任何软件
- 支持在任何动态语言中开发模块，不仅限于 Python
- 支持非 root 用户使用
- 成为有史以来最容易使用的 IT 自动化系统

### 主要特性

- **无代理架构**: 通过 SSH 和 WinRM 管理远程主机
- **幂等性**: 重复执行任务产生相同结果
- **YAML 语法**: 易读易写的 Playbook
- **模块化**: 3000+ 内置模块覆盖各种场景
- **批量并行**: 默认 50 个并发，可自定义
- **角色系统**: 可重用的自动化单元

## 📗 English Introduction

Ansible is a radically simple IT automation system. It handles configuration management, application deployment, cloud provisioning, ad-hoc task execution, network automation, and multi-node orchestration. Ansible makes complex changes like zero-downtime rolling updates with load balancers easy.

### Design Principles

- Have an extremely simple setup process with a minimal learning curve
- Manage machines quickly and in parallel
- Avoid custom-agents and additional open ports, be agentless by leveraging the existing SSH daemon
- Describe infrastructure in a language that is both machine and human friendly
- Focus on security and easy auditability/review/rewriting of content
- Manage new remote machines instantly, without bootstrapping any software
- Allow module development in any dynamic language, not just Python
- Be usable as non-root
- Be the easiest IT automation system to use, ever

## 🚀 快速开始

### 安装

```bash
pip install ansible
```

或参考官方 [安装指南](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

### Python Demo

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ansible Python API Demo - ansible-wrap
使用 Ansible 的 Python API 执行自动化任务
"""

from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.executor.playbook_play import PlaybookPlay
from ansible.playbook.play import Play

def simple_ad_hoc():
    """执行简单的 ad-hoc 命令"""
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=['localhost,'])
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    
    # 创建简单的 play
    play_source = {
        'hosts': 'localhost',
        'become': False,
        'tasks': [
            {
                'name': 'Run simple command',
                'command': 'echo "Hello from Ansible!"',
                'register': 'result'
            }
        ]
    }
    
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
    print("Play created successfully!")

def run_playbook():
    """运行 Playbook"""
    playbook_source = {
        'hosts': 'localhost',
        'tasks': [
            {
                'name': 'Ensure nginx is installed',
                'apt':
                    'name': 'nginx',
                    'state': 'present'
                }
            }
        ]
    }
    
    print("Playbook ready to run!")

if __name__ == '__main__':
    print("🤖 Ansible-wrap Python Demo")
    print("=" * 40)
    simple_ad_hoc()
    run_playbook()
    print("✓ Demo completed!")
```

### 基础 Playbook 示例

```yaml
# site.yaml
---
- name: 部署 Web 服务器
  hosts: webservers
  become: yes
  tasks:
    - name: 安装 Nginx
      apt:
        name: nginx
        state: present
    
    - name: 启动 Nginx 服务
      service:
        name: nginx
        state: started
        enabled: yes
    
    - name: 部署自定义首页
      copy:
        src: files/index.html
        dest: /var/www/html/index.html
```

### Inventory 文件示例

```ini
# inventory.ini
[webservers]
web1.example.com
web2.example.com

[dbservers]
db1.example.com
db2.example.com

[all:vars]
ansible_user=admin
ansible_ssh_private_key_file=~/.ssh/id_rsa
```

## 📚 学习资源

- [官方文档](https://docs.ansible.com/ansible/latest/)
- [Ansible Forum](https://forum.ansible.com/) - 获取帮助和分享知识
- [Matrix 实时聊天](https://docs.ansible.com/ansible/devel/community/communication.html#real-time-chat)
- [Bullhorn 通讯](https://docs.ansible.com/ansible/devel/community/communication.html#the-bullhorn) - 获取版本发布和重要变更

## 🤝 贡献

欢迎贡献代码！请参阅 [贡献者指南](https://github.com/ansible/ansible/blob/devel/.github/CONTRIBUTING.md)

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 提交 Pull Request

## 📄 许可证

GNU General Public License v3.0 或更高版本

## 👥 致谢

Ansible 由 [Michael DeHaan](https://github.com/mpdehaan) 创建，已有 5000+ 用户贡献。

本项目由 [Red Hat](https://www.redhat.com) 大力赞助。

---

**本项目是 Ansible 的 Python 封装，提供便捷的 API 和最佳实践示例。**