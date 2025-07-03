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
from textdisplay_parse import *
from colorpicker import ColorPicker

class TextDisplayEdit(MCEdit):
    global point_size
    def __init__(self, parent : QWidget | None):
        super().__init__(parent)
        self._parent = parent
        sheet = f"""QTextEdit {{ background-color: lightgray;
                                       font-size: {point_size}px; 
                                      font-family: 'mcprev','unimc';
                                      padding: 0;
                                      margin-bottom: 0px;
                                      background: url("./src/oak.png") repeat top center;
                                      }}"""

        self.setStyleSheet(sheet)
        self.setMinimumHeight(300)
    
    def trySetSTyleSheet(self, sheet):
        if self._parent.background_select.isChecked():
            return #ignore it
        return super().trySetSTyleSheet(sheet)

class TextDisplayPanel(EditPanel):

    def __init__(self, parent = ...):
        super().__init__(parent)
        self.name = "Text Display"
        self.doc = TextDisplayDoc()
        self.doc.type = 'oak_sign'

        self.text_panel = TextDisplayEdit(self)
        self.edit_fields.append(self.text_panel)

    def currentEditor(self) -> MCEdit:
        return self.text_panel

    def initBaseUI(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.text_panel)
        
        text_tool_layout = QHBoxLayout()
        self.align_left = QRadioButton("Left")
        self.align_center = QRadioButton("Center")
        self.align_right = QRadioButton("Right")
        self.align_left.toggled.connect(self.onAlignToggled);self.align_right.toggled.connect(self.onAlignToggled)
        self.align_center.toggled.connect(self.onAlignToggled)
        self.align_mode = "left"
        self.align_center.setChecked(True)

        self.background_select = QCheckBox("Background")
        self.background_select.toggled.connect(self.onBackgroundChecked)
        self.background_picker = ColorPicker(None, self, "█", enable_alpha=True)
        self.background_picker.colorbutton.setVisible(True)
        self.background_picker.colorbutton.setEnabled(False)
        self.background_picker.color_change = self.onBackgroundChanged

        self.glowing_select = QCheckBox("Glowing")
        self.glowing_select.setChecked(True)
        self.shadow_select = QCheckBox("Shadow")
        self.glowing_select.toggled.connect(self.onGlowingShadowChecked)
        self.shadow_select.toggled.connect(self.onGlowingShadowChecked)

        text_tool_layout.addWidget(QLabel("Alignment:"))
        text_tool_layout.addWidget(self.align_left)
        text_tool_layout.addWidget(self.align_center)
        text_tool_layout.addWidget(self.align_right)
        text_tool_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        text_tool_layout.addWidget(self.background_select)
        color_picker = QToolButton()
        color_picker.addAction(self.background_picker)
        text_tool_layout.addWidget(self.background_picker.colorbutton)
        text_tool_layout.addWidget(self.glowing_select)
        text_tool_layout.addWidget(self.shadow_select)

        text_tool_wid =  QWidget()
        text_tool_wid.setLayout(text_tool_layout)
        self.main_layout.addWidget(text_tool_wid)

    def initCopyPanel(self):
        copy_panel_layout = QHBoxLayout()
        copy_panel_widget = QWidget()

        self.mode_summon = QRadioButton("Summon")
        self.mode_copy_wall = QRadioButton("/give (wall)")
        self.mode_copy_ground = QRadioButton("/give (ground)")
        self.mode_copy_wall.setChecked(True)

        copy_panel_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        copy_panel_layout.addWidget(QLabel("Command format:"))
        copy_panel_layout.addWidget(self.mode_summon)
        copy_panel_layout.addWidget(self.mode_copy_wall)
        copy_panel_layout.addWidget(self.mode_copy_ground)

        copy_panel_widget.setLayout(copy_panel_layout)
        self.main_layout.addWidget(copy_panel_widget)





    def document(self):
        return self.doc
    
    def onBackgroundChanged(self, color : QColor):
        global point_size
        color = QColor(color)
        (r, g, b, a) = color.toRgb().getRgb()
        self.background_picker.colorbutton.setStyleSheet("color:#%02x%02x%02x;" % (r, g, b))
        sheet = "QTextEdit { background-color: #%02x%02x%02x;\
                                       font-size: %dpx; \
                                      font-family: 'mcprev','unimc';\
                                      padding: 0;\
                                      margin-bottom: 0px;\
                                      }" % (r, g, b, point_size)
        self.text_panel.setStyleSheet(sheet)
        self.doc.background = (r, g, b, a)
    
    def onAlignToggled(self, e):

        align_dict = {'center':Qt.AlignCenter, 'left':Qt.AlignLeft, 'right':Qt.AlignRight}

        if self.align_center.isChecked():
            align = 'center'
        elif self.align_left.isChecked():
            align = 'left'
        elif self.align_right.isChecked():
            align = 'right'

        if self.align_mode != align:
            self.align_mode = align
            cursor = self.text_panel.textCursor()
            cursor.select(QtGui.QTextCursor.Document)
            block = cursor.blockFormat()
            block.setAlignment(align_dict[align])
            cursor.mergeBlockFormat(block)
            self.doc.align = align

    def onBackgroundChecked(self, e):
        global point_size
        if self.background_select.isChecked():
            self.doc.use_background = True
            self.background_picker.colorbutton.setEnabled(True)
            self.onBackgroundChanged(QColor.fromRgb(self.doc.background[0], self.doc.background[1], self.doc.background[2], 0))
        else: #set back to the sign background
            wood_type = self.document().type
            wood_type = wood_type.replace("_hanging_sign", "")
            wood_type = wood_type.replace("_sign", "")

            sheet = f"""QTextEdit {{ background-color: lightgray;
                                       font-size: {point_size}px; 
                                      font-family: 'mcprev','unimc';
                                      padding: 0;
                                      margin-bottom: 0px;
                                      background: url("./src/{wood_type}.png") repeat top center;
                                      }}"""
            
            self.text_panel.setStyleSheet(sheet)
            self.doc.use_background = False
            self.background_picker.colorbutton.setEnabled(False)

    def onGlowingShadowChecked(self, e):
        if self.glowing_select.isChecked():
            self.doc.glow = True
        else:
            self.doc.glow = False

        if self.shadow_select.isChecked():
            self.doc.shadow = True
        else:
            self.doc.shadow = False