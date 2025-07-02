import sys

import platform

from sign_text_edit import SignTextEdit
from mcedit import *
from constants import *
from younyao_in import YounyaoIn
from insert_pic import PicInsert
from cmd2htm import parseCommand

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont, QTextCursor, QColor, QIcon, QTextCharFormat, QClipboard, \
    QTextDocumentFragment, QTextBlock
from options import *
from constants import *

class EditPanel(QWidget):
    edit_field : MCEdit
    result_field : QPlainTextEdit
    options : Options
    def __init__(self, parent = ...):
        super().__init__(parent)

    def updateCommand(self):
        pass

class SignEditPanel(EditPanel):
    text_panel: SignEdit

    # side control
    face_panel: QWidget
    front_switch: QRadioButton
    back_switch: QRadioButton
    both_side_check: QCheckBox

    #wax control
    wax_switch: QCheckBox

    # command
    command_panel: QPlainTextEdit

    # result
    result_panel: QPlainTextEdit
    copy_button: QPushButton
    load_button: QPushButton
    version_combo: QComboBox

    version : str

    # document data
    sign : Sign

    def __init__(self, parent=...):
        super().__init__(parent)

        global win_width, win_height, point_size
        global names, types

        grid = QGridLayout()
        grid.setSpacing(10)

        self.sign = Sign()
        self.text_panel = SignEdit(parent=self)
        self.text_panel.sign = self.sign
        self.text_panel.textChanged.connect(self.onTextChange)
        #self.text_panel.cursorPositionChanged.connect(self.onCursorPosChange)

        # ----side control----
        face_panel = QWidget(self)
        face_layout = QHBoxLayout()
        face_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        face_panel.setLayout(face_layout)
        self.front_switch = QRadioButton("Front sign")
        self.back_switch = QRadioButton("Back sign")
        self.front_switch.setStyleSheet("border:none")
        self.back_switch.setStyleSheet("border:none")
        self.front_switch.setChecked(True)
        self.front_switch.toggled.connect(self.onFaceChange)
        self.both_side_check = QCheckBox('Both side')
        self.both_side_check.setToolTip('Use the same text for both side')
        self.both_side_check.toggled.connect(self.onFaceChange)
        face_layout.addWidget(self.front_switch)
        face_layout.addWidget(self.back_switch)
        face_layout.addWidget(self.both_side_check)

        # ----wax control----
        self.wax_switch = QCheckBox("Waxed")
        self.wax_switch.setChecked(False)
        self.wax_switch.toggled.connect(self.onWaxed)
        face_layout.addWidget(self.wax_switch)

        # ----command----
        self.command_panel = QPlainTextEdit()
        self.command_panel.textChanged.connect(self.onCommandChange)
        #self.command_panel.setAcceptRichText(False)

        # ----result output----
        self.result_panel = QPlainTextEdit()
        self.copy_button = QPushButton("Click to Copy")
        self.load_button = QPushButton('Load')
        self.version_combo = QComboBox()

        #----set views----
        self.sign.editor = self.text_panel
        self.sign.result_display = self.result_panel

        global supported_versions  # create version selector
        for i in supported_versions:
            self.version_combo.addItem(i)
        self.version_combo.setCurrentIndex(0)
        self.version = '1.20'
        self.version_combo.currentIndexChanged.connect(self.onVersionChange)
        self.copy_button.clicked.connect(self.onCopyClick)
        # self.load_button.clicked.connect(self.onLoadCLick)

        # create UI
        grid.addWidget(self.text_panel, 1, 1, 2, 4)

        grid.addWidget(QLabel('Run Command(1 command/line, 4 commands max)'), 3, 1, 1, 1)

        grid.addWidget(face_panel, 3, 3, 1, 2)

        grid.addWidget(self.command_panel, 4, 1, 1, 4)
        grid.addWidget(QLabel("Result"), 5, 1, 1, 1)
        grid.addWidget(self.result_panel, 6, 1, 1, 4)

        grid.addWidget(self.copy_button, 7, 4, 1, 1)
        grid.addWidget(self.load_button, 7, 3, 1, 1)
        grid.addWidget(self.version_combo, 7, 2, 1, 1)

        self.setLayout(grid)

        self.edit_field = self.text_panel
        self.result_field = self.result_panel

    def onFaceChange(self):
        if self.both_side_check.isChecked():
            self.text_panel.bothMode()
            self.front_switch.setEnabled(False)
            self.back_switch.setEnabled(False)

        elif self.front_switch.isChecked():
            self.front_switch.setEnabled(True)
            self.back_switch.setEnabled(True)
            self.text_panel.frontMode()
        elif self.back_switch.isChecked():
            self.front_switch.setEnabled(True)
            self.back_switch.setEnabled(True)
            self.text_panel.backMode()

        #update command panel
        commands = self.sign.getCommandForFace(self.text_panel.face_mode)
        command_str = ''
        for command in commands:
            command_str += command
            command_str += '\n'
        self.command_panel.setPlainText(command_str)

        #update result
        self.updateCommand()

    def onWaxed(self):
        if self.wax_switch.isChecked():
            self.sign.waxed = True
            self.updateCommand()
        else:
            self.sign.waxed = False
            self.updateCommand()

    def updateCommand(self):
        if self.version == '1.20':
            self.result_panel.setPlainText(self.text_panel.getCommand120())
        if self.version == '1.21':
            self.result_panel.setPlainText(self.text_panel.getCommand121())
        if self.version == 'Raw':
            self.result_panel.setPlainText(self.text_panel.getJsonText())
        if self.version == 'HTML':
            self.result_panel.setPlainText(self.text_panel.toHtml())

        self.copy_button.setText('Click to Copy')

    def onVersionChange(self,index):
        self.version = self.version_combo.currentText()
        if index == 0: #1.20
            self.result_panel.setPlainText(self.text_panel.getCommand120())
        if index == 1: #1.21
            self.result_panel.setPlainText(self.text_panel.getCommand121())
        if index == 2: #Json Raw
            self.result_panel.setPlainText(self.text_panel.getJsonText())

    def onTextChange(self):
        #sync text
        self.text_panel.syncTextToDocument()
        self.updateCommand()

    def onCommandChange(self):
        # re-arrange commands in the textedit to list
        commands = self.command_panel.toPlainText().split('\n')

        # if there are commands
        if len(commands) >= 1:
            self.text_panel.setCommandsForCurrentFace(commands)
        self.updateCommand()

    def onCopyClick(self):
        clipboard : QClipboard = self.parent().app.clipboard()
        clipboard.setText(self.result_panel.toPlainText())
        self.result_panel.selectAll()
        self.copy_button.setText("Copied!")
        print(self.text_panel.getCommand120())

