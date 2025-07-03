import sys

import platform

from mcedit import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont, QTextCursor, QColor, QIcon, QTextCharFormat, QClipboard, \
    QTextDocumentFragment, QTextBlock
from options import *
from constants import *
from editpanel import *
from resultdisplay import *
from mcedit import *
from textdisplay import *

class FoolTextDisplayPanel(TextDisplayPanel):

    def __init__(self, parent = ...):
        super().__init__(parent)

        self.name = "Text Display(Fool)"

    def initUI(self):
        super().initBaseUI()

        fool_tool_layout = QHBoxLayout()
        fool_tool_wid  = QWidget()

        self.scaler = QDoubleSpinBox()
        self.scaler.setSingleStep(0.1)
        self.scaler.setValue(2.0)
        self.scaler.setSuffix("x")
        self.scaler.valueChanged.connect(self.onScaleChange)

        self.normal_offset = QDoubleSpinBox()
        self.normal_offset.setSingleStep(0.1)
        self.normal_offset.setValue(0)
        self.offset_label = QLabel("Normal offset")
        self.offset_label.setToolTip("0.0: Block\n0.0: Glass pane\n0.0: Sign")

        self.y_offset = QDoubleSpinBox()
        self.y_offset.setSingleStep(0.1)
        self.y_offset.setValue(0)

        self.auto_offsetting = QCheckBox()
        self.auto_offsetting.setChecked(True)

        fool_tool_layout.addWidget(QLabel("Scale"))
        fool_tool_layout.addWidget(self.scaler)
        fool_tool_layout.addWidget(self.offset_label)
        fool_tool_layout.addWidget(self.normal_offset)
        fool_tool_layout.addWidget(QLabel("Y offset"))
        fool_tool_layout.addWidget(self.y_offset)
        fool_tool_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        auto_offset_label = QLabel("Auto Offsetting")
        auto_offset_label.setToolTip("Auto offset adjusting for Y axis")
        fool_tool_layout.addWidget(auto_offset_label)
        fool_tool_layout.addWidget(self.auto_offsetting)

        fool_tool_wid.setLayout(fool_tool_layout)
        self.main_layout.addWidget(fool_tool_wid)

        self.initCopyPanel()

        self.result = ResultDisplay()
        self.main_layout.addWidget(self.result)

        self.setLayout(self.main_layout)

    def updateCommand(self):
        pass

    def onVersionChaneged(self,index):
        pass

    def currentEditor(self) -> MCEdit:
        return self.text_panel
    
    def document(self):
        return super().document()
    
    def onScaleChange(self, e):
        self.doc.scale = (self.scaler.value(), self.scaler.value())

