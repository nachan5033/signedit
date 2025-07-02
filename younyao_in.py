import sys
import platform

from constants import *
from pyconv import toPinyin,makeFullWidth

from PyQt5.QtWidgets import (QApplication,QWidget, QGridLayout, 
    QPushButton,QLineEdit,QLabel,QHBoxLayout,QRadioButton,QDialog)
from PyQt5.QtCore import Qt,QSize

class YounyaoIn(QWidget):
    text_panel : QLineEdit
    width_mode : QHBoxLayout
    
    result_1    :QLineEdit
    result_2    :QLineEdit
    result_3    :QLineEdit

    copy1       :QPushButton
    copy2       :QPushButton
    copy3       :QPushButton

    app         :QApplication

    width : int
    height: int

    def __init__(self,app):
        if platform.system() == 'Windows':
            self.width = 440;self.height = 220
        elif platform.system() == 'Darwin':
            self.width = 420;self.height = 220
        else:
            self.width = 420;self.height = 220

        super().__init__()
        
        self.app = app
        self.initUI()
    
    def initUI(self):
        layout = QGridLayout(self)
        self.setLayout(layout)

        self.text_panel = QLineEdit()
        self.result_1   = QLineEdit()
        self.result_2   = QLineEdit()
        self.result_3   = QLineEdit()
        self.width_mode      = QHBoxLayout()

        self.copy1 = QPushButton("Copy")
        self.copy2 = QPushButton("Copy")
        self.copy3 = QPushButton("Copy")

        self.copy1.clicked.connect(self.onCopyClick)
        self.copy2.clicked.connect(self.onCopyClick)
        self.copy3.clicked.connect(self.onCopyClick)

        layout.addWidget(QLabel("待轉換文本"),1,1,1,1)
        layout.addWidget(self.text_panel,1,2,1,3)
        self.text_panel.textEdited.connect(self.onTextChange)
        
        desp = QLabel("用【】或[]標記多音字發音")
        desp.setAlignment(Qt.AlignCenter)
        layout.addWidget(desp,2,2,1,1)

        widget = QWidget(self)
        widget.setLayout(self.width_mode)
        widget.setStyleSheet("spacing:0px")
        btn1 = QRadioButton("半寬",self);btn1.setChecked(True);btn1.setStyleSheet("spacing:0px")
        btn2 = QRadioButton("全寬",self);btn2.setStyleSheet("spacing:0px")
        btn1.toggled.connect(self.onStateChange)
        btn2.toggled.connect(self.onStateChange)
        
        self.width_mode.addWidget(btn1,1)
        self.width_mode.addWidget(btn2,2)
        self.width_mode.setAlignment(Qt.AlignLeft)
        self.width_mode.setSpacing(0)
        layout.addWidget(widget,2,1,1,1)

        layout.addWidget(self.result_1,3,1,1,3)
        layout.addWidget(self.copy1,3,4,1,1)
        layout.addWidget(self.result_2,4,1,1,3)
        layout.addWidget(self.copy2,4,4,1,1)
        layout.addWidget(self.result_3,5,1,1,3)
        layout.addWidget(self.copy3,5,4,1,1)

        self.setGeometry(300, 300, self.width, self.height)
        #self.resize(420,200)
        self.setFixedSize(QSize(self.width, self.height))
        self.setWindowTitle('有鳥音轉換實用程式')   
        
    def onTextChange(self):
        res = toPinyin(self.text_panel.text())
        in2 = ""
        in1 = ""
        for i in res:
            in2 += i
            in1 += i.title()

        in3 = in2.upper()
        in2 = in2.title()

        self.result_1.setText(in1)
        self.result_2.setText(in2)
        self.result_3.setText(in3)

        self.copy1.setText("Copy")
        self.copy2.setText("Copy")
        self.copy3.setText("Copy")
    
    def onStateChange(self):
        if self.sender().text() == "全寬":
            self.result_1.setText(makeFullWidth(self.result_1.text()))
            self.result_2.setText(makeFullWidth(self.result_2.text()))
            self.result_3.setText(makeFullWidth(self.result_3.text()))
        else:
            self.onTextChange()
    
    def onCopyClick(self):
        clipboard = self.app.clipboard()
        sender = self.sender()
        sender.setText("Copied!")

        if sender == self.copy1:
            clipboard.setText(self.result_1.text())
            self.result_1.selectAll()
        elif sender == self.copy2:
            clipboard.setText(self.result_2.text())
            self.result_2.selectAll()
        elif sender == self.copy3:
            clipboard.setText(self.result_3.text())
            self.result_3.selectAll()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = YounyaoIn(app)
    win.show()
    sys.exit(app.exec_())