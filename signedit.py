import sys

import platform

from parse import makegive
from sign_text_edit import SignTextEdit
from mcedit import MCEdit, SignEdit
from constants import *
from younyao_in import YounyaoIn
from insert_pic import PicInsert
from cmd2htm import parseCommand

from PyQt5.QtWidgets import (QApplication,QWidget, QGridLayout, 
    QPushButton, QTextEdit, QLineEdit,QComboBox,QLabel,QHBoxLayout,
    QMainWindow,QAction,QWidgetAction,QToolButton,QColorDialog,QMenu,QTabWidget,
    QScrollArea,QRadioButton,QCheckBox,QPlainTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence,QFont,QTextCursor,QColor,QIcon,QTextCharFormat,QClipboard,QTextDocumentFragment,QTextBlock

from lxml import etree


class mainwin(QMainWindow):
    
    text_panel : SignEdit
    sign_name  : QLineEdit
    sign_combo : QComboBox
    char_table  : QTabWidget

    front_switch : QRadioButton
    back_switch  : QRadioButton

    command_panel   : QTextEdit
    result_panel    : QPlainTextEdit
    copy_button     : QPushButton

    bold   :    QAction
    italic :    QAction
    underline   : QAction
    strikeline  : QAction
    younyao_in  : QAction
    #font_trans  : QAction
    font_choose : QComboBox
    textcolor   : QWidgetAction    
    special_char: QWidget
    insert      : QAction

    app         :QApplication

    toolbar     = None
    colorbutton = None

    current_font = 0 #Normal

    sign_type : str = "birch"

    storage_html : str
    storage_command : str

    def __init__(self,app):
        global point_size,win_width,win_height
        if platform.system() == "Windows":
            point_size = 36;win_width=1200;win_height=600
        elif platform.system() == "Darwin":
            point_size = 24;win_width=1000;win_height=500
        else:
            point_size = 24;win_width=1000;win_height=500
        
        self.storage_html = ""
        self.storage_command = ""

        super().__init__()

        self.initUI()
        self.app = app
    
    def initUI(self):
        global win_width,win_height,point_size
        global names,types

        grid = QGridLayout()
        grid.setSpacing(10)

        #self.toolbar     = QLineEdit()
        self.createToolBox()
        self.text_panel  = SignEdit(parent=self)
        self.text_panel.textChanged.connect(self.onTextChange)
        self.text_panel.cursorPositionChanged.connect(self.onCursorPosChange)
        self.text_panel.setLineWrapMode(QTextEdit.NoWrap)
        #test#####################
        pass
        
    
        ##########################

        self.sign_name   = QLineEdit()
        self.sign_name.setText("Custom Sign")
        self.sign_name.textChanged.connect(self.onTextChange)

        self.sign_combo   = QComboBox()
        self.createSignCombo(self.sign_combo)
        self.sign_combo.activated.connect(self.onComboActivated)

        self.char_table  = QTabWidget()
        self.createCharTab(self.char_table)

        face_panel = QWidget(self)
        #face_panel.setStyleSheet("QWidget{border:1px solid gray; border-radius:15px;}")
        face_layout = QHBoxLayout()
        face_panel.setLayout(face_layout)
        self.front_switch = QRadioButton("Front sign")
        self.back_switch  = QRadioButton("Back sign")
        self.front_switch.setStyleSheet("border:none")
        self.back_switch.setStyleSheet("border:none")
        self.front_switch.setChecked(True)
        self.front_switch.toggled.connect(self.onFaceChange)
        self.both_side_check = QCheckBox('Both side')
        self.both_side_check.toggled.connect(self.onBothSideToggled)
        self.both_side_check.setToolTip('Use the same text for both side')
        #self.back_switch.toggled.connect(self.onFaceChange)

        face_layout.addWidget(self.front_switch)
        face_layout.addWidget(self.back_switch)
        face_layout.addWidget(self.both_side_check)

        self.command_panel   =   QTextEdit()
        self.command_panel.textChanged.connect(self.onTextChange)
        self.command_panel.setAcceptRichText(False)
        
        self.result_panel    =   QTextEdit()
        self.copy_button     =   QPushButton("Click to Copy")
        self.load_button     =   QPushButton('Load')
        self.copy_button.clicked.connect(self.onCopyClick)
        self.load_button.clicked.connect(self.onLoadCLick)
        self.signnames = dict(zip(types,names))
        self.result_panel.setAcceptRichText(False)

        #create UI
        grid.addWidget(self.text_panel,1,1,4,4)

        grid.addWidget(QLabel('Sign Name'),1,5,1,1)
        grid.addWidget(self.sign_name,1,6,1,3)
        grid.addWidget(QLabel('Sign Type'),2,5,1,1)
        grid.addWidget(self.sign_combo,2,6,1,3)
        grid.addWidget(self.char_table,3,5,3,4)

        grid.addWidget(QLabel('Run Command(1 command/line, 4 commands max)'),5,1,1,2)

        grid.addWidget(face_panel,5,3,1,2)

        grid.addWidget(self.command_panel,6,1,2,8)
        grid.addWidget(QLabel("Result"),8,1,1,8)
        grid.addWidget(self.result_panel,9,1,2,8)

        grid.addWidget(self.copy_button,11,8,1,1)
        grid.addWidget(self.load_button,11,7,1,1)

        #set editbox style

        sheet = """QTextEdit { background-color: lightgray;
                                       font-size: %dpx; 
                                      font-family: 'minecraft','unifont';
                                      padding: 0;
                                      margin-bottom: 0px;
                                      background: url("./src/oak.png") repeat top center;
                                      }""" % point_size

        self.text_panel.setStyleSheet(sheet)
        
        self.text_panel.setAlignment(Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(grid)
        self.setCentralWidget(widget)
        self.setGeometry(300, 300, win_width, win_height)
        self.setWindowTitle('Minecraft Sign Generator')    
        self.show()

    def createToolBox(self):
        self.toolbar = self.addToolBar('Toolbar')

        self.bold = QAction(self)
        self.bold.setText("B")
        self.bold.setShortcut(QKeySequence.Bold)
        self.bold.setToolTip("Bold")
        self.bold.setCheckable(True)
        font1 = QFont("minecraft",pointSize=18);font1.setBold(True)
        self.bold.setFont(font1)
        self.bold.triggered.connect(self.onBoldSideToggled)

        self.italic = QAction(self)
        self.italic.setText("I")
        self.italic.setShortcut(QKeySequence.Italic)
        self.italic.setToolTip("Italic")
        self.italic.setCheckable(True)
        self.italic.setFont(QFont("minecraft",pointSize=18,italic=True))
        self.italic.triggered.connect(self.onItalicToggle)

        self.underline = QAction(self)
        self.underline.setText("U")
        self.underline.setShortcut(QKeySequence.Underline)
        self.underline.setToolTip("Underline")
        self.underline.setCheckable(True)
        font2 = QFont("minecraft",pointSize=18);font2.setUnderline(True)
        self.underline.setFont(font2)
        self.underline.triggered.connect(self.onUnderlineToggle)

        self.strikeline = QAction(self)
        self.strikeline.setText("S")
        self.strikeline.setToolTip("Strikeline")
        self.strikeline.setCheckable(True)
        font3 = QFont("minecraft",pointSize=18);font3.setStrikeOut(True)
        self.strikeline.setFont(font3)
        self.strikeline.triggered.connect(self.onStrikelineToggle)

        self.font_choose   = QComboBox()
        self.createFontCombo(self.font_choose)
        self.font_choose.activated.connect(self.onFontChanged)

        self.textcolor = QWidgetAction(self.toolbar)
        #self.textcolor.setText("C")
        font4 = QFont("Minecraft",pointSize=18)

        self.colorbutton = QToolButton(self)
        self.colorbutton.setText("C")
        self.colorbutton.setFont(font4)
        self.colorbutton.setStyleSheet("color: green")
        self.colorbutton.setPopupMode(QToolButton.InstantPopup)
        self.colorbutton.setAutoRaise(True)

        self.younyao_in   = QAction("音")
        self.younyao_in.setToolTip("有鸟音")
        font5 = QFont("Minecraft,unifont",pointSize=18,italic=True);font5.setBold(True)
        self.younyao_in.setFont(font5)
        self.younyao_in.setCheckable(False)
        self.younyao_in.triggered.connect(self.onYounyaoInPopup)

        #self.font_trans  = QAction("𝓕")
        #self.younyao_in.setToolTip("Font translation")
        #font5 = QFont("Minecraft,unifont",pointSize=18,italic=True);font5.setBold(True)
        #self.younyao_in.setFont(font5)
        #self.younyao_in.setCheckable(False)
        #self.younyao_in.triggered.connect(self.onFontPopup)

        self.insert   = QAction("P")
        self.insert.setToolTip("Insert Image")
        font5 = QFont("Minecraft,unifont",pointSize=18,italic=True);font5.setBold(True)
        self.insert.setFont(font5)
        self.insert.setCheckable(False)
        self.insert.triggered.connect(self.onInsert)

        menu = QMenu(self.colorbutton)
        self.createColorMenu(menu)
        self.colorbutton.setMenu(menu)

        #self.createCharMenu(self.special_char)

        self.textcolor.setToolTip("Color")
        self.textcolor.setDefaultWidget(self.colorbutton)

        self.toolbar.addAction(self.bold)
        self.toolbar.addAction(self.italic)
        self.toolbar.addAction(self.underline)
        self.toolbar.addAction(self.strikeline)
        self.toolbar.addWidget(self.font_choose)
        self.toolbar.addSeparator()
        #self.toolbar.addWidget(self.colorbutton)
        self.toolbar.addAction(self.textcolor)
        self.toolbar.addAction(self.younyao_in)
        #self.toolbar.addAction(self.special_char)
        self.toolbar.addAction(self.insert)
        #self.toolbar.addAction(self.font_trans)


        self.toolbar.setStyleSheet("QToolBar { spacing: 2px; }")

    def createColorMenu(self,menu:QMenu)->None:
        global colors,desp

        #layout = QHBoxLayout()
        layout = QGridLayout()
        layout.setContentsMargins(4,4,4,4)
        widget = QWidget()
        
        for i in range(len(colors)):
            col = QToolButton(menu)
            col.setText(" ")
            col.setStyleSheet("background-color: %s; width:8; height:10" % colors[i])
            col.setToolTip(desp[i])

            action = QAction(col)
            action.setCheckable(False)
            action.triggered.connect(self.onColorClick)
            col.setDefaultAction(action)
            layout.addWidget(col,i//8,i%8)
        
        widget.setLayout(layout)

        action = QWidgetAction(menu)
        action.setDefaultWidget(widget)
        menu.addAction(action)
        menu.setStyleSheet("color: black")
        menu.addSeparator()
        more = QAction("More Color...",menu)
        more.triggered.connect(self.onMoreClick)
        menu.addAction(more)

    def createCharTab(self,tab : QTabWidget) -> None:
        global special_chars

        char_tabs = [QWidget(),QWidget(),QWidget(),QWidget()]
        scrolls   = [QScrollArea(),QScrollArea(),QScrollArea(),QScrollArea()]

        for i in range(len(char_tabs)):
            scrolls[i].setWidgetResizable(True)

            layout = QGridLayout()
            layout.setSpacing(1)
            layout.setAlignment(Qt.AlignLeft)
            char_tabs[i].setLayout(layout)
            scrolls[i].setWidget(char_tabs[i])
            #print("**************")

            for j in range(len(special_chars[i])):
                
                button = QToolButton()
                #button = QPushButton()
                button.setText(special_chars[i][j])
                button.setStyleSheet("width:20; height:20;background-color:#efefef;color:#000000")
                action = QAction(special_chars[i][j])
                action.setFont(QFont("unifont",18))
                action.triggered.connect(self.onCharSelect)
                button.setDefaultAction(action)
                layout.addWidget(button,j//14+1,j%14+1,1,1)

        tab.addTab(scrolls[0],"Arrows/Math")
        tab.addTab(scrolls[1],"Shapes")
        tab.addTab(scrolls[2],"Characters")
        tab.addTab(scrolls[3],"Icons")

    def createSignCombo(self,combo : QComboBox) -> None:
        global types,names

        for i in range(len(types)):
            combo.addItem(QIcon("./src/%s.png" % types[i-i%2]),'%s Sign' % names[i])
    
    def createFontCombo(self,combo : QComboBox) -> None:
        global fonts_name
        for i in range(len(fonts_name)):
            combo.addItem(fonts_name[i])
        pass

    def onTextChange(self):
        front_html = ""
        front_command = ""
        back_html = ""
        back_command = ""

        if self.front_switch.isChecked():
            if self.text_panel.toPlainText() != "":
                front_html = self.text_panel.toHtml()
                front_command = self.command_panel.toPlainText()
            back_html = self.storage_html
            back_command = self.storage_command
        else:
            if self.text_panel.toPlainText() != "":
                back_html = self.text_panel.toHtml()
                back_command = self.command_panel.toPlainText()
            front_html = self.storage_html
            front_command = self.storage_command
            
        #print(front_html)
        res = makegive(self.sign_type,front_html,front_command,back_html,back_command,self.sign_name.text(),bothside=self.both_side_check.isChecked())
        #self.result_panel.setText(res)
        self.result_panel.setPlainText(self.text_panel.toHtml())
        self.copy_button.setText("Click to copy")

        if self.text_panel.alignment() != Qt.AlignCenter:
            self.text_panel.setAlignment(Qt.AlignCenter)

    def onFaceChange(self):
        temp_html = self.storage_html
        temp_command = self.storage_command

        if self.text_panel.toPlainText() != "":
            self.storage_html = self.text_panel.toHtml()
        else:
            self.storage_html = ""

        self.storage_command = self.command_panel.toPlainText()

        self.text_panel.setHtml(temp_html)
        self.command_panel.setText(temp_command)

    def onBoldSideToggled(self,checked):
        cursor : QTextCursor = self.text_panel.textCursor()

        if not cursor.selection().isEmpty():
            cursor.beginEditBlock()
            
            format = QTextCharFormat()
            if checked:
                format.setFontWeight(75)
            else:
                format.setFontWeight(50)
            cursor.mergeCharFormat(format)
            cursor.endEditBlock()
        else:
            if checked:
                self.text_panel.setFontWeight(75)
            else:
                self.text_panel.setFontWeight(50)
        
    def onItalicToggle(self,checked):
        cursor : QTextCursor = self.text_panel.textCursor()

        if not cursor.selection().isEmpty():
            cursor.beginEditBlock()
            format = QTextCharFormat()#cursor.charFormat()
            if checked:
                format.setFontItalic(True)
            else:
                format.setFontItalic(False)
            cursor.mergeCharFormat(format)
            cursor.endEditBlock()
            
        else:
            if checked:
                self.text_panel.setFontItalic(True)
            else:
                self.text_panel.setFontItalic(False)

    def onUnderlineToggle(self,checked):
        cursor : QTextCursor = self.text_panel.textCursor()

        if not cursor.selection().isEmpty():
            cursor.beginEditBlock()
            
            format = QTextCharFormat()
            if checked:
                format.setFontUnderline(True)
            else:
                format.setFontUnderline(False)
            cursor.mergeCharFormat(format)
            cursor.endEditBlock()
        else:
            if checked:
                self.text_panel.setFontUnderline(True)
            else:
                self.text_panel.setFontUnderline(False)

    def onStrikelineToggle(self,checked):
        global point_size
        cursor : QTextCursor = self.text_panel.textCursor()

        if not cursor.selection().isEmpty():
            cursor.beginEditBlock()
            
            format = QTextCharFormat()
            if checked:
                format.setFontStrikeOut(True)
            else:
                format.setFontStrikeOut(False)
            cursor.mergeCharFormat(format)
            cursor.endEditBlock()
        else:
            font = QFont("minecraft",pointSize=point_size)
            
            if checked:
                font.setStrikeOut(True)
            else:
                font.setStrikeOut(False)
            self.text_panel.setCurrentFont(font)
        
    def onColorClick(self):
        cursor : QTextCursor = self.text_panel.textCursor()
        sender = self.sender().sender().parent()
        style = sender.styleSheet()
        color = style[18:25]
        
        if not cursor.selection().isEmpty():
            cursor.beginEditBlock()
            format = QTextCharFormat()
            format.setForeground(QColor(color))
            cursor.mergeCharFormat(format)
            cursor.endEditBlock()
        else:
            self.text_panel.setTextColor(QColor(color))
    
    def onMoreClick(self):
        cursor : QTextCursor = self.text_panel.textCursor()
        dlg = QColorDialog(self.text_panel.textColor(),self)
        #dlg.show()
        color = dlg.getColor()
        dlg.close()
        
        if not cursor.selection().isEmpty():
            cursor.beginEditBlock()
            print(self.hasFocus())
            format = QTextCharFormat()
            format.setForeground(color.toRgb())
            cursor.mergeCharFormat(format)
            cursor.endEditBlock()
        else:
            self.text_panel.setTextColor(color)

    def onCursorPosChange(self):
        self.italic.setChecked(self.text_panel.fontItalic())
        self.underline.setChecked(self.text_panel.fontUnderline())
        font : QFont = self.text_panel.currentFont()
        self.strikeline.setChecked(font.strikeOut())
        self.bold.setChecked(font.bold())

    def onComboActivated(self, index):
        global types,names,point_size
        filename = "./src/%s.png" % types[index - index%2]
        sheet = """QTextEdit { background-color: lightgray;
                                       font-size: %dpx; 
                                      font-family: 'minecraft','unifont';
                                      padding: 0;
                                      margin-bottom: 0px;
                                      background: url("%s") repeat top center;
                                      }""" % (point_size,filename)
        self.text_panel.setStyleSheet(sheet)
        self.sign_type = types[index]
        self.onTextChange()        

    def onFontChanged(self,index):
        self.current_font = index
        cursor : QTextCursor = self.text_panel.textCursor()
        if not cursor.selection().isEmpty():
            
            start = cursor.selectionStart()
            end   = cursor.selectionEnd()

            texts = cursor.selectedText()
            (new_texts,vlen) = self.mapping_text(texts)

            cursor.beginEditBlock()
            cursor.setPosition(start,QTextCursor.MoveAnchor)
            for i in range(len(texts)):
                org_pos = cursor.position()
                cursor.setPosition(org_pos+1,QTextCursor.MoveAnchor)
                format = cursor.charFormat()
                cursor.setPosition(org_pos,QTextCursor.MoveAnchor)
                #print('setting %d,color as %x' % (i,format.foreground().color().rgb()))
                cursor.deleteChar()
                
                cursor.insertText(new_texts[i],format)
            cursor.endEditBlock()
            cursor.setPosition(start)
            cursor.setPosition(start + vlen,QTextCursor.KeepAnchor)
            self.text_panel.setTextCursor(cursor)
            

    def mapping_text(self,text) -> tuple[str,int]:
        global fonts_mapping

        result = ""
        vlen = 0

        for i in text:
            chr = ''
            for j in range(len(fonts_mapping)):
                if i in fonts_mapping[j]:
                    chr = fonts_mapping[self.current_font][fonts_mapping[j].find(i)]
                    if self.current_font > 1 and self.current_font != 9:
                        vlen += 2
                    else:
                        vlen += 1
                    result += chr
                    break
            if chr == "":
                result += i
                vlen += 1
            
        
        return (result,vlen)
    
    def onCopyClick(self):
        clipboard : QClipboard = self.app.clipboard()
        clipboard.setText(self.result_panel.toPlainText())
        self.result_panel.selectAll()
        self.copy_button.setText("Copied!")

    def onCharSelect(self):
        cursor :QTextCursor = self.text_panel.textCursor()
        format = QTextCharFormat()
        format.setFontFamilies(["minecraft","unifont"])
        cursor.mergeCharFormat(format)
        cursor.insertText(self.sender().text())

    def onYounyaoInPopup(self):
        self.in_win = YounyaoIn(self.app)
        self.in_win.show()

    def onFontPopup(self):
        pass

    def onInsert(self):
        self.dialog = PicInsert(self,"")
        self.dialog.show()

    def onBothSideToggled(self):
        if self.both_side_check.isChecked():
            self.front_switch.setChecked(True)
            self.front_switch.setEnabled(False)
            self.back_switch.setEnabled(False)
        else:
            self.front_switch.setEnabled(True)
            self.back_switch.setEnabled(True)
        self.onTextChange()
    
    def onLoadCLick(self): 
        global names, types,point_size
        cmd = self.result_panel.toPlainText()
        sign_type,front,back = parseCommand(cmd)

        if sign_type.endswith('_sign'):
            sign_type = sign_type[:-5]
        name = self.signnames[sign_type]
        
        self.sign_combo.setCurrentText(name + ' Sign')
        self.front_switch.setChecked(True)
        self.text_panel.setHtml(front[0])    
        self.storage_html = back[0]
        self.command_panel.setText(front[1])
        self.storage_command = back[1] 
        
        index = self.sign_combo.currentIndex()   
        filename = "./src/%s.png" % types[index - index%2]
        sheet = """QTextEdit { background-color: lightgray;
                                       font-size: %dpx; 
                                      font-family: 'minecraft','unifont';
                                      padding: 0;
                                      margin-bottom: 0px;
                                      background: url("%s") repeat top center;
                                      }""" % (point_size,filename)
        self.text_panel.setStyleSheet(sheet)
        self.sign_type = types[index]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = mainwin(app)
    win.show()
    sys.exit(app.exec_())