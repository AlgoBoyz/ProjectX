import enum
import os.path
import time
from turtledemo.chaos import coosys

try:
    from PySide6.QtCore import Qt, QTimer, QThread, Signal
    from PySide6.QtWidgets import *
    from PySide6.QtGui import QStandardItemModel, QStandardItem, QPen, QBrush, QColor, QPainter, QPalette
    from PySide6.QtCore import QSize
    import shiboken6
except ModuleNotFoundError:
    from PySide2.QtCore import Qt, QTimer, QThread, Signal
    from PySide2.QtWidgets import *
    from PySide2.QtGui import QStandardItemModel, QStandardItem, QPen, QBrush, QColor, QPainter, QPalette
    from PySide2.QtCore import QSize
    import shiboken2
import maya.api.OpenMaya as om
from maya.OpenMayaUI import MQtUtil

from XModules import MRigModules
from XModules import MComponent
from XBase.MBaseFunctions import StrUtils


def get_maya_main_window():
    try:
        instance = shiboken6.wrapInstance(int(MQtUtil().mainWindow()), QWidget)
    except NameError:
        instance = shiboken2.wrapInstance(int(MQtUtil().mainWindow()), QWidget)
    return instance


class HSeparator(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)


class VSeparator(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.VLine)


class XTreeView(QTreeView):

    def __init__(self):
        super().__init__()

        self.model = QStandardItemModel()

        self.model.setHorizontalHeaderLabels(['item', 'descript'])
        self.setModel(self.model)
        self._populate_tree()

        self.module_items = []

    def _populate_tree(self):
        # 创建根项目
        root = self.model.invisibleRootItem()

        # 一级项目1
        item1 = QStandardItem("水果")
        item1.appendRow([QStandardItem("苹果"), QStandardItem("红色的水果")])
        item1.appendRow([QStandardItem("香蕉"), QStandardItem("黄色的水果")])
        root.appendRow(item1)

        # 一级项目2
        item2 = QStandardItem("动物")
        # 二级项目
        sub_item1 = QStandardItem("哺乳动物")
        sub_item1.appendRow([QStandardItem("狗"), QStandardItem("人类的朋友")])
        sub_item1.appendRow([QStandardItem("猫"), QStandardItem("独立的宠物")])
        # 二级项目
        sub_item2 = QStandardItem("鸟类")
        sub_item2.appendRow([QStandardItem("鹦鹉"), QStandardItem("会说话的鸟")])
        item2.appendRow(sub_item1)
        item2.appendRow(sub_item2)
        root.appendRow(item2)

        # 展开所有节点
        self.expandAll()

    def add_rig_module(self):
        module_item = QStandardItem('test')
        self.module_items.append(module_item)
        return module_item


