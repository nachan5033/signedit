
import lxml.etree
import lxml.html
from constants import *
from insert_pic import PicInsert
from parse import *

from PyQt5.QtWidgets import QTextEdit, QTextBrowser, QWidget,QPlainTextEdit,QStyle
from PyQt5.QtCore import QMimeData,Qt,QUrl
from PyQt5.QtGui import QTextCharFormat,QTextBlockFormat, QFont, QColor
from PyQt5 import QtGui
from options import Options
from sign import *

import json

import lxml, re

class SignEdit:
    pass

class MCEdit(QTextEdit):
    pass

class Document:
    pass

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

    def _removeFontSizeData(self, html_data : str):
        html = lxml.html.fromstring(html_data)

        #Replace h1-h5 label with a <p> label

        elements = html.xpath('//h1|//h2|//h3|//h4|//h5')
        for element in elements:
            p = lxml.html.Element('p')
            p.text = element.text
            for child in element.getchildren():
                p.append(child)
            element.getparent().replace(element, p)

        
        #replace font weights 
        elements = html.xpath('//*[@style]')
        for element in elements:
            exist_style = element.attrib.get("style", "")
            index = exist_style.find('font-size')
            if index != -1:
                font_size = re.match("font\\-size:[ A-Za-z0-9\\-_]*;", exist_style[index:])
                if font_size is not None:
                    new_style = exist_style.replace(font_size.group(), '')
                    element.attrib["style"] = new_style
                    exist_style = new_style

        return lxml.html.tostring(html).decode()
    
    def insertFromMimeData(self, source: QMimeData | None) -> None:
        global point_size
        newdata = QMimeData()
        if source.hasHtml():
            html = source.html()
            html = self._removeFontSizeData(html)
            doc = QTextEdit()
            doc.setHtml(html)

            cursor = doc.textCursor()
            cursor.select(QtGui.QTextCursor.Document)
            char_format = QTextCharFormat()
            block_format = cursor.blockFormat()

            block_format.clearBackground()
            block_format.setAlignment(Qt.AlignCenter)

            char_format.setFontFamily('')
            char_format.setFontFamilies(['mcprev', 'unimc'])
            char_format.setBackground(block_format.background())

            cursor.setBlockFormat(block_format)
            cursor.mergeCharFormat(char_format)

            font = QFont()
            font.setFamily('mcprev')
            font.setPixelSize(point_size)
            doc.setFont(font)
            
            print(doc.toHtml())
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
    
    def trySetSTyleSheet(self, sheet : str):
        """
        :param sheet: style sheet of CSS format

        try to set the style of the text panel, may be ignored by the children class
        """
        self.setStyleSheet(sheet)

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
        self.sign = parent.sign
        
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

        sign_type = self.sign.type
        sign_type = sign_type.replace('_hanging_sign', '')
        sign_type = sign_type.replace('_sign','')
        sheet = f"""QTextEdit {{ background-color: lightgray;
                                       font-size: {point_size}px; 
                                      font-family: 'mcprev','unimc';
                                      padding: 0;
                                      margin-bottom: 0px;
                                      background: url("./src/{sign_type}.png") repeat top center;
                                      }}""" 

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

