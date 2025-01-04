from ClassWidgets.base import (PluginBase, SettingsBase, PluginConfig)  # 导入CW的基类

WIDGET_CODE = 'cw-swtdents-on-duty.ui' # 插件代号
WIDGET_NAME = '值日生组件'  # 您的插件显示的名称
WIDGET_WIDTH = 245

class Plugin(PluginBase):  # 插件类
    def __init__(self, cw_contexts, method):  # 初始化
        super().__init__(cw_contexts, method)  # 调用父类初始化方法
        self.method.register_widget(WIDGET_CODE, WIDGET_NAME, WIDGET_WIDTH)

    def execute(self):  # 自启动执行部分
        """
        当 Class Widgets启动时，将会执行此部分的代码
        """
        self.your_plugin = self.method.get_widget(WIDGET_CODE)  # 获取小组件对象

    def update(self, cw_contexts):  # 自动更新部分（每秒更新）
        super().update(cw_contexts)  # 获取最新接口
        if State(0):
            pass


class Settings(SettingsBase):  # 设置类
    def __init__(self, plugin_path, parent=None):  # 初始化
        super().__init__(plugin_path, parent)
        """
        在这里写设置页面
        """
    # 其他代码……