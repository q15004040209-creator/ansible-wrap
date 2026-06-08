#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ansible Python API Demo - ansible-wrap
使用 Ansible 的 Python API 执行自动化任务
"""

import json
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.executor.playbook_play import PlaybookPlay
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackDefault
from ansible.executor.task_queue_manager import TaskQueueManager


class ResultCallback(CallbackDefault):
    """自定义回调类，用于处理任务执行结果"""
    
    def __init__(self):
        super().__init__()
        self.results = []
    
    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        self.results.append({
            'host': host.name,
            'status': 'ok',
            'result': result._result
        })
        print(f"✓ [{host.name}] Task completed: {result._task.name}")
    
    def v2_runner_on_failed(self, result, **kwargs):
        host = result._host
        self.results.append({
            'host': host.name,
            'status': 'failed',
            'result': result._result
        })
        print(f"✗ [{host.name}] Task failed: {result._result.get('msg', 'Unknown error')}")
    
    def v2_runner_on_unreachable(self, result, **kwargs):
        host = result._host
        print(f"✗ [{host.name}] Host unreachable")


def ad_hoc_command(hosts='localhost', module='command', args='whoami'):
    """
    执行 Ad-hoc 命令
    
    Args:
        hosts: 目标主机（逗号分隔）
        module: Ansible 模块名
        args: 模块参数
    
    Returns:
        dict: 执行结果
    """
    print(f"\n🚀 执行 Ad-hoc 命令：{module} {args}")
    print("=" * 50)
    
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=[f'{hosts},'])
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    
    play_source = {
        'hosts': hosts,
        'gather_facts': False,
        'tasks': [
            {
                'name': f'Run {module}',
                module: args,
                'register': 'result'
            }
        ]
    }
    
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
    
    callback = ResultCallback()
    tqm = None
    
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            passwords={},
            stdout_callback=callback,
        )
        result = tqm.run(play)
        return result == 0
    finally:
        if tqm:
            tqm.cleanup()


def run_playbook_from_file(playbook_path, inventory_path='localhost,'):
    """
    从文件运行 Playbook
    
    Args:
        playbook_path: Playbook 文件路径
        inventory_path: Inventory 文件路径或主机列表
    
    Returns:
        bool: 执行是否成功
    """
    print(f"\n📋 运行 Playbook: {playbook_path}")
    print("=" * 50)
    
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=[inventory_path])
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    
    playbook = PlaybookPlay.load(playbook_path, variable_manager=variable_manager, loader=loader)
    
    callback = ResultCallback()
    tqm = None
    
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            passwords={},
            stdout_callback=callback,
        )
        result = tqm.run(playbook)
        return result == 0
    finally:
        if tqm:
            tqm.cleanup()


def create_dynamic_playbook(hosts='all', tasks=None):
    """
    动态创建并执行 Playbook
    
    Args:
        hosts: 目标主机
        tasks: 任务列表（dict 格式）
    
    Returns:
        bool: 执行是否成功
    """
    if tasks is None:
        tasks = [
            {
                'name': 'Ping hosts',
                'ping': {}
            },
            {
                'name': 'Gather system info',
                'setup': {
                    'filter': 'ansible_distribution*'
                }
            }
        ]
    
    print(f"\n🎯 动态创建 Playbook")
    print("=" * 50)
    
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=[f'{hosts},'])
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    
    play_source = {
        'hosts': hosts,
        'gather_facts': True,
        'tasks': tasks
    }
    
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
    
    callback = ResultCallback()
    tqm = None
    
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            passwords={},
            stdout_callback=callback,
        )
        result = tqm.run(play)
        return result == 0
    finally:
        if tqm:
            tqm.cleanup()


def demo_basic_tasks():
    """基础任务演示"""
    print("\n\n🤖 Ansible-wrap 基础演示")
    print("=" * 60)
    
    # 1. Ad-hoc 命令
    print("\n[1/3] 执行 Ad-hoc 命令...")
    success1 = ad_hoc_command('localhost', 'command', 'echo "Hello from Ansible!"')
    
    # 2. 检查系统信息
    print("\n[2/3] 收集系统信息...")
    success2 = ad_hoc_command('localhost', 'setup', 'filter=ansible_distribution*')
    
    # 3. 动态 Playbook
    print("\n[3/3] 执行动态 Playbook...")
    tasks = [
        {'name': 'Check uptime', 'command': 'uptime'},
        {'name': 'List processes', 'command': 'ps aux | head -5'}
    ]
    success3 = create_dynamic_playbook('localhost', tasks)
    
    print("\n" + "=" * 60)
    print(f"✓ 演示完成！成功：{sum([success1, success2, success3])}/3")
    return all([success1, success2, success3])


if __name__ == '__main__':
    import sys
    
    print("🚀 Ansible-wrap Python Demo")
    print("Ansible Python API 封装示例")
    print("=" * 60)
    
    # 检查 Ansible 是否已安装
    try:
        import ansible
        print(f"✓ Ansible 版本：{ansible.__version__}")
    except ImportError:
        print("✗ 错误：未找到 Ansible，请先安装：pip install ansible")
        sys.exit(1)
    
    # 运行演示
    success = demo_basic_tasks()
    
    if success:
        print("\n🎉 所有演示任务成功完成！")
        sys.exit(0)
    else:
        print("\n⚠️ 部分任务失败，请检查日志")
        sys.exit(1)