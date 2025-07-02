
from constants import *
from insert_pic import PicInsert
from parse import *

from PyQt5.QtWidgets import QTextEdit, QTextBrowser, QWidget,QPlainTextEdit
from PyQt5.QtCore import QMimeData,Qt,QUrl
from PyQt5.QtGui import QTextCharFormat,QTextBlockFormat
from PyQt5 import QtGui
from options import Options

import json


class SignEdit:
    pass

class MCEdit(QTextEdit):
    pass

class Document:
    name : str
    type : str
    options : Options

    editor : MCEdit
    result_display : QPlainTextEdit

class Sign(Document):
    name : str
    type : str

    front_HTML :str
    back_HTML : str
    both_HTML : str

    front_commands : list
    back_commands : list
    both_commands : list#temp command list for BOTH mode

    waxed : bool

    options : Options #options for generate command

    face_mode: Facemodes

    editor : SignEdit
    command_editor : QPlainTextEdit
    result_display : QPlainTextEdit

    parser : MyHTMLParser

    def __init__(self):
        self.name = 'Custom Sign'
        self.type = 'oak_sign'
        self.front_HTML = ''
        self.back_HTML = ''
        self.both_HTML = ''
        self.front_commands = []
        self.back_commands = []
        self.both_commands = []
        self.waxed = False

        self.parser = MyHTMLParser()

    def getJsonText(self):
        pass

    def getCommandForFace(self,face:Facemodes):
        if face == Facemodes.FRONT:
            return self.front_commands
        elif face == Facemodes.BACK:
            return self.back_commands
        elif face == Facemodes.BOTH:
            return self.both_commands
        return []

    def updateCommand(self):
        face = self.editor.face_mode
        #self.result_display.setPlainText(self.editor.)


    def getJsonTree(self, face:Facemodes):
        self.parser.set_options(self.options)
        json_obj = {'name': self.name, 'type': self.type}
        if self.waxed:
            json_obj['waxed'] = True

        if face == Facemodes.BOTH: #both mode
            self.parser.set_command(self.both_commands)
            self.parser.parse(self.both_HTML)
            text_obj = self.parser.result().copy()
            json_obj['front_text'] = text_obj
            json_obj['back_text'] = text_obj
            self.parser.clearHTML()
        else:
            #parse front
            self.parser.set_command(self.front_commands)
            self.parser.parse(self.front_HTML)
            front_obj = self.parser.result().copy()  # prevent it from deleting by clearHTML()
            json_obj['front_text'] = front_obj
            self.parser.clearHTML()
            #parse back
            self.parser.set_command(self.back_commands)
            self.parser.parse(self.back_HTML)
            back_obj = self.parser.result().copy()
            json_obj['back_text'] = back_obj

            self.parser.clearHTML()

        return json_obj

    def getJsonText(self, face:Facemodes):
        obj = self.getJsonTree(face)
        return json.dumps(obj)

    def getCommand120(self, face:Facemodes):
        obj = self.getJsonTree(face)
        return treeToCommand120(obj)

    def getCommand121(self, face:Facemodes):
        return 'Not implemented'


class MCEdit(QTextEdit):
    font : Fonts
    parser : MyHTMLParser
    
    def __init__(self, parent : QWidget | None):
        super().__init__(parent)
        
        self.font = Fonts.NORMAL
        self.parser = MyHTMLParser()
    
    def keyPressEvent(self, ev):
        if self.font == Fonts.NORMAL:
            return super().keyPressEvent(ev)
        
        else: #special font mode, capture input
            chr : str
            if len(ev.text()) != 1: #no input
                return super().keyPressEvent(ev)
            chr = ev.text()[0]
            mapping = fonts_mapping[self.font]
                
            if 'a' <= chr <= 'z': #lower case
                index = ord(chr) - ord('a') #find where the character is in the mapping
                self.insertPlainText(mapping[index])
                ev.ignore()
                
            elif 'A' <= chr <= 'Z': #upper case
                index = ord(chr) - ord('A') + 26
                self.insertPlainText(mapping[index])
                ev.ignore()
            
            elif '0' <= chr <= '9':
                index = ord(chr) - ord('0') + 52
                self.insertPlainText(mapping[index])
                ev.ignore()
            
            else:
                return super().keyPressEvent(ev)
        return
    
    def getJsonText(self, opt : Options) -> str:
        return ''


    
    def insertFromMimeData(self, source: QMimeData | None) -> None:
        global point_size
        newdata = QMimeData()
        if source.hasHtml():
            html = source.html()
    
            doc = QTextEdit()
            doc.setHtml(html)

            textformat = QTextCharFormat()
            textformat.setFontFamilies(["mcprev","unimc"])
            textformat.setFontPointSize(point_size - 14)
            textformat.clearBackground()

            block  = QTextBlockFormat()
            block.clearBackground()
            block.setAlignment(Qt.AlignCenter)

            cursor = doc.textCursor()
            cursor.select(QtGui.QTextCursor.Document)
            cursor.setBlockFormat(block)
            cursor.mergeCharFormat(textformat)
            
            newdata.setHtml(doc.toHtml())
            return super().insertFromMimeData(newdata)
        elif source.hasUrls():
            path :str = source.urls()[0].toString()
            if path.startswith("file://"):
                path = path[7:]
            self.insert_panel = PicInsert(self.parent().parent(),path)
            self.insert_panel.show()
        else:
            return super().insertFromMimeData(source)

