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