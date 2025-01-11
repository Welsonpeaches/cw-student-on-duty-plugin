from .ClassWidgets.base import PluginBase, SettingsBase, PluginConfig  # 导入CW的基类

from PyQt5 import uic
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QScrollArea, QWidget, QVBoxLayout, QScrollBar
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal
from loguru import logger
import os
import csv
from datetime import datetime, timedelta
from PyQt5 import uic
from loguru import logger
from datetime import datetime
from .ClassWidgets.base import PluginBase, SettingsBase, PluginConfig  # 导入CW的基类

from PyQt5.QtWidgets import QHBoxLayout
from qfluentwidgets import ImageLabel, LineEdit

import json
from datetime import datetime, timedelta


WIDGET_CODE = 'cw-swtdents-on-duty.ui'  # 插件代号
WIDGET_NAME = '值日生组件'  # 您的插件显示的名称
WIDGET_WIDTH = 500




class Plugin(PluginBase):  # 插件类
    def __init__(self, cw_contexts, method):  # 初始化
        super().__init__(cw_contexts, method)  # 调用父类初始化方法

        self.method.register_widget(WIDGET_CODE, WIDGET_NAME, WIDGET_WIDTH)  # 注册小组件到CW
        self.cfg = PluginConfig(self.PATH, 'config.json')# 实例化配置类
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.json_file_path = os.path.join(self.script_dir, "duty.json")



    def execute(self):  # 自启动执行部分
        # 小组件自定义（照PyQt的方法正常写）
        self.students_on_duty_widget = self.method.get_widget(WIDGET_CODE)  # 获取小组件对象

        if self.students_on_duty_widget:  # 判断小组件是否存在
            contentLayout = self.students_on_duty_widget.findChild(QHBoxLayout, 'contentLayout')  # 标题布局
            contentLayout.setSpacing(1)  # 设置间距

            self.testimg = ImageLabel(f'{self.PATH}/img/favicon.png')  # 自定义图片
            self.testimg.setFixedSize(36, 30)

            contentLayout.addWidget(self.testimg)  # 添加图片到布局

        logger.success('值日生插件加载成功！本插件开发者：月下的桃子')
        logger.success('我喜欢你')


    def load_data_from_json(self,file_path):
        with open(file_path, 'r') as file:
            self.data_dict = json.load(file)
        return self.data_dict['start_date'], self.data_dict['data']

    def get_current_day_index(self,start_date_str):
        self.start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        self.current_date = datetime.now()
        self.delta_days = (self.current_date - self.start_date).days
        return self.delta_days % len(self.data_dict['data'])


    def update(self, cw_contexts):  # 自动更新部分
        super().update(cw_contexts)  # 调用父类更新方法
        self.cfg.update_config()  # 更新配置

        self.duty = self.load_data_from_json(self.json_file_path)
        self.start_date_str = '2024-09-01'
        self.current_day_index = self.get_current_day_index(self.start_date_str)
        data = self.data_dict['data']
        self.today_duty_list = data[self.current_day_index]
        self.today_duty_list2 = []

        for i in self.today_duty_list:

            self.today_duty_list2.append(i)
            

        duty_1 = self.today_duty_list2[0]
        duty_2 = self.today_duty_list2[1]
        duty_3 = self.today_duty_list2[2]
        duty_4 = self.today_duty_list2[3]

        if hasattr(self, 'students_on_duty_widget'):  # 判断小组件是否存在
            widget_title = f'今天的值日生'  # 标题内容
            self.method.change_widget_content(WIDGET_CODE, widget_title, f'{duty_1},{duty_2},{duty_3},{duty_4}')






class Settings(SettingsBase):  # 设置类
    def __init__(self, plugin_path, parent=None):  # 初始化
        super().__init__(plugin_path, parent)
        """
        在这里写设置页面
        """
    # 其他代码……
