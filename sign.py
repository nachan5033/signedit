from parse import *
from editpanel import EditPanel
from constants import *

from PyQt5.QtWidgets import QTextEdit, QTextBrowser, QWidget,QPlainTextEdit,QStyle
from PyQt5.QtCore import QMimeData,Qt,QUrl
from PyQt5.QtGui import QTextCharFormat,QTextBlockFormat, QFont, QColor
from PyQt5 import QtGui
from options import Options

import json

import lxml, re

def commandList2Str(commandList):
    s = ''
    for command in commandList:
        s += command
        s += '\n'
    return s

class Document:
    name: str
    type: str
    options: Options

    view_editor: EditPanel
    result_display: QPlainTextEdit


class Sign(Document):
    name: str
    type: str

    front_HTML: str
    back_HTML: str
    both_HTML: str

    front_commands: list
    back_commands: list
    both_commands: list  # temp command list for BOTH mode

    waxed: bool

    options: Options  # options for generate command

    face_mode: Facemodes

    parser: MyHTMLParser

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

        self.view_editor = None

        self.parser = MyHTMLParser()

    def getJsonText(self):
        pass

    def getCommandForFace(self, face: Facemodes):
        if face == Facemodes.FRONT:
            return self.front_commands
        elif face == Facemodes.BACK:
            return self.back_commands
        elif face == Facemodes.BOTH:
            return self.both_commands
        return []


    def loadFromJsonText(self, json_txt: str):
        json_obj = json.loads(json_txt)
        try:
            pass
        except:
            pass

    def getJsonTree(self, face: Facemodes):
        self.parser.set_options(self.options)
        json_obj = {'name': self.name, 'type': self.type}
        if self.waxed:
            json_obj['waxed'] = True

        if face == Facemodes.BOTH:  # both mode
            self.parser.set_command(self.both_commands)
            self.parser.parse(self.both_HTML)
            text_obj = self.parser.result().copy()
            json_obj['front_text'] = text_obj
            json_obj['back_text'] = text_obj
            self.parser.clearHTML()
        else:
            # parse front
            self.parser.set_command(self.front_commands)
            self.parser.parse(self.front_HTML)
            front_obj = self.parser.result().copy()  # prevent it from deleting by clearHTML()
            json_obj['front_text'] = front_obj
            self.parser.clearHTML()
            # parse back
            self.parser.set_command(self.back_commands)
            self.parser.parse(self.back_HTML)
            back_obj = self.parser.result().copy()
            json_obj['back_text'] = back_obj

            self.parser.clearHTML()

        return json_obj

    def getJsonText(self, face: Facemodes):
        obj = self.getJsonTree(face)
        return json.dumps(obj)

    def getCommand120(self, face: Facemodes):
        obj = self.getJsonTree(face)
        return treeToCommand120(obj)

    def getCommand121(self, face: Facemodes):
        return 'Not implemented'


