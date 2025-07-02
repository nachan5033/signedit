import sys
import platform

from constants import *
from signpic import analyzeImage

from PyQt5.QtWidgets import (QApplication,QWidget, QGridLayout, 
    QPushButton,QLineEdit,QLabel,QHBoxLayout,QRadioButton,QDialog,QTextEdit,QAction,
    QToolButton,QStyle,QFileDialog)
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui  import QIcon,QFont

class PicInsert(QWidget):
    width   : int
    height  : int
    parent_window = None

    img_path    : QLineEdit
    img_open    : QPushButton
    img_browse  : QToolButton

    img_size    : QHBoxLayout
    btn1        : QRadioButton
    btn2        : QRadioButton
    btn3        : QRadioButton

    preview     : QLabel
    cancel      : QPushButton
    insert      : QPushButton

    html        : str
    def __init__(self, parent_window=None,default_path : str="") -> None:
        if platform.system() == 'Windows':
            self.width = 600;self.height = 220
        elif platform.system() == 'Darwin':
            self.width = 600;self.height = 220
        else:
            self.width = 600;self.height = 220

        self.parent_window = parent_window
        super().__init__()

        self.initUI()

        if default_path != "":
            self.img_path.setText(default_path)
            self.readImage()
    
    def initUI(self):
        global point_size

        layout = QGridLayout()
        self.setLayout(layout)

        self.img_path  = QLineEdit()
        self.img_path.setText("../18.png")
        self.img_open  = QPushButton("Open")
        self.img_open.clicked.connect(self.readImage)
        #self.img_path.textEdited.connect()

        self.img_browse= QToolButton()
        self.img_browse.setCheckable(False)
        action = QAction()
        action.setIcon(QIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton)))
        action.triggered.connect(self.onFileOpen)
        self.img_browse.setDefaultAction(action)

        self.img_size = QHBoxLayout()

        self.preview = QLabel("Preview")
        sheet = """QLabel{       
                                      font-size: %dpx; 
                                      font-family: 'mcprev','unimc';
                                      padding: 0;
                                      margin-bottom: 0px;
                                      background: url("./src/oak.png") repeat top center;
                                      }""" % point_size
        self.preview.setStyleSheet(sheet)
        font = QFont()
        font.setKerning(False)
        self.preview.setFont(font)
        self.preview.setAlignment(Qt.AlignCenter)

        self.cancel = QPushButton("Cancel")
        self.cancel.clicked.connect(self.close)
        self.insert = QPushButton("Insert Image")
        self.insert.clicked.connect(self.onInsert)

        layout.addWidget(QLabel("Image File:"),1,1,1,1)
        layout.addWidget(self.img_path,1,2,1,2)
        layout.addWidget(self.img_browse,1,4,1,1)
        layout.addWidget(self.img_open,1,5,1,1)

        layout.addWidget(QLabel("Width Mode:"),2,1,1,1)

        widget = QWidget()
        widget.setLayout(self.img_size)
        widget.setStyleSheet("{spacing:0px}")
        self.btn1 = QRadioButton("11px",self)
        self.btn2 = QRadioButton("18px",self)
        self.btn3 = QRadioButton("45px",self)
        self.btn1.toggled.connect(self.pixelChange)
        self.btn2.toggled.connect(self.pixelChange)
        self.btn3.toggled.connect(self.pixelChange)
        self.img_size.addWidget(self.btn1,1)
        self.img_size.addWidget(self.btn2,2)
        self.img_size.addWidget(self.btn3,4)

        layout.addWidget(widget,2,2,1,3)
        layout.addWidget(self.preview,3,1,4,4)
        layout.addWidget(self.cancel,5,5,1,1)
        layout.addWidget(self.insert,6,5,1,1)

        self.setGeometry(300, 300, self.width, self.height)
        #self.setFixedSize(QSize(self.width, self.height))
        self.setWindowTitle('Insert')   
    
    def readImage(self) -> None:
        path = self.img_path.text()
        width,self.html = analyzeImage(path)
        #replacement : str

        if width == -1:
            self.preview.setText("\nImage not found:\n%s" % path)
        else:
            if width <= 11:
                self.btn1.setChecked(True)
            elif width >= 45:
                self.btn3.setChecked(True)
            else:
                self.btn2.setChecked(True)
                
    def pixelChange(self):
        replacement : str
        if self.btn1.isChecked():
            replacement = "\u2b1b"
        elif self.btn2.isChecked():
            replacement = "▌"
        elif self.btn3.isChecked():
            replacement = "|"
        
        self.preview.setText(self.html.replace("$",replacement))
    
    def onInsert(self):
        if self.parent_window != None:
            html :str = self.preview.text()
            if html.startswith("<!DOCTYPE HTML"):
                self.parent_window.edit_panel.text_panel.setHtml(html)
                self.close()

    def onFileOpen(self):
        filename = QFileDialog.getOpenFileName(self,"Open Image",filter="Image files(*.jpg *.png *.gif *.jpeg *.bmp);;All files(*.*)")
        if len(filename) > 0:
            self.img_path.setText(filename[0])
            self.readImage()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = PicInsert(None,"")
    win.show()
    sys.exit(app.exec_())