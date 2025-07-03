from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont, QTextCursor, QColor, QIcon, QTextCharFormat, QClipboard, \
    QTextDocumentFragment, QTextBlock
from options import *
from constants import *

class ColorPicker(QWidgetAction):
    def __init__(self, color : QColor | None, parent = ..., caption = '', enable_alpha = False):
        super().__init__(parent)

        self.enable_alpha = enable_alpha
        if color is not None:
            self.color = color
        else:
            self.color = QColor()
            self.color.setRgb(0, 0, 0, 0)

        self.colorbutton = QToolButton(parent)
        if caption == '':
            font = QFont("mcprev",pointSize=18)
            self.colorbutton.setText("C")
            self.colorbutton.setFont(font)
        else:
            self.colorbutton.setText(caption)

        self.colorbutton.setStyleSheet("color: green")
        self.colorbutton.setPopupMode(QToolButton.InstantPopup)
        self.colorbutton.setAutoRaise(True)

        self.color_menu = QMenu(self.colorbutton)
        self.createColorMenu()
        self.colorbutton.setMenu(self.color_menu)

        self.setToolTip("Color")
        self.setDefaultWidget(self.colorbutton)

        self.color_change = lambda color : color
        self.color_dialog_launched = lambda def_color : def_color
    
    def createColorMenu(self):
        global colors, desp

        layout = QGridLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        widget = QWidget()

        for i in range(len(colors)):
            col = QToolButton(self.color_menu)
            col.setText(" ")
            col.setStyleSheet("background-color: %s; width:8; height:10" % colors[i])
            col.setToolTip(desp[i])

            action = QAction(col)
            action.setCheckable(False)
            action.triggered.connect(self.onColorClick)
            col.setDefaultAction(action)
            layout.addWidget(col, i // 8, i % 8)

        widget.setLayout(layout)

        action = QWidgetAction(self.color_menu)
        action.setDefaultWidget(widget)
        self.color_menu.addAction(action)
        self.color_menu.setStyleSheet("color: black")
        self.color_menu.addSeparator()
        more = QAction("More Color...", self.color_menu)
        more.triggered.connect(self.onMoreColorClick)
        self.color_menu.addAction(more)
    
    def onColorClick(self, e):
        sender = self.sender().sender().parent()
        style = sender.styleSheet()
        self.color = style[18:25]
        self.color = QColor(self.color)
        self.color_change(self.color)

    def onMoreColorClick(self, e):
        self.color_dialog_launched(self.color)
        dlg = QColorDialog(self.color, self.parent())
        if self.enable_alpha:
            self.color = dlg.getColor(self.color, options=QColorDialog.ShowAlphaChannel)
        else:
            self.color = dlg.getColor(self.color)
        dlg.close()
        self.color_change(self.color)