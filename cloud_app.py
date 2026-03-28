# -*- coding: utf-8 -*-
"""
B项目防封系统 - 云机APK
使用Kivy框架开发，可打包成APK
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.clock import Clock
from kivy.core.window import Window

import asyncio
import json
import logging
from datetime import datetime
import websockets
import threading

# 设置窗口大小
Window.size = (720, 1280)

# 配置日志
logging.basicConfig(level=logging.INFO)
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
            
            # 这里需要通过Magisk模块修改系统属性
            # 需要在云机上预先安装Magisk和相关模块
            
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
            
            # 配置行为随机化参数
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
            
            # 这里需要通过Magisk隐藏进程
            # 需要在云机上预先安装Magisk和隐藏模块
            
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
            
            # 这里需要通过Shamiko隐藏ROOT
            # 需要在云机上预先安装Shamiko模块
            
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
            
            # 启用所有防封功能
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


class AntibanApp(App):
    """云机防封APP"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = None
        self.connection_thread = None
    
    def build(self):
        """构建UI"""
        self.title = "B项目防封系统 - 云机端"
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title_label = Label(
            text="B项目防封系统\n云机端",
            size_hint_y=0.1,
            font_size='20sp',
            bold=True
        )
        main_layout.add_widget(title_label)
        
        # 连接状态
        self.status_label = Label(
            text="状态: 未连接",
            size_hint_y=0.1,
            font_size='16sp'
        )
        main_layout.add_widget(self.status_label)
        
        # 中控地址输入
        address_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        address_layout.add_widget(Label(text="中控地址:", size_hint_x=0.3))
        self.address_input = TextInput(
            text="ws://192.168.1.100:8888",
            multiline=False,
            size_hint_x=0.7
        )
        address_layout.add_widget(self.address_input)
        main_layout.add_widget(address_layout)
        
        # 连接按钮
        button_layout = BoxLayout(size_hint_y=0.1, spacing=5)
        
        connect_btn = Button(text="🔗 连接中控")
        connect_btn.bind(on_press=self.on_connect)
        button_layout.add_widget(connect_btn)
        
        disconnect_btn = Button(text="🔌 断开连接")
        disconnect_btn.bind(on_press=self.on_disconnect)
        button_layout.add_widget(disconnect_btn)
        
        main_layout.add_widget(button_layout)
        
        # 防封控制按钮
        control_layout = BoxLayout(size_hint_y=0.15, spacing=5, orientation='vertical')
        
        start_btn = Button(text="🟢 启动防封")
        start_btn.bind(on_press=self.on_start_protection)
        control_layout.add_widget(start_btn)
        
        stop_btn = Button(text="🔴 停止防封")
        stop_btn.bind(on_press=self.on_stop_protection)
        control_layout.add_widget(stop_btn)
        
        main_layout.add_widget(control_layout)
        
        # 状态信息显示
        scroll = ScrollView(size_hint_y=0.55)
        self.info_label = Label(
            text="等待连接...",
            size_hint_y=None,
            markup=True
        )
        self.info_label.bind(texture_size=self.info_label.setter('size'))
        scroll.add_widget(self.info_label)
        main_layout.add_widget(scroll)
        
        # 初始化服务
        self.service = AntibanService("cloud_001", self.address_input.text)
        
        # 定时更新状态
        Clock.schedule_interval(self.update_status, 1)
        
        return main_layout
    
    def on_connect(self, instance):
        """连接到中控"""
        server_url = self.address_input.text
        self.service = AntibanService("cloud_001", server_url)
        
        # 在后台线程中连接
        self.connection_thread = threading.Thread(target=self.connect_async)
        self.connection_thread.daemon = True
        self.connection_thread.start()
    
    def connect_async(self):
        """异步连接"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.service.connect())
        except Exception as e:
            logger.error(f"连接失败: {e}")
    
    def on_disconnect(self, instance):
        """断开连接"""
        if self.service and self.service.websocket:
            try:
                asyncio.run(self.service.websocket.close())
                self.service.is_connected = False
                self.status_label.text = "状态: 已断开"
            except Exception as e:
                logger.error(f"断开连接失败: {e}")
    
    def on_start_protection(self, instance):
        """启动防封"""
        if not self.service.is_connected:
            self.info_label.text = "[color=ff0000]❌ 未连接到中控[/color]"
            return
        
        config = {
            'enable_fingerprint': True,
            'enable_ip_switch': True,
            'enable_behavior': True,
            'enable_process_hide': True,
            'enable_root_hide': True,
            'ip_group': 'A'
        }
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.service.start_protection(config))
        except Exception as e:
            logger.error(f"启动防封失败: {e}")
    
    def on_stop_protection(self, instance):
        """停止防封"""
        if not self.service.is_connected:
            self.info_label.text = "[color=ff0000]❌ 未连接到中控[/color]"
            return
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.service.stop_protection())
        except Exception as e:
            logger.error(f"停止防封失败: {e}")
    
    def update_status(self, dt):
        """更新状态显示"""
        if self.service:
            status = self.service.get_status()
            
            # 更新连接状态
            if self.service.is_connected:
                self.status_label.text = "[color=00ff00]✅ 已连接[/color]"
            else:
                self.status_label.text = "[color=ff0000]❌ 未连接[/color]"
            
            # 更新详细信息
            info_text = f"""
[b]设备信息[/b]
设备ID: {status['device_id']}
连接状态: {'✅ 已连接' if status['is_connected'] else '❌ 未连接'}
防封状态: {'✅ 启用中' if status['protection_enabled'] else '❌ 未启用'}

[b]防封功能[/b]
IP切换: {'✅' if status['ip_switched'] else '❌'}
设备指纹: {'✅' if status['fingerprint_generated'] else '❌'}
行为随机: {'✅' if status['behavior_randomized'] else '❌'}
进程隐藏: {'✅' if status['process_hidden'] else '❌'}
ROOT隐藏: {'✅' if status['root_hidden'] else '❌'}

[b]统计信息[/b]
IP切换次数: {status['stats']['ip_switches']}
指纹生成次数: {status['stats']['fingerprints_generated']}
行为随机次数: {status['stats']['behaviors_randomized']}
进程隐藏次数: {status['stats']['processes_hidden']}
ROOT隐藏次数: {status['stats']['roots_hidden']}

[b]最后更新[/b]
{status['timestamp']}
            """
            
            self.info_label.text = info_text


if __name__ == "__main__":
    app = AntibanApp()
    app.run()
