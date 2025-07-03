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
from sign import *

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
    resultdisplay : ResultDisplay

    # document data
    sign : Sign


    def __init__(self, parent=...):
        super().__init__(parent)

        global win_width, win_height, point_size
        global names, types

        self.name = 'Sign'

        grid = QGridLayout()
        grid.setSpacing(10)

        self.sign = Sign()
        self.text_panel = SignEdit(parent=self)
        self.text_panel.sign = self.sign
        self.text_panel.textChanged.connect(self.onTextChange)

        self.edit_fields.append(self.text_panel)

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
        self.resultdisplay = ResultDisplay()
        self.resultdisplay.registerUpdateFunc('1.20',self.text_panel.getCommand120)
        self.resultdisplay.registerUpdateFunc('1.21',self.text_panel.getCommand121)
        self.resultdisplay.registerUpdateFunc('Raw',self.text_panel.getJsonText)
        self.resultdisplay.registerUpdateFunc('HTML',self.text_panel.toHtml)

        # create UI
        grid.addWidget(self.text_panel, 1, 1, 2, 4)
        grid.addWidget(QLabel('Run Command(1 command/line, 4 commands max)'), 3, 1, 1, 1)
        grid.addWidget(face_panel, 3, 3, 1, 2)
        grid.addWidget(self.command_panel, 4, 1, 1, 4)

        grid.addWidget(self.resultdisplay, 8, 1, 1, 4)

        self.setLayout(grid)


    def currentEditor(self) -> MCEdit:
        return self.text_panel

    def document(self) -> Document:
        return self.sign

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
        self.resultdisplay.updateCommand()
        self.resultdisplay.resetCopyButton()

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




