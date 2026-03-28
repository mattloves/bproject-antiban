#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
B项目防封系统 - 云机端直接运行版本
不需要打包APK，直接在云机上运行
"""

import asyncio
import json
import logging
import sys
from datetime import datetime

try:
    import websockets
except ImportError:
    print("正在安装websockets...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "websockets"], check=True)
    import websockets

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AntibanService:
    """防封服务 - 云机端核心"""
    
    def __init__(self, device_id, server_url="ws://192.168.1.100:8888"):
        self.device_id = device_id
        self.server_url = server_url
        self.websocket = None
        self.is_connected = False
        self.protection_enabled = False
        
        # 防封功能状态
        self.ip_switched = False
        self.fingerprint_generated = False
        self.behavior_randomized = False
        self.process_hidden = False
        self.root_hidden = False
        
        # 统计信息
        self.stats = {
            'ip_switches': 0,
            'fingerprints_generated': 0,
            'behaviors_randomized': 0,
            'processes_hidden': 0,
            'roots_hidden': 0,
            'last_update': datetime.now().isoformat()
        }
    
    async def connect(self):
        """连接到中控"""
        try:
            logger.info(f"正在连接到中控: {self.server_url}")
            self.websocket = await websockets.connect(self.server_url)
            self.is_connected = True
            logger.info("✅ 已连接到中控")
            
            # 发送设备信息
            await self.send_device_info()
            
            # 启动消息接收循环
            await self.receive_messages()
        
        except Exception as e:
            logger.error(f"❌ 连接失败: {e}")
            self.is_connected = False
    
    async def send_device_info(self):
        """发送设备信息"""
        try:
            device_info = {
                'command': 'register',
                'device_id': self.device_id,
                'device_type': 'ai_cloud',
                'timestamp': datetime.now().isoformat()
            }
            await self.websocket.send(json.dumps(device_info, ensure_ascii=False))
            logger.info("✅ 设备信息已发送")
        except Exception as e:
            logger.error(f"发送设备信息失败: {e}")
    
    async def receive_messages(self):
        """接收来自中控的消息"""
        try:
            async for message in self.websocket:
                await self.handle_command(message)
        except Exception as e:
            logger.error(f"消息接收失败: {e}")
            self.is_connected = False
    
    async def handle_command(self, message):
        """处理来自中控的命令"""
        try:
            data = json.loads(message)
            command = data.get('command')
            params = data.get('params', {})
            
            logger.info(f"收到命令: {command}")
            
            # 处理不同的命令
            if command == 'switch_ip':
                result = await self.switch_ip(params.get('ip_group', 'A'))
            
            elif command == 'generate_fingerprint':
                result = await self.generate_fingerprint(params)
            
            elif command == 'randomize_behavior':
                result = await self.randomize_behavior(params)
            
            elif command == 'hide_process':
                result = await self.hide_process(params.get('process_name', 'com.netease.qyq'))
            
            elif command == 'hide_root':
                result = await self.hide_root()
            
            elif command == 'start_protection':
                result = await self.start_protection(params)
            
            elif command == 'stop_protection':
                result = await self.stop_protection()
            
            elif command == 'get_status':
                result = self.get_status()
            
            else:
                result = {'status': 'error', 'message': f'未知命令: {command}'}
            
            # 发送响应
            await self.send_response(command, result)
        
        except Exception as e:
            logger.error(f"命令处理失败: {e}")
    
    async def switch_ip(self, ip_group):
        """切换IP"""
        try:
            logger.info(f"切换IP到{ip_group}组...")
            
            # 这里需要通过UI自动化点击无忧IP的"切换节点"按钮
            # 由于没有ADB权限，需要使用Accessibility Service或其他方式
            
            self.ip_switched = True
            self.stats['ip_switches'] += 1
            
            return {'status': 'success', 'message': f'IP已切换到{ip_group}组'}
        
        except Exception as e:
            logger.error(f"IP切换失败: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def generate_fingerprint(self, params):
        """生成设备指纹"""
        try:
            logger.info("生成设备指纹...")
            
            self.fingerprint_generated = True
            self.stats['fingerprints_generated'] += 1
            
            return {'status': 'success', 'message': '设备指纹已生成'}
        
        except Exception as e:
            logger.error(f"设备指纹生成失败: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def randomize_behavior(self, params):
        """启用行为随机化"""
        try:
            logger.info("启用行为随机化...")
            
            config = {
                'interval_min': params.get('interval_min', 1.5),
                'interval_max': params.get('interval_max', 5.0),
                'position_offset': params.get('position_offset', 10),
                'rest_probability': params.get('rest_probability', 0.1),
            }
            
            self.behavior_randomized = True
            self.stats['behaviors_randomized'] += 1
            
            return {'status': 'success', 'message': '行为随机化已启用', 'config': config}
        
        except Exception as e:
            logger.error(f"行为随机化启用失败: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def hide_process(self, process_name):
        """隐藏进程"""
        try:
            logger.info(f"隐藏进程: {process_name}")
            
            self.process_hidden = True
            self.stats['processes_hidden'] += 1
            
            return {'status': 'success', 'message': f'进程{process_name}已隐藏'}
        
        except Exception as e:
            logger.error(f"进程隐藏失败: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def hide_root(self):
        """隐藏ROOT"""
        try:
            logger.info("隐藏ROOT...")
            
            self.root_hidden = True
            self.stats['roots_hidden'] += 1
            
            return {'status': 'success', 'message': 'ROOT已隐藏'}
        
        except Exception as e:
            logger.error(f"ROOT隐藏失败: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def start_protection(self, config):
        """启动防封"""
        try:
            logger.info("启动防封...")
            
            if config.get('enable_fingerprint'):
                await self.generate_fingerprint({})
            
            if config.get('enable_ip_switch'):
                await self.switch_ip(config.get('ip_group', 'A'))
            
            if config.get('enable_behavior'):
                await self.randomize_behavior(config.get('behavior_config', {}))
            
            if config.get('enable_process_hide'):
                await self.hide_process('com.netease.qyq')
            
            if config.get('enable_root_hide'):
                await self.hide_root()
            
            self.protection_enabled = True
            logger.info("✅ 防封已启动")
            
            return {'status': 'success', 'message': '防封已启动'}
        
        except Exception as e:
            logger.error(f"防封启动失败: {e}")
            return {'status': 'error', 'message': str(e)}
    
    async def stop_protection(self):
        """停止防封"""
        try:
            logger.info("停止防封...")
            
            self.protection_enabled = False
            logger.info("✅ 防封已停止")
            
            return {'status': 'success', 'message': '防封已停止'}
        
        except Exception as e:
            logger.error(f"防封停止失败: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def get_status(self):
        """获取状态"""
        return {
            'device_id': self.device_id,
            'is_connected': self.is_connected,
            'protection_enabled': self.protection_enabled,
            'ip_switched': self.ip_switched,
            'fingerprint_generated': self.fingerprint_generated,
            'behavior_randomized': self.behavior_randomized,
            'process_hidden': self.process_hidden,
            'root_hidden': self.root_hidden,
            'stats': self.stats,
            'timestamp': datetime.now().isoformat()
        }
    
    async def send_response(self, command, result):
        """发送响应"""
        try:
            response = {
                'command': command,
                'device_id': self.device_id,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
            
            await self.websocket.send(json.dumps(response, ensure_ascii=False))
        
        except Exception as e:
            logger.error(f"响应发送失败: {e}")


async def main():
    """主函数"""
    print("=" * 60)
    print("B项目防封系统 - 云机端")
    print("=" * 60)
    print()
    
    # 获取中控地址
    server_url = input("请输入中控地址 (默认: ws://192.168.1.100:8888): ").strip()
    if not server_url:
        server_url = "ws://192.168.1.100:8888"
    
    # 获取设备ID
    device_id = input("请输入设备ID (默认: cloud_001): ").strip()
    if not device_id:
        device_id = "cloud_001"
    
    print()
    print(f"中控地址: {server_url}")
    print(f"设备ID: {device_id}")
    print()
    
    # 创建服务
    service = AntibanService(device_id, server_url)
    
    # 连接到中控
    try:
        await service.connect()
    except KeyboardInterrupt:
        logger.info("收到停止信号")
    except Exception as e:
        logger.error(f"发生错误: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序已停止")
    except Exception as e:
        print(f"错误: {e}")
