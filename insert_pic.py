import sys
import platform

from constants import *
from signpic import analyzeImage, openImage

from PyQt5.QtWidgets import*
from PyQt5.QtCore import Qt,QSize
from PyQt5.QtGui  import QIcon,QFont
from options import *

class PicInsert(QWidget):

    def __init__(self, parent = None, path = ""):
        global qApp
        self.opt : Options = Options()
        self.opt.loadoptions()
        super().__init__()
        self.parent_window = parent
        self.html = ''
        self.image = None
        self.image_width = -1
        self.image_height = -1
        self.initUI(path)
        self.setGeometry(300, 300, 640, 480)
        self.setWindowTitle('Insert')   

    def initUI(self, default_path : str):
        global point_size
        layout = QVBoxLayout()

        #Open file
        file_layout = QHBoxLayout()
        file_Widget = QWidget()

        self.file_path = QLineEdit()
        if default_path == '':
            self.file_path.setText(self.opt.default_pic_path)
        else:
            self.file_path.setText(default_path)
        self.file_path.setMinimumWidth(300)
        self.img_browse= QToolButton()
        self.img_browse.setCheckable(False)
        action = QAction()
        action.setIcon(QIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton)))
        action.triggered.connect(self.onFileOpen)
        self.img_browse.setDefaultAction(action)
        self.info_label = QLabel()
        self.info_label.setText("")
        self.info_label.setStyleSheet("color:red;")
        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(self.onLoadClick)

        file_layout.addWidget(QLabel("Image File:"))
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(self.img_browse)
        file_layout.addWidget(self.info_label)
        file_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        file_layout.addWidget(self.load_button)

        file_Widget.setLayout(file_layout)

        #Tools
        tool_layout = QHBoxLayout()
        tool_Widget = QWidget()
        
        self.pixel_mode_1 = QRadioButton("\u2b1b")
        self.pixel_mode_2 = QRadioButton("▌")
        self.pixel_mode_1.toggled.connect(self.onPixelModeChange)
        self.pixel_mode_2.toggled.connect(self.onPixelModeChange)

        self.resize_width = QLineEdit()
        self.resize_width.textEdited.connect(self.onResizeChange)
        self.resize_height = QLineEdit()
        self.resize_height.textEdited.connect(self.onResizeChange)
        self.keep_ratio = QCheckBox("Keep Ratio")
        self.keep_ratio.toggled.connect(self.onResizeChange)

        self.crop_width = QLineEdit()
        self.crop_width.textEdited.connect(self.loadImage)
        self.crop_height = QLineEdit()
        self.crop_height.textEdited.connect(self.loadImage)

        tool_layout.addWidget(QLabel("Pixel Mode"))
        tool_layout.addWidget(self.pixel_mode_1)
        tool_layout.addWidget(self.pixel_mode_2)
        self.pixel_mode_2.setChecked(True)
        tool_layout.addWidget(QLabel("Resize to"))
        tool_layout.addWidget(self.resize_width)
        tool_layout.addWidget(QLabel('x'))
        tool_layout.addWidget(self.resize_height)
        tool_layout.addWidget(self.keep_ratio)
        tool_layout.addSpacing(80)
        tool_layout.addWidget(QLabel("Crop to"))
        tool_layout.addWidget(self.crop_width)
        tool_layout.addWidget(QLabel("x"))
        tool_layout.addWidget(self.crop_height)
        tool_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        tool_Widget.setLayout(tool_layout)

        #Preview
        self.preview_layout = QGridLayout()

        self.preview = QLabel("Preview")
        sheet = """QLabel{       
                                      font-size: %dpx; 
                                      font-family: 'mcprev','unimc';
                                      padding: 0;
                                      margin-bottom: 0px;
                                      background: url("./src/oak.png") repeat top center;
                                      }""" % point_size
        self.preview.setStyleSheet(sheet)
        self.preview.setMinimumHeight(300)
        self.preview.setAlignment(Qt.AlignCenter)

        self.insert_image = QPushButton("Insert Image")
        self.insert_image.clicked.connect(self.onInsertClicked)
        self.cancel = QPushButton("Cancel")
        self.cancel.clicked.connect(self.close)

        done_layout = QHBoxLayout()
        done_widget = QWidget()

        done_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        done_layout.addWidget(self.insert_image)
        done_layout.addWidget(self.cancel)
        done_widget.setLayout(done_layout)

        layout.addWidget(file_Widget)
        layout.addWidget(tool_Widget)
        layout.addWidget(self.preview)
        layout.addWidget(done_widget)

        self.setLayout(layout)

    def onFileOpen(self, e):
        filename = QFileDialog.getOpenFileName(self,"Open Image",filter="Image files(*.jpg *.png *.gif *.jpeg *.bmp);;All files(*.*)")
        if len(filename) > 0:
            self.file_path.setText(filename[0])
            self.onLoadClick(None)
    
    def onLoadClick(self, e):
        path = self.file_path.text()
        img = openImage(path)
        
        if img is None: #image not found
            self.info_label.setText("Image not found.")
            return
        
        self.html = analyzeImage(img)
        self.info_label.setText("")
        width = img.size[0]
        height = img.size[1]

        self.resize_width.setText(str(width))
        self.resize_height.setText(str(height))
        self.image = img
        self.image_width = width
        self.image_height = height

        self.loadImage()

    def loadImage(self):
        global point_size
        if self.image is None:
            return

        resize = None
        crop = None
        final_height = self.image_height
        final_width = self.image_width
        if self.resize_width.text().isnumeric() and self.resize_height.text().isnumeric():
            resize_width = int(self.resize_width.text())
            resize_height = int(self.resize_height.text())
            if resize_width > 0 and resize_height > 0:
                resize = (resize_width, resize_height)
                final_width = resize_width
                final_height = resize_height

        if self.crop_width.text().isnumeric() and self.crop_height.text().isnumeric():
            crop_width = int(self.crop_width.text())
            crop_height = int(self.crop_height.text())
            crop_width = min(crop_width, self.image_width)
            crop_height = min(crop_height, self.image_height)
            if crop_width > 0 and crop_height > 0:
                crop = (0, 0, crop_width, crop_height)
                final_height = crop_height
                final_width = crop_width
        
        if final_width > self.opt.max_pic_width:
            final_width = self.opt.max_pic_width
            self.info_label.setText("Image size exceed")
            crop = (final_width, final_height)
        if final_height > self.opt.max_pic_height:
            final_height = self.opt.max_pic_height
            self.info_label.setText("Image size exceed")
            crop = (final_width, final_height)
        
        self.html = analyzeImage(self.image, resize, crop)
        if self.pixel_mode_1.isChecked():
            pixel = "\u2b1b"
        else:
            pixel = "▌"
        
        show_text = self.html.replace("$", pixel)

        #Choose a proper font size
        if final_height <= 7:
            show_text = show_text.replace("#POINT_SIZE", str(point_size))
        else:
            show_text = show_text.replace("#POINT_SIZE", str(point_size >> 1))
        self.preview.setText(show_text)
    
    def onPixelModeChange(self, e):
        if self.sender().isChecked():
            self.loadImage()

    def onResizeChange(self, e):
        if self.image is not None and self.keep_ratio.isChecked():
            if self.sender() == self.resize_width and self.resize_width.text().isnumeric():
                width = int(self.resize_width.text())
                supposed_height = int((self.image_height/self.image_width)*width + 0.5)
                self.resize_height.setText(str(supposed_height))
            elif self.resize_height.text().isnumeric():
                height = int(self.resize_height.text())
                supposed_width = int((self.image_width/self.image_height)*height + 0.5)
                self.resize_width.setText(str(supposed_width))

        
        self.loadImage()

    def onInsertClicked(self, e):
        global point_size
        if self.html != '':
            if self.pixel_mode_1.isChecked():
                pixel = "\u2b1b"
            else:
                pixel = "▌"
            result = self.html.replace('$', pixel).replace('#POINT_SIZE', str(point_size))
            self.parent_window.currentEditPanel().currentEditor().setHtml(result)
        self.close()

class old_PicInsert(QWidget):
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