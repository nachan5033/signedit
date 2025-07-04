import sys

import platform
from typing import Callable

from mcedit import *
from sign import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont, QTextCursor, QColor, QIcon, QTextCharFormat, QClipboard, \
    QTextDocumentFragment, QTextBlock
from options import *
from constants import *
#from signedit2 import *


class ResultDisplay(QWidget):

    updateFuncDict : dict[str,Callable]

    def __init__(self):
        super().__init__()
        self.updateFuncDict = {}
        self.loadFuncDict = {}

        self.result_panel = QPlainTextEdit()
        self.copy_button = QPushButton("Click to Copy")
        self.load_button = QPushButton('Load')
        self.version_combo = QComboBox()

        self.copy_button.clicked.connect(self.onCopyClicked)
        self.load_button.clicked.connect(self.onLoadButtonClicked)


        # load supported versions
        global supported_versions
        global_options = getGlobalOptions()
        for i in supported_versions:
            self.version_combo.addItem(i)

        # select default versions
        self.version_combo.setCurrentText(global_options.default_version)

        self.version_combo.currentIndexChanged.connect(self.onVersionChaneged)

        grid = QGridLayout()
        grid.addWidget(QLabel('Result'), 1, 1, 1, 1)
        grid.addWidget(self.result_panel, 2, 1, 1, 4)
        grid.addWidget(self.version_combo, 3, 2, 1, 1)
        grid.addWidget(self.load_button, 3, 3, 1, 1)
        grid.addWidget(self.copy_button, 3, 4, 1, 1)
        self.setLayout(grid)

    def resetCopyButton(self):
        self.copy_button.setText('Click to Copy')

    def version(self):
        return self.version_combo.currentText()

    def result_edit(self):
        return self.result_panel

    def registerUpdateFunc(self,version : str,func : Callable):
        """
        Register update function to update command
        update function: update() -> str
        """
        self.updateFuncDict[version] = func

    def registerLoadFunc(self,version : str,func : Callable):
        """
        Register load function to specific version

        load function: load(command : str) -> None
        """
        self.loadFuncDict[version] = func

    def onVersionChaneged(self,index):
        self.updateCommand()

    def updateCommand(self):
        self.resetCopyButton()
        version = self.version()
        if version in self.updateFuncDict.keys():
            s = self.updateFuncDict[version]()
            self.result_panel.setPlainText(s)
        else:
            self.result_panel.setPlainText('Version not supported')

    def onCopyClicked(self):
        global qApp
        clipboard: QClipboard = qApp.clipboard()
        clipboard.setText(self.result_panel.toPlainText())
        self.result_panel.selectAll()
        self.copy_button.setText("Copied!")

    def onLoadButtonClicked(self):
        if self.version() in self.loadFuncDict.keys():
            self.loadFuncDict[self.version()](self.result_panel.toPlainText())
        else:
            print('Load command from specific version is not supported')