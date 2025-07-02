
from mcedit import *
from constants import *
from younyao_in import YounyaoIn
from insert_pic import PicInsert
from cmd2htm import parseCommand
from app import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont, QTextCursor, QColor, QIcon, QTextCharFormat, QClipboard, \
    QTextDocumentFragment, QTextBlock
from options import *
from constants import *



class SignInfoEditor(QWidget):
    app : SignApp
    def __init__(self, parent=None,app : SignApp = None):
        super(SignInfoEditor, self).__init__(parent)

        self.app = app

        layout = QGridLayout()
        self.sign_name = QLineEdit()
        self.sign_name.setPlaceholderText("Sign name")
        self.sign_name.setText('Custom Sign')
        self.sign_name.textChanged.connect(self.onSignChange)

        self.sign_combo = QComboBox()
        self.createSignCombo(self.sign_combo)
        self.sign_combo.setCurrentIndex(0)
        self.sign_combo.currentIndexChanged.connect(self.onSignChange)

        layout.addWidget(QLabel('Sign Name'),1,1,1,1)
        layout.addWidget(self.sign_name,1,2,1,1)
        layout.addWidget(QLabel('Sign Type'),2,1,1,1)
        layout.addWidget(self.sign_combo,2,2,1,1)

        self.setLayout(layout)

    def createSignCombo(self, combo):
        global types,names

        for i in range(len(types)):
            combo.addItem(QIcon("./src/%s.png" % types[i - i % 2]), '%s Sign' % names[i])

    def onSignChange(self):
        global types,names
        i = self.sign_combo.currentIndex()
        doc = self.app.currentEditPanel().document()
        doc.name = self.sign_name.text()
        doc.type = types[i] + '_sign'

        filename = "./src/%s.png" % types[i - i % 2]
        sheet = """QTextEdit { background-color: lightgray;
                                               font-size: %dpx; 
                                              font-family: 'mcprev','unimc';
                                              padding: 0;
                                              margin-bottom: 0px;
                                              background: url("%s") repeat top center;
                                              }""" % (point_size, filename)
        self.app.currentEditPanel().currentEditor().setStyleSheet(sheet)
        self.app.currentEditPanel().updateCommand()

    def updateSignInfo(self):
        doc = self.app.currentEditPanel().document()
        self.sign_name.setText(doc.name)
        if doc.type != '':
            self.sign_combo.setCurrentText(doc.type[:-5]) #stripe '_sign'
