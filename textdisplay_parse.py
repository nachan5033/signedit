from parse import *
from mcedit import *

class TextDisplayDoc(Document):
    def __init__(self):
        self.html = ''
        self.position = (0.0,0.0,0.0)
        self.background = False
        self.glow = True
        self.shadow = False
        self.align = 'center' #left, right and center
        self.scale = (1.0,1.0)

        self.billboard = 'fixed' #fixed, vertical, horizontal, center
        self.right_rotation = (0.0,0.0,0.0,0.0)
        self.left_rotation = (0.0,0.0,0.0,0.0)
        self.translation = (0.0,0.0,0.0)
        self.opacity = -1

        self.background = (0,0,0,0)
        self.use_background = False

def genWallSign(html : str,):
    pass