class TrafficLightIndicator(QWidget):
    """双灯状态指示器，用于显示操作进行中或完成状态"""

    def __init__(self, parent=None):
        super().__init__(parent)
        # 设置固定大小
        self.setFixedSize(QSize(80, 40))

        # 状态变量
        self.is_working = False
        self.left_light_on = False

        # 颜色定义
        self.color_red = QColor(255, 100, 0)
        self.color_green = QColor(0, 255, 100)
        self.color_gray = QColor(60, 60, 60)  # 熄灭状态的颜色

        # 定时器，用于控制闪烁
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.toggle_lights)

        # 设置背景为白色，确保指示灯清晰可见
        palette = self.palette()
        self.setPalette(palette)

    def start_working(self):
        """开始工作状态，两个灯交替闪烁"""
        self.is_working = True
        self.left_light_on = True
        self.timer.start(300)  # 每500毫秒切换一次状态
        self.update()

    def stop_working(self):
        """停止工作状态，左灯熄灭，右灯显示绿色"""
        self.is_working = False
        self.timer.stop()
        self.update()

    def toggle_lights(self):
        """切换指示灯状态"""
        self.left_light_on = not self.left_light_on
        self.update()

    def paintEvent(self, event):
        """绘制指示灯"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制左灯
        left_light_color = self.color_red if (self.is_working and self.left_light_on) else self.color_gray
        self.draw_light(painter, 15, 20, left_light_color)

        # 绘制右灯
        right_light_color = self.color_green if not self.is_working else \
            (self.color_red if (self.is_working and not self.left_light_on) else self.color_gray)
        self.draw_light(painter, 55, 20, right_light_color)

    def draw_light(self, painter, x, y, color):
        """绘制单个指示灯"""
        painter.save()

        # 绘制灯的外圆
        pen = QPen(Qt.black, 1)
        painter.setPen(pen)
        painter.setBrush(QBrush(color))
        painter.drawEllipse(x - 10, y - 10, 20, 20)

        painter.restore()

    def switch(self):
        if self.is_working:
            self.stop_working()
        elif not self.is_working:
            self.start_working()


class BlinkLight(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(QSize(40, 40))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.blink)

        self.blinking = False

        self.blink_on_color = QColor('#30e3ca')
        self.blink_off_color = QColor('#40514e')

        self.blink_ok = False
        self.blink_ok_color = QColor(0, 255, 0)
        self.seq_idx = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        blink_seq = [self.blink_on_color, self.blink_off_color]
        color = blink_seq[self.seq_idx]
        self.draw_light(painter, 20, 20, color)

    def blink(self):
        self.seq_idx = 1 if self.seq_idx == 0 else 0
        self.update()

    def draw_light(self, painter, x, y, color):
        painter.save()

        # 绘制灯的外圆
        pen = QPen(Qt.black, 1)
        painter.setPen(pen)
        painter.setBrush(QBrush(color))
        painter.drawEllipse(x - 10, y - 10, 10, 10)

        painter.restore()

    def start_blink(self):
        self.timer.start(100)

        self.update()

    def stop_blink(self):
        self.timer.stop()
        self.update()


class StandarProgressBar(QWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.bar = QProgressBar(self)
        self.light = BlinkLight(self)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.bar, 8)
        self.main_layout.addWidget(self.light, 2)

        self.setLayout(self.main_layout)

        self.light.start_blink()

        self.thread = ProgressThread()
        self.thread.progress_updated.connect(self.update_progress)

    def reset(self):
        self.bar.setValue(0)
        self.light.stop_blink()

    def update_progress(self, value):
        """更新进度条的值"""
        self.bar.setValue(value)


class ProgressThread(QThread):
    """更新进度的工作线程"""
    progress_updated = Signal(int)  # 定义一个信号，用于发送进度更新

    def run(self):
        """线程执行的方法"""
        for i in range(101):
            time.sleep(0.1)  # 模拟耗时操作
            self.progress_updated.emit(i)  # 发送进度信号


class ConfigWidget(QWidget):

    def __init__(self, parent, config=MComponent.SplineIKComponentConfig()):
        super().__init__(parent)
        self.config = config
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.editable = True
        self.items = []

        self.module_info_layout = QHBoxLayout()
        self.main_layout.addLayout(self.module_info_layout)

        self.parse_config()
        self.main_layout.addStretch()
        # self.load_style_sheet(rf'{os.path.dirname(__file__)}/qss/combobox_style.qss')

    @classmethod
    def create_by_component_config(cls, parent, config):
        instance = cls(parent, config=config)
        return instance

    def parse_config(self):

        for attr_name, attr_value in self.config.__dict__.items():
            print(attr_name, attr_value)
            if isinstance(attr_value, str):
                self.add_string_item(f'{StrUtils(attr_name).make_nice_string()}:', attr_value)
            elif isinstance(attr_value, bool):
                self.add_bool_item(f'{StrUtils(attr_name).make_nice_string()}:', attr_value)
            elif issubclass(type(attr_value), enum.Enum):
                self.add_combobox_item(attr_name, attr_value)
            elif isinstance(attr_value, int):
                self.add_numeric_item(attr_name, attr_value)
            self.main_layout.addWidget(HSeparator())

    def add_combobox_item(self, attr_name, attr_value):
        enum_class: enum.Enum = attr_value.__class__
        layout = QHBoxLayout()
        cbb = QComboBox()
        self.items.append(cbb)
        lable = QLabel(attr_name)
        layout.addWidget(lable, 2)
        layout.addWidget(cbb, 8)
        for item in enum_class:
            cbb.addItem(str(item.value))
        cbb.currentIndexChanged.connect(lambda idx: setattr(self.config, attr_name, list(enum_class)[idx]))
        cbb.currentIndexChanged.connect(lambda idx: print(getattr(self.config, attr_name)))
        self.main_layout.addLayout(layout)

    def add_numeric_item(self, attr_name, attr_value):
        layout = QHBoxLayout()
        sbox = QSpinBox()
        self.items.append(sbox)
        sbox.setValue(attr_value)
        lable = QLabel(attr_name)
        layout.addWidget(lable, 2)
        layout.addWidget(sbox, 8)
        sbox.valueChanged.connect(lambda x: setattr(self.config, attr_name, x))
        sbox.valueChanged.connect(lambda x: print(getattr(self.config, attr_name)))
        self.main_layout.addLayout(layout)
        return layout

    def add_string_item(self, attr_name, attr_value):
        layout = QHBoxLayout()
        line = QLineEdit(attr_value)
        self.items.append(line)
        lable = QLabel(attr_name)
        layout.addWidget(lable, 2)
        layout.addWidget(line, 8)
        line.textChanged.connect(lambda t: setattr(self.config, attr_name, t))
        line.textChanged.connect(lambda t: print(getattr(self.config, attr_name)))
        self.main_layout.addLayout(layout)
        return layout

    def add_bool_item(self, attr_name, attr_value):
        layout = QHBoxLayout()
        check_box = QCheckBox()
        self.items.append(check_box)
        check_box.setChecked(attr_value)
        lable = QLabel(attr_name)
        layout.addWidget(lable, 2)
        layout.addWidget(check_box, 8)
        check_box.stateChanged.connect(
            lambda s: setattr(self.config, attr_name, True) if s == 2 else setattr(self.config, attr_name, False))
        check_box.stateChanged.connect(lambda s: print(getattr(self.config, attr_name)))
        self.main_layout.addLayout(layout)
        return layout

    def set_editable(self, editable: bool):
        pass

    def craate_module_info(self):
        pass

    def load_style_sheet(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            style = f.read()
            self.setStyleSheet(style)
