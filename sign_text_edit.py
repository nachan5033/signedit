from constants import *
from insert_pic import PicInsert

from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import QMimeData,Qt,QUrl
from PyQt5.QtGui import QTextCharFormat,QTextBlockFormat
from PyQt5 import QtGui

class SignTextEdit(QTextEdit):

    def insertFromMimeData(self, source: QMimeData | None) -> None:
        global point_size
        newdata = QMimeData()
        if source.hasHtml():
            html = source.html()
    
            doc = QTextEdit()
            doc.setHtml(html)

            format = QTextCharFormat()
            format.setFontFamilies(["minecraft","unifont"])
            format.setFontPointSize(point_size - 14)

            block  = QTextBlockFormat()
            block.clearBackground()
            block.setAlignment(Qt.AlignCenter)

            cursor = doc.textCursor()
            cursor.select(QtGui.QTextCursor.Document)
            cursor.setBlockFormat(block)
            cursor.mergeCharFormat(format)
            
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