class SignEdit(MCEdit):
    face_mode : Facemodes
    front_html : str
    back_html : str
    both_html : str #temp HTML for BOTH mode
    
    front_command: list
    back_command: list
    both_command: list #temp command list for BOTH mode
    
    sign_type : str
    sign_name : str


    sign : Sign
    
    def __init__(self, parent):
        global point_size
        
        super().__init__(parent)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setMinimumHeight(250)
        #self.sign = Sign()

        self.face_mode = Facemodes.FRONT
        self.waxed = False
        
        self.syncStyle()

    def setSign(self, sign:Sign):
        self.sign = sign
        self.setHtml(self.getCachedHTML(self.face_mode))

    def getCachedHTML(self,facemode:Facemodes):
        if facemode == Facemodes.FRONT:
            return self.sign.front_HTML
        elif facemode == Facemodes.BACK:
            return self.sign.back_HTML
        return ''
    
    def syncStyle(self):
        sheet = """QTextEdit { background-color: lightgray;
                                       font-size: %dpx; 
                                      font-family: 'mcprev','unimc';
                                      padding: 0;
                                      margin-bottom: 0px;
                                      background: url("./src/oak.png") repeat top center;
                                      }""" % point_size

        self.setStyleSheet(sheet)
        self.setAlignment(Qt.AlignCenter)
    
    def setHtml(self, text):
        if text == '': #no html, just clear the page
            self.clear()
            self.syncStyle()
            return
        return super().setHtml(text)

    def switchMode(self, mode : Facemodes):
        if mode == Facemodes.FRONT:
            self.frontMode()
        elif mode == Facemodes.BACK:
            self.backMode()
        elif mode == Facemodes.BOTH:
            self.bothMode()

    def frontMode(self):
        if self.face_mode == Facemodes.BOTH:
            self.sign.front_HTML = self.toHtml()
        self.face_mode = Facemodes.FRONT
        self.setHtml(self.sign.front_HTML)
        self.syncStyle()
        
    
    def backMode(self):
        if self.face_mode == Facemodes.BOTH:
            self.sign.back_HTML = self.toHtml()
        self.face_mode = Facemodes.BACK
        self.setHtml(self.sign.back_HTML)
        self.syncStyle()


    def bothMode(self):
        self.sign.both_HTML = self.toHtml()
        self.face_mode = Facemodes.BOTH
        self.syncStyle()


    def syncTextToDocument(self):
        '''
        Sync text on the view to document object
        '''
        if self.face_mode == Facemodes.FRONT:
            self.sign.front_HTML = self.toHtml()
        elif self.face_mode == Facemodes.BACK:
            self.sign.back_HTML = self.toHtml()
        elif self.face_mode == Facemodes.BOTH:
            self.sign.both_HTML = self.toHtml()


    def getJsonText(self):
        return self.sign.getJsonText(self.face_mode)

    def getCommand120(self):
        return self.sign.getCommand120(self.face_mode)

    def getCommand121(self):
        return self.sign.getCommand121(self.face_mode)


    def setCommandsForCurrentFace(self,commands: list):
        if self.face_mode == Facemodes.FRONT: self.sign.front_commands = commands
        elif self.face_mode == Facemodes.BACK: self.sign.back_commands = commands
        elif self.face_mode == Facemodes.BOTH: self.sign.both_commands = commands

