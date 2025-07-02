import sys

import platform
from sign_text_edit import SignTextEdit
from mcedit import MCEdit, SignEdit
from signeditpanel import *
from constants import *
from younyao_in import YounyaoIn
from insert_pic import PicInsert
from cmd2htm import parseCommand

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont, QTextCursor, QColor, QIcon, QTextCharFormat, QClipboard, \
    QTextDocumentFragment, QTextBlock, QFontDatabase
import json
from options import *
from app import *
from signinfo import *
from charpanel import *
from editpanel import *

class mainwin(QMainWindow):
    edit_panel : SignEditPanel
    sign_info : SignInfoEditor
    app : SignApp
    toolbar : QToolBar
    options : Options

    #toolbar buttons
    newtab :    QWidgetAction
    bold   :    QAction
    italic :    QAction
    underline   : QAction
    strikeline  : QAction
    younyao_in  : QAction
    fontcombo : QComboBox
    systemfontcombo : QComboBox #
    textcolor   : QWidgetAction
    colorbutton : QToolButton
    special_char: QWidget
    insert      : QAction

    #edit tab
    tabs : QTabWidget
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.options = Options()
        self.options.loadoptions()

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.onTabClosing)
        self.tabs.currentChanged.connect(self.onTabChange)

        #default editor panel
        edit_panel = SignEditPanel(parent=self)
        edit_panel.options = self.options
        edit_panel.sign.options = self.options
        self.addEdiorPanel(edit_panel)

        self.app.setCurrentPanel(edit_panel)


        #default side panel: sign info editor
        self.sign_info = SignInfoEditor(parent=self,app = self.app)
        self.sign_info_dock = QDockWidget('Sign Info', self)
        self.sign_info_dock.setWidget(self.sign_info)

        #default side panel: character picker
        self.char_picker = CharacterPanel(parent=self,app = self.app)
        self.char_picker_dock = QDockWidget('Character Picker', self)
        self.char_picker_dock.setWidget(self.char_picker)


        #add tabs
        self.setCentralWidget(self.tabs)

        #add default side panels
        self.addDockWidget(Qt.RightDockWidgetArea, self.sign_info_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, self.char_picker_dock)

        self.setGeometry(300, 300, win_width, win_height)
        self.setWindowTitle('Minecraft Sign Generator')
        
        self.createToolBar()

    def createToolBar(self):
        self.toolbar = self.addToolBar('Toolbar')
        font1 = QFont("minecraft", pointSize=18);
        font1.setBold(True)

        #add new tab
        self.newtab = QWidgetAction(self)
        self.newtab.setText('+')
        self.newtab.setFont(font1)

        newtab_button = QToolButton(self)
        newtab_button.setText('+')
        newtab_button.setFont(font1)
        newtab_button.setPopupMode(QToolButton.InstantPopup)
        newtab_button.setAutoRaise(True)

        tabmenu = QMenu(newtab_button)
        self.createNewTableMenu(tabmenu)
        newtab_button.setMenu(tabmenu)

        self.newtab.setToolTip('New tab')
        self.newtab.setDefaultWidget(newtab_button)


        #bold
        self.bold = QAction(self)
        self.bold.setText("B")
        self.bold.setShortcut(QKeySequence.Bold)
        self.bold.setToolTip("Bold")
        self.bold.setCheckable(True)

        self.bold.setFont(font1)
        self.bold.triggered.connect(self.onBold)

        #italic
        self.italic = QAction(self)
        self.italic.setText("I")
        self.italic.setShortcut(QKeySequence.Italic)
        self.italic.setToolTip("Italic")
        self.italic.setCheckable(True)
        self.italic.setFont(QFont("minecraft",pointSize=18,italic=True))
        self.italic.triggered.connect(self.onItalic)

        #underline
        self.underline = QAction(self)
        self.underline.setText("U")
        self.underline.setShortcut(QKeySequence.Underline)
        self.underline.setToolTip("Underline")
        self.underline.setCheckable(True)
        font2 = QFont("minecraft",pointSize=18);font2.setUnderline(True)
        self.underline.setFont(font2)
        self.underline.triggered.connect(self.onUnderline)

        #Strikeline
        self.strikeline = QAction(self)
        self.strikeline.setText("S")
        self.strikeline.setToolTip("Strikeline")
        self.strikeline.setCheckable(True)
        font3 = QFont("minecraft",pointSize=18);font3.setStrikeOut(True)
        self.strikeline.setFont(font3)
        self.strikeline.triggered.connect(self.onStrikeline)

        #font selector
        self.fontcombo = QComboBox()
        self.createFontCombo(self.fontcombo)
        self.fontcombo.activated.connect(self.onFontChanged)

        #color
        self.textcolor = QWidgetAction(self.toolbar)
        font4 = QFont("Minecraft",pointSize=18)

        self.colorbutton = QToolButton(self)
        self.colorbutton.setText("C")
        self.colorbutton.setFont(font4)
        self.colorbutton.setStyleSheet("color: green")
        self.colorbutton.setPopupMode(QToolButton.InstantPopup)
        self.colorbutton.setAutoRaise(True)

        menu = QMenu(self.colorbutton)
        self.createColorMenu(menu)
        self.colorbutton.setMenu(menu)

        self.textcolor.setToolTip("Color")
        self.textcolor.setDefaultWidget(self.colorbutton)

        #system font selector
        self.systemfontcombo = QComboBox()
        self.createSystemFontCombo(self.systemfontcombo)
        self.systemfontcombo.activated.connect(self.onSystemFontChange)

        self.younyao_in   = QAction("音")
        self.younyao_in.setToolTip("有鳥音轉換")
        font5 = QFont("mcprev,unimc",pointSize=18,italic=True);font5.setBold(True)
        self.younyao_in.setFont(font5)
        self.younyao_in.setCheckable(False)
        self.younyao_in.triggered.connect(self.onYounyaoInPopup)
        
        self.insert   = QAction("P")
        self.insert.setToolTip("Insert Image")
        font5 = QFont("mcprev,unimc",pointSize=18,italic=True);font5.setBold(True)
        self.insert.setFont(font5)
        self.insert.setCheckable(False)
        self.insert.triggered.connect(self.onInsert)

        self.textcolor.setToolTip("Color")
        self.textcolor.setDefaultWidget(self.colorbutton)

        self.toolbar.addAction(self.newtab)
        self.toolbar.addAction(self.bold)
        self.toolbar.addAction(self.italic)
        self.toolbar.addAction(self.underline)
        self.toolbar.addAction(self.strikeline)
        self.toolbar.addWidget(self.fontcombo)
        self.toolbar.addWidget(self.systemfontcombo)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.textcolor)
        self.toolbar.addAction(self.younyao_in)
        self.toolbar.addAction(self.insert)


        self.toolbar.setStyleSheet("QToolBar { spacing: 2px; }")

    def createNewTableMenu(self, menu : QMenu):
        newsign = QAction(self)
        newsign.setText('Sign editor')
        newsign.setData('sign')
        newsign.triggered.connect(self.onNewTab)

        menu.addAction(newsign)

    def createColorMenu(self, menu: QMenu) -> None:
        global colors, desp

        layout = QGridLayout()
        layout.setContentsMargins(4, 4, 4, 4)
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
            layout.addWidget(col, i // 8, i % 8)

        widget.setLayout(layout)

        action = QWidgetAction(menu)
        action.setDefaultWidget(widget)
        menu.addAction(action)
        menu.setStyleSheet("color: black")
        menu.addSeparator()
        more = QAction("More Color...", menu)
        more.triggered.connect(self.onMoreColorClick)
        menu.addAction(more)

    def createFontCombo(self, combo: QComboBox) -> None:
        global fonts_name
        combo.clear()
        for font in fonts_name:
            combo.addItem(font)
        combo.setCurrentIndex(0)

    def createSystemFontCombo(self, combo: QComboBox) -> None:
        for font in self.options.fontlist.keys():
            combo.addItem(font)
        combo.setCurrentIndex(0)

    def currentEditPanel(self) -> EditPanel:
        return self.tabs.currentWidget()

    def addEdiorPanel(self,panel : EditPanel):
        for editor in panel.edit_fields:
            editor.cursorPositionChanged.connect(self.onCursorPosChanged)
        self.tabs.addTab(panel, panel.name)

    def onTabChange(self):
        tab = self.tabs.currentWidget()
        self.app.setCurrentPanel(tab)

    def onNewTab(self):
        sender = self.sender()
        tab_type = sender.data() #should be string

        if tab_type == 'sign':
            panel = SignEditPanel(parent=self)
            panel.options = self.options
            panel.sign.options = self.options

            self.addEdiorPanel(panel)
        else:
            raise AssertionError('Unknown tab type: ' + tab_type)

    def onTabClosing(self,index):
        self.tabs.removeTab(index)

    def onColorClick(self):
        textpanel = self.currentEditPanel().currentEditor()
        cursor: QTextCursor = textpanel.textCursor()
        sender = self.sender().sender().parent()
        style = sender.styleSheet()
        color = style[18:25]

        if not cursor.selection().isEmpty():
            cursor.beginEditBlock()
            textformat = QTextCharFormat()
            textformat.setForeground(QColor(color))
            cursor.mergeCharFormat(textformat)
            cursor.endEditBlock()
        else:
            textpanel.setTextColor(QColor(color))

    def onMoreColorClick(self):
        textpanel = self.currentEditPanel().currentEditor()
        cursor: QTextCursor = textpanel.textCursor()

        dlg = QColorDialog(textpanel.textColor(), self)
        # dlg.show()
        color = dlg.getColor()
        dlg.close()

        if not cursor.selection().isEmpty():
            cursor.beginEditBlock()
            print(self.hasFocus())
            textformat = QTextCharFormat()
            textformat.setForeground(color.toRgb())
            cursor.mergeCharFormat(textformat)
            cursor.endEditBlock()
        else:
            textpanel.setTextColor(color)

    def onYounyaoInPopup(self):
        self.in_win = YounyaoIn(self.app)
        self.in_win.show()

    def onInsert(self):
        self.dialog = PicInsert(self,"")
        self.dialog.show()

    def onBold(self, ischecked):
        textpanel = self.currentEditPanel().currentEditor()
        cursor : QTextCursor = textpanel.textCursor()

        if not cursor.selection().isEmpty():
            cursor.beginEditBlock()
            textformat = QTextCharFormat()
            if ischecked:
                textformat.setFontWeight(75)
            else:
                textformat.setFontWeight(50)
            cursor.mergeCharFormat(textformat)
            cursor.endEditBlock()
        else:
            if ischecked:
                textpanel.setFontWeight(75)
            else:
                textpanel.setFontWeight(50)

    def onItalic(self, ischecked):
        textpanel = self.currentEditPanel().currentEditor()
        cursor : QTextCursor = textpanel.textCursor()

        if not cursor.selection().isEmpty():
            cursor.beginEditBlock()
            textformat = QTextCharFormat()
            if ischecked:
                textformat.setFontItalic(True)
            else:
                textformat.setFontItalic(False)
            cursor.mergeCharFormat(textformat)
            cursor.endEditBlock()
        else:
            if ischecked:
                textpanel.setFontItalic(True)
            else:
                textpanel.setFontItalic(False)

    def onUnderline(self, ischecked):
        textpanel = self.currentEditPanel().currentEditor()
        cursor : QTextCursor = textpanel.textCursor()

        if not cursor.selection().isEmpty():
            cursor.beginEditBlock()
            textformat = QTextCharFormat()
            if ischecked:
                textformat.setFontUnderline(True)
            else:
                textformat.setFontUnderline(False)
            cursor.mergeCharFormat(textformat)
            cursor.endEditBlock()
        else:
            if ischecked:
                textpanel.setFontUnderline(True)
            else:
                textpanel.setFontUnderline(False)

    def onStrikeline(self, ischecked):
        global pointSize
        textpanel = self.currentEditPanel().currentEditor()
        cursor : QTextCursor = textpanel.textCursor()

        if not cursor.selection().isEmpty():
            cursor.beginEditBlock()
            textformat = QTextCharFormat()
            if ischecked:
                textformat.setFontStrikeOut(True)
            else:
                textformat.setFontStrikeOut(False)
            cursor.mergeCharFormat(textformat)
            cursor.endEditBlock()
        else:
            #font = QFont("minecraft, unifont",pointSize=point_size)
            textformat = QTextCharFormat()
            if ischecked:
                textformat.setFontStrikeOut(True)
            else:
                textformat.setFontStrikeOut(False)
            textpanel.setCurrentCharFormat(textformat)

    def onSystemFontChange(self,index):
        global point_size
        textpanel = self.currentEditPanel().currentEditor()
        cursor: QTextCursor = textpanel.textCursor()
        selectedfont = self.systemfontcombo.currentText()


        if not cursor.selection().isEmpty(): #something is selected
            if selectedfont == 'default':
                print('Default font selected')
                textformat = QTextCharFormat()
                #textformat.setFontFamily('') #default font
                textformat.setFontFamilies(["mcprev", "unimc"])
                cursor.beginEditBlock()
                cursor.mergeCharFormat(textformat)
                cursor.endEditBlock()
                html = textpanel.toHtml()#avoding bug
                textpanel.setHtml(html)
            else:
                fontfamily = self.options.fontlist[selectedfont]
                textformat = QTextCharFormat()
                textformat.setFontFamilies(fontfamily)
                cursor.beginEditBlock()
                cursor.mergeCharFormat(textformat)
                cursor.endEditBlock()
        else:
            textformat = QTextCharFormat()
            if selectedfont == 'default':
                textpanel.setCurrentCharFormat(textformat) #reset text format
            else:
                fontfamily = self.options.fontlist[selectedfont]
                textformat.setFontFamilies(fontfamily)
                #textpanel.setFontFamily(fontfamily)
                textpanel.setCurrentCharFormat(textformat)

    def onCursorPosChanged(self):
        textpanel = self.currentEditPanel().currentEditor()
        self.italic.setChecked(textpanel.fontItalic())
        self.underline.setChecked(textpanel.fontUnderline())
        font = textpanel.currentFont()
        self.strikeline.setChecked(font.strikeOut())
        self.bold.setChecked(font.bold())

        #set font
        families = font.families()

        f = families_str(families)
        if f != "'mcprev','unimc'":
            if f in self.options.reverse_fontlist.keys():
                fontname = self.options.reverse_fontlist[f]
                self.systemfontcombo.setCurrentText(fontname)
            else:#font not supported
                print('Font not supported')
                self.systemfontcombo.setCurrentText('default')
        else:
            self.systemfontcombo.setCurrentText('default')

    def onFontChanged(self,index):
        textpanel = self.currentEditPanel().currentEditor()
        textpanel.font = index #set auto font conversion of mcedit

        cursor = self.currentEditPanel().currentEditor().textCursor()
        if not cursor.selection().isEmpty(): #some text selected, convert them to specific font
            start = cursor.selectionStart()
            end = cursor.selectionEnd()

            texts = cursor.selectedText()
            new_text = mapFont(texts,index)

            cursor.beginEditBlock()
            cursor.setPosition(start,QTextCursor.MoveAnchor)
            #replace old characters with new ones
            for i in range(len(texts)):
                org_pos = cursor.position()
                cursor.setPosition(org_pos + 1, QTextCursor.MoveAnchor)
                format = cursor.charFormat()
                cursor.setPosition(org_pos, QTextCursor.MoveAnchor)
                cursor.deleteChar()

                cursor.insertText(new_text[i],format)
                end = cursor.position()
            cursor.endEditBlock()
            cursor.setPosition(start)
            cursor.setPosition(end ,QTextCursor.KeepAnchor)
            self.currentEditPanel().currentEditor().setTextCursor(cursor)

def mapFont(text : str, target : Fonts):
    '''
    Map given text to target font
    @param text: text to map
    @param target: target font
    '''
    global fonts_mapping
    result = ''

    for c in text:
        #faster mapping method if text is in ASCII
        if ord('a') <= ord(c) <= ord('z'):
            index = ord(c) - ord('a')
            result += fonts_mapping[target][index]
            continue
        if ord('A') <= ord(c) <= ord('Z'):
            index = ord(c) - ord('A')
            result += fonts_mapping[target][index + 26]
            continue
        if ord('0') <= ord(c) <= ord('9'):
            index = ord(c) - ord('0')
            result += fonts_mapping[target][index + 52]
            continue

        #character not in ASCII
        conv_c = ''
        for available_font in fonts_mapping:
            if c in available_font:
                index = available_font.find(c)
                conv_c = fonts_mapping[target][index]
                break

        if conv_c == '':
            result += c # no match
        else:
            result += conv_c
    return result

def main():
    global point_size,win_width,win_height
    if platform.system() == "Windows":
        point_size = 36;win_width=1200;win_height=600
    elif platform.system() == "Darwin":
        point_size = 24;win_width=1000;win_height=500
    else:
        point_size = 24;win_width=1000;win_height=500

    print('Loading char list...')
    loadChars()
    app = SignApp(sys.argv)
    win = mainwin(app)
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    