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

class TextDisplayPanel(EditPanel):

    text_panel : MCEdit

    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Text Display"
        self.text_panel = MCEdit(parent)

        self.edit_fields.append(self.text_panel)

    def currentEditor(self) -> MCEdit:
        return self.text_panel
