try:
    from PySide6 import QtCore, QtGui
    from PySide6.QtWidgets import *
    from PySide6.QtCore import QSize
    from PySide6.QtGui import Qt
except ModuleNotFoundError:
    from PySide2 import QtCore, QtGui
    from PySide2.QtWidgets import *
    from PySide2.QtCore import QSize
    from PySide2.QtGui import Qt
from . import XUIWidgets as xw


class XRigMainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(parent=xw.get_maya_main_window(), *args, **kwargs)
        self.setWindowTitle('XRig')
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self._resize_windows(0.2, 0.6)
        self.vis = True

        self.test_btn()
        # self.start_btn.clicked.connect(self.on_licked)
        self.frame = True

        self.page_widgets = []
        self.current_page_idx = 0

        self.create_info()

    def _resize_windows(self, *factors):
        width_factor = factors[0]
        height_factor = factors[1]
        main_screen = QApplication.primaryScreen()
        width = int(main_screen.size().width() * width_factor)
        height = int(main_screen.size().height() * height_factor)
        self.resize(QSize(width, height))

    def test_btn(self):
        self.start_btn = QPushButton('start')
        self.end_btn = QPushButton('end')
        self.main_layout.addWidget(self.start_btn)
        # self.main_layout.addWidget(self.end_btn)

    def test_treeview(self):
        self.tree_view = xw.XTreeView()
        self.main_layout.addWidget(self.tree_view)

    def create_stack(self):
        self.stack = QStackedWidget()
        self.main_layout.addWidget(self.stack)
        self.create_pages()

    def create_pages(self):
        for i in range(5):
            page = QWidget()
            layout = QVBoxLayout()
            page.setLayout(layout)
            self.page_widgets.append(page)
            button = QLabel(f'Page{i + 1}')
            layout.addWidget(button)
            self.stack.addWidget(page)

    def on_licked(self):
        self.current_page_idx = self.current_page_idx + 1 if self.current_page_idx < 4 else 0
        self.stack.setCurrentIndex(self.current_page_idx)

    def create_info(self):
        widget = xw.ConfigWidget(self)
        self.main_layout.addWidget(widget)


class FloatingWindow(QWidget):

    def __init__(self, parent):
        super().__init__(parent=xw.get_maya_main_window())
        self.setWindowTitle('Test')
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(QPushButton('test'))


class MiniWin(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(parent=xw.get_maya_main_window(), *args, **kwargs)
        self.setWindowTitle('XRig')
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self._resize_windows(0.2, 0.6)
        self.button1 = QPushButton('test1')
        self.button2 = QPushButton('test2')

        self.main_layout.addWidget(self.button1)
        self.main_layout.addWidget(self.button2)
        self.button1.clicked.connect(self.create_bp)
        self.button2.clicked.connect(self.read_bp)

    def create_bp(self):
        from XModules import MBlueprint as mb
        self.bp = mb.MBlueprintArm('LF_Arm_01')
        self.bp.create_initial_skeleton()

    def read_bp(self):
        self.bp.read_skeleton_from_scene()

    def _resize_windows(self, *factors):
        width_factor = factors[0]
        height_factor = factors[1]
        main_screen = QApplication.primaryScreen()
        width = int(main_screen.size().width() * width_factor)
        height = int(main_screen.size().height() * height_factor)
        self.resize(QSize(width, height))
