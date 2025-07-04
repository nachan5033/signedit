import sys

import platform

from mcedit import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont, QTextCursor, QColor, QIcon, QTextCharFormat, QClipboard, \
    QTextDocumentFragment, QTextBlock
from options import *
from constants import *

class EditPanel(QWidget):
    edit_fields : list[MCEdit]
    #list of MCEdits in the panel
    options : Options

    name : str
    doc : Document


    def __init__(self, parent = ...):
        super().__init__(parent)
        self.name = 'Undefined'
        self.edit_fields = []

    def updateCommand(self):
        pass

    def currentEditor(self) -> MCEdit:
        pass

    def document(self) -> Document:
        pass