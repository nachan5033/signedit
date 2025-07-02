import sys

import platform

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
import  math


class SignInfoEditor(QWidget):
    sign : Sign
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
        self.sign.name = self.sign_name.text()
        self.sign.type = types[i] + '_sign'

        filename = "./src/%s.png" % types[i - i % 2]
        sheet = """QTextEdit { background-color: lightgray;
                                               font-size: %dpx; 
                                              font-family: 'mcprev','unimc';
                                              padding: 0;
                                              margin-bottom: 0px;
                                              background: url("%s") repeat top center;
                                              }""" % (point_size, filename)
        self.app.getCurrentEditor().edit_field.setStyleSheet(sheet)
        self.app.getCurrentEditor().updateCommand()

class CharacterPanel(QTabWidget):
    app : SignApp

    char_tables : list[QWidget]
    scrolls : list[QScrollArea]
    buttons : list[list[QAction]]
    actions : list[QAction]
    current_category : list[int]
    page_spins : list[QSpinBox]
    max_pages_display : list[QLabel]

    type_display : list[QLabel]#type label for Emojis and Characters

    def __init__(self, parent=None,app : SignApp = None):
        super(CharacterPanel, self).__init__(parent)
        self.app = app
        self.type_display = []
        self.buttons = [[],[]]
        self.current_category = []
        self.page_spins = []
        self.max_pages_display = []
        self.initUI()


        global type_list
        for i in range(2):#load the first pages
            typenames = type_list[i]
            category_name = typenames[0]
            self.current_category[i] = 0

            self.type_display[i].setText(category_name)
            self.loadChars(type_index=i,category_index=0,page=1)



    def initUI(self):
        global type_list,icon_list
        self.char_tables = [QWidget(),QWidget(),QWidget()]
        self.scrolls = [QScrollArea(),QScrollArea(),QScrollArea()]
        font = QFont('mcprev,unimc',18)

        for i in range(2):
            self.scrolls[i].setWidgetResizable(True)
            layout0 = QVBoxLayout()
            layout0.setAlignment(Qt.AlignLeft)
            layout0.setContentsMargins(0,0,0,0)
            layout = QGridLayout()
            layout.setSpacing(1)
            layout.setAlignment(Qt.AlignLeft)

            self.char_tables[i].setLayout(layout0)
            self.scrolls[i].setWidget(self.char_tables[i])
            self.current_category.append(0)

            #create type switch
            type_names = type_list[i]
            layout1 = QGridLayout()
            layout1.setSpacing(1)
            type_switch_panel = QWidget()
            type_switch_panel.setLayout(layout1)

            for j in range(len(type_names)):
                button = QToolButton()
                button.setText(' ')
                button.setStyleSheet("width:20; height:20;background-color:#efefef;color:#000000")
                button.setToolTip(type_names[j])
                button.setFont(font)

                action = QAction(icon_list[i][j])
                action.setToolTip(type_names[j])
                action.setData((i,j))
                action.triggered.connect(self.onTypeSelectorClicked)
                button.setDefaultAction(action)
                layout1.addWidget(button,1,j + 1,1,1)


            layout0.addWidget(type_switch_panel)
            l = QLabel(type_names[i])
            l.setStyleSheet('padding-left:10;')
            self.type_display.append(l)
            layout0.addWidget(l)

            #create char buttons
            char_panel = QWidget()
            for j in range(80):
                button = QToolButton()
                button.setText('?')
                button.setStyleSheet("width:20; height:20;background-color:#efefef;color:#000000")
                action = QAction(' ')
                action.setFont(font)
                action.triggered.connect(self.onCharClicked)
                self.buttons[i].append(action)

                button.setDefaultAction(action)
                layout.addWidget(button, j // 10 + 2, j % 10 + 1, 1, 1)
                char_panel.setLayout(layout)

            layout0.addWidget(char_panel)

            #create page switch
            layout2 = QHBoxLayout()
            page_panel = QWidget()
            page_panel.setLayout(layout2)

            layout2.addWidget(QLabel('Pages:'))
            page_spin = QSpinBox()
            page_spin.setMinimum(0)
            prev,after = QToolButton(), QToolButton()
            prev_act, after_act = QAction(), QAction()
            prev_act.setText('<')
            after_act.setText('>')
            self.page_spins.append(page_spin)
            if i == 0:
                page_spin.valueChanged.connect(lambda : self.onPageChange(0))
                prev_act.triggered.connect(lambda : self.onPrevClicked(0))
                after_act.triggered.connect(lambda : self.onNextClicked(0))
            else:
                page_spin.valueChanged.connect(lambda : self.onPageChange(1))
                prev_act.triggered.connect(lambda: self.onPrevClicked(1))
                after_act.triggered.connect(lambda: self.onNextClicked(1))

            prev.setDefaultAction(prev_act)
            after.setDefaultAction(after_act)

            self.max_pages_display.append(QLabel(''))

            layout2.addWidget(prev)
            layout2.addWidget(after)
            layout2.addWidget(page_spin)
            layout2.addWidget(self.max_pages_display[i])

            layout0.addWidget(page_panel)


        self.addTab(self.scrolls[0],"Emojis")
        self.addTab(self.scrolls[1],"Characters")
        self.addTab(self.scrolls[2],'Icons')

    def loadChars(self,type_index : int,category_index : int, page : int):
        '''
        Load characters to specific button matrix
        @param type_index : index of character types (0 for emojis, 1 for chars)
        @param page : int : which page to load

        @return: total number of pages
        '''
        global type_list,special_char_list
        chars = special_char_list[type_index][category_index]


        page_size = len(self.buttons[type_index])
        pages =  math.ceil( len(chars) / page_size )
        if page > pages:
            page = 1
            self.page_spins[type_index].setValue(1)
            return
        if page < 1:
            page = pages
            self.page_spins[type_index].setValue(pages)
            return

        for i in range(page_size):
            index = (page - 1)*page_size + i
            c = ' '
            if index < len(chars):
                c = chars[index]
            self.buttons[type_index][i].setText(c)

        self.max_pages_display[type_index].setText('/%d'%pages)


    def onTypeSelectorClicked(self):
        global type_list
        chartype_index, category = self.sender().data()
        typenames = type_list[chartype_index]
        category_name = typenames[category]
        self.current_category[chartype_index] = category

        self.type_display[chartype_index].setText(category_name)
        self.loadChars(type_index=chartype_index,category_index=category,page=1)

    def onPrevClicked(self, type_index : int):
        spin = self.page_spins[type_index]
        spin.setValue(spin.value() - 1)
        #self.loadChars(type_index=type_index,category_index=self.current_category[type_index],page=spin.value())

    def onNextClicked(self, type_index : int):
        spin = self.page_spins[type_index]
        spin.setValue(spin.value() + 1)
        #self.loadChars(type_index=type_index,category_index=self.current_category[type_index],page=spin.value())


    def onPageChange(self,type_index):

        #if self.sender() is QSpinBox:
        self.loadChars(type_index,self.current_category[type_index],page=self.sender().value())

    def onCharClicked(self):
        editor = self.app.getCurrentEditor()
        cursor : QTextCursor = editor.edit_field.textCursor()

        format = QTextCharFormat()
        format.setFontFamilies(["mcprev", "unimc"])
        cursor.mergeCharFormat(format)
        cursor.insertText(self.sender().text())

        #print(self.sender().t)

