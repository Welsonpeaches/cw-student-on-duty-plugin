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


WIDGET_CODE = 'cw-swtdents-on-duty.ui'  # 插件代号
WIDGET_NAME = '值日生组件'  # 您的插件显示的名称
WIDGET_WIDTH = 600




class Plugin(PluginBase):  # 插件类
    def __init__(self, cw_contexts, method):  # 初始化
        super().__init__(cw_contexts, method)  # 调用父类初始化方法

        self.method.register_widget(WIDGET_CODE, WIDGET_NAME, WIDGET_WIDTH)  # 注册小组件到CW
        self.cfg = PluginConfig(self.PATH, 'config.json')  # 实例化配置类


        self.file_path = "duty.txt"
        self.start_date = datetime.now().date()
        self.days = 30
        self.students = self.read_duty_schedule()
        self.schedule = self.assign_groups(self.students, self.start_date, self.days)

    def read_duty_schedule(self):
        students = []
        with open("D:\Welson\Class_Widgets_Plugins\Class-Widgets\plugins\Students_On_Duty\duty.txt", 'r', encoding='utf-8') as file:
            for i, line in enumerate(file.readlines()):
                if i >= 4:
                    break
                students.append(line.strip())

        return students

    def assign_groups(self, students, start_date, days):
        schedule = []
        student_count = len(students)
        index = 0

        current_date = start_date
        for _ in range(days):
            if current_date.day % 5 == 0:
                group_size = 2
            else:
                group_size = 1

            group = []
            for _ in range(group_size):
                group.append(students[index])
                index = (index + 1) % student_count

            schedule.append((current_date.strftime('%Y-%m-%d'), group))
            current_date += timedelta(days=1)

        return schedule

    def get_todays_duty(self, target_date):
        for date, group in self.schedule:
            if date == target_date.strftime('%Y-%m-%d'):
                return group
        return None

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

    def update(self, cw_contexts):  # 自动更新部分
        super().update(cw_contexts)  # 调用父类更新方法
        self.cfg.update_config()  # 更新配置

        start_date = datetime.now().date()  # 假设从今天开始安排
        days = 30  # 假设我们要安排一个月的日程表
        students = self.read_duty_schedule()
        schedule = self.assign_groups(students, start_date, days)

        # 获取今天的值日生
        today = datetime.now().date()
        today_duty = self.get_todays_duty(today)

        if hasattr(self, 'students_on_duty_widget'):  # 判断小组件是否存在
            widget_title = f'今天的值日生'  # 标题内容
            self.method.change_widget_content(WIDGET_CODE, widget_title, f'{today_duty}')





class Settings(SettingsBase):  # 设置类
    def __init__(self, plugin_path, parent=None):  # 初始化
        super().__init__(plugin_path, parent)
        """
        在这里写设置页面
        """
    # 其他代码……
