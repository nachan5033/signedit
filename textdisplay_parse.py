import math

from parse import *
from mcedit import *
import numpy as np
import math

def fequ(a,b,prec = 0.001):
    return abs(a - b) < prec

def arc2deg(arc : float):
    return arc * 180 / math.pi

def toMCCoord(n : tuple[float,float,float], offset : tuple[float,float,float],
              origin : tuple[float,float,float] | None = None,
              origin_offset = (0.0,0.0,0.0)) -> tuple[str,float,float]:
    """
    Convert relative coordinates to minecraft coordinates
    :param n: normal vector of the text face(in mc coordinates)
    :param offset: offset vector of the text to the face (in face coordinates)
    :param origin_offset: origin vector of the origin to command origin (in mc coordinates)
    :param origin: origin of the entity in the world (set it None to use relative coordinates)

    :return string of the position of the entity, rotation y, pitch
    """
    n = np.array(n)
    offset = np.array(offset)
    origin = np.array(origin)

    n = n / np.linalg.norm(n)

    #rotation y: rotation angle around Y (clockwise from above)
    #pitch: rotation angle around XZ face (clockwise when looking at X direction)
    #default normal vector is (0,0,1)

    yr = np.arcsin(-n[0] / np.sqrt(1-n[1]**2))
    xr = np.arcsin(n[1])




class TextDisplayDoc(Document):
    def __init__(self):
        self.html = ''
        self.position = '~ ~5 ~'
        self.brightness = (15,15)#sky, block
        self.glow = False #auto lighting calc
        self.shadow = False
        self.align = 'center' #left, right and center
        self.scale = (1.0,1.0)

        self.billboard = 'fixed' #fixed, vertical, horizontal, center
        self.right_rotation = (0.0,0.0,0.0,1.0)
        self.left_rotation = (0.0,0.0,0.0,1.0)
        self.rotation = (0.0,0.0)
        self.translation = (0.0,0.0,0.0)
        self.opacity = -1

        self.background = (0,0,0,0xff) #RGBA
        self.use_background = False

        self.name = 'text display'
        self.type = 'oak_sign'
        self.options = Options()

        self.parser = MyHTMLParser()

    def genSummonCommand120_caching(self, text_str : str):
        command_base = ('summon minecraft:text_display %s {%s transformation:{left_rotation:'
                        '%s, right_rotation:%s, translation:%s, scale:%s} '
                        ',text:%s, background:%d,shadow:%s, %s Rotation:%s, alignment:%s}')

        brightness_str = ''
        billboard_str = ''
        shadow_str = ''
        background = 0  # no background
        lr_str = '[%2.2ff,%2.2ff,%2.2ff,%2.2ff]' % self.left_rotation
        rr_str = '[%2.2ff,%2.2ff,%2.2ff,%2.2ff]' % self.right_rotation
        tr_str = '[%2.2ff,%2.2ff,%2.2ff]' % self.translation
        rot_str = '[%2.2ff,%2.2ff]' % self.rotation
        sca_str = '[%2.2ff,%2.2ff,1f]' % self.scale
        if self.glow:
            brightness_str = 'brightness:{sky:%d,block:%d},' % self.brightness
        if self.billboard != 'fixed':
            billboard_str = 'billboard:%s,' % self.billboard
        if self.use_background:
            # convert RGBA to ARGB
            R, G, B, A = self.background
            background = (A << 24) + (R << 16) + (G << 8) + B
            if background > 0x80000000:
                background = background - 0xffffffff
        if self.shadow:
            shadow_str = 'true'
        else:
            shadow_str = 'false'
        return command_base%(self.position,billboard_str,lr_str,rr_str,tr_str,sca_str,
                             text_str,background,shadow_str,brightness_str,rot_str,self.align)

    def genSummonCommand120(self):
        command_base = ('summon minecraft:text_display %s {%s transformation:{left_rotation:'
                        '%s, right_rotation:%s, translation:%s, scale:%s} '
                        ',text:%s, background:%d,shadow:%s, %s Rotation:%s, alignment:%s}')

        #generate Json text
        self.parser.parse(self.html)
        tree = self.parser.tree
        text_str = treeToJsonText120(tree)
        self.parser.clearHTML()

        return self.genSummonCommand120_caching(text_str)


    def genWallSign120(self, offset = 0.01,y_offset = 0.0,y_cali = False,
                    protect_mode = True):
        """
        Generate give command of a wall mode sign
        :param html: HTML content of text display entity
        :param offset: depth offset of the text to the block
        :param y_offset: vertical offset of the text to the block
        :param y_cali: whether to calibrate the vertical offset (default font only)
        :param protect_mode: whether to prevent the sign from creating multiple entities
        """

        sign = Sign()
        sign.name = self.name
        sign.type = self.type

        sign.options = self.options

        type = sign.type.replace('_hanging_sign','')
        type = type.replace('_sign','')

        type += '_wall_sign'

        protect_str = ''
        if protect_mode:
            protect_str = ' unless entity @e[type=text_display,distance=..0.2]'

        #tips
        tip_htm = '<p>Place it on walls</p><p>Click to put text</p>'
        brightness_tip = '<p>Ambient light</p>'
        if self.glow:
            brightness_tip = '<p>Light s:%d b:%d </p>'%self.brightness

        #generate JsonText
        self.parser.parse(self.html)
        tree = self.parser.tree
        text_str = treeToJsonText120(tree)

        preview_html = ''
        #preview
        if len(tree) > 0:
            preview_html,cmd = loadFromTree([tree[0]])

        sign.front_HTML = tip_htm + brightness_tip + preview_html


        #calibrate
        if y_cali:
            #calibrate method:
            #height of a character is 8px (default font)
            #spacing between lines is 2px (default font, equals to 4px in unifont)
            #about 40px / block (scale = 1)
            num_lines = len(tree)
            height = num_lines*10
            height *= self.scale[1]
            y_offset = (-height / 2) / 40

        self.parser.clearHTML()
        y_str = '~'
        if not fequ(y_offset,0):
            y_str = '~%2.2f' % y_offset

        self.position = '~ ~ ~'
        #facing north
        z_off = 0.5 - offset
        pos = '~ %s ~%2.2f'%(y_str,z_off)
        self.rotation = (180,0)
        cmd_north = self.genSummonCommand120_caching(text_str)
        cmd_north = f'execute if block ~ ~ ~ {type}[facing=north] positioned {pos}{protect_str} run {cmd_north}'

        #facing south
        z_off = -0.5 + offset
        pos = '~ %s ~%2.2f'%(y_str,z_off)
        self.rotation = (0,0)
        cmd_south = self.genSummonCommand120_caching(text_str)
        cmd_south = f'execute if block ~ ~ ~ {type}[facing=south] positioned {pos}{protect_str} run {cmd_south}'

        #facing east
        x_off = -0.5 + offset
        pos = '~%2.2f %s ~'%(x_off, y_str)
        self.rotation = (270,0)
        cmd_east = self.genSummonCommand120_caching(text_str)
        cmd_east = f'execute if block ~ ~ ~ {type}[facing=east] positioned {pos}{protect_str} run {cmd_east}'

        #facing west
        x_off = 0.5 - offset
        pos = '~%2.2f %s ~'%(x_off,y_str)
        self.rotation = (90,0)
        cmd_west = self.genSummonCommand120_caching(text_str)
        cmd_west = f'execute if block ~ ~ ~ {type}[facing=west] positioned {pos}{protect_str} run {cmd_west}'

        sign.front_commands = [cmd_north, cmd_south, cmd_east, cmd_west]

        return sign.getCommand120(Facemodes.FRONT)

    def genGroundSign120(self, offset = 0.01,y_offset = 0.0,y_cali = False,
                      protect_mode = True):
        '''
        Generate give command of a ground mode sign
        '''

        sign = Sign()
        sign.name = self.name
        sign.type = self.type

        sign.options = self.options

        type = sign.type.replace('_hanging_sign', '')
        type = type.replace('_sign', '')

        type += '_sign'

        protect_str = ''
        if protect_mode:
            protect_str = ' unless entity @e[type=text_display,distance=..0.2]'

        # tips
        tip_htm = '<p>Place on ground</p><p>Click to put text</p>'
        brightness_tip = '<p>Ambient light</p>'
        if self.glow:
            brightness_tip = '<p>Light s:%d b:%d </p>' % self.brightness

        # generate JsonText
        self.parser.parse(self.html)
        tree = self.parser.tree
        text_str = treeToJsonText120(tree)

        preview_html = ''
        # preview
        if len(tree) > 0:
            preview_html,cmd = loadFromTree([tree[0]])

        sign.front_HTML = tip_htm + brightness_tip + preview_html

        # calibrate
        if y_cali:
            # calibrate method:
            # height of a character is 8px (default font)
            # spacing between lines is 2px (default font, equals to 4px in unifont)
            # about 40px / block (scale = 1)
            num_lines = len(tree)
            height = num_lines * 10
            height *= self.scale[1]
            y_offset = (-height / 2) / 40


        self.parser.clearHTML()
        cali_str = '~'
        y_off = -0.5 + offset
        self.position = '~ ~ ~'
        # pointing to north
        if not fequ(y_offset, 0):
            cali_str = '~%2.2f' % -y_offset

        pos = '~ ~%2.2f %s' % (y_off,cali_str)
        self.rotation = (0, 270)
        cmd_north = self.genSummonCommand120_caching(text_str)
        cmd_north = f'execute if block ~ ~ ~ {type}[rotation=0] positioned {pos}{protect_str} run {cmd_north}'

        # pointing to south
        if not fequ(y_offset, 0):
            cali_str = '~%2.2f' % y_offset
        pos = '~ ~%2.2f %s' % (y_off,cali_str)
        self.rotation = (180, 270)
        cmd_south = self.genSummonCommand120_caching(text_str)
        cmd_south = f'execute if block ~ ~ ~ {type}[rotation=8] positioned {pos}{protect_str} run {cmd_south}'

        # pointing to east
        if not fequ(y_offset, 0):
            cali_str = '~%2.2f' % y_offset
        pos = '%s ~%2.2f ~' % (cali_str,y_off)
        self.rotation = (90, 270)
        cmd_east = self.genSummonCommand120_caching(text_str)
        cmd_east = f'execute if block ~ ~ ~ {type}[rotation=4] positioned {pos}{protect_str} run {cmd_east}'

        # pointing to west
        if not fequ(y_offset, 0):
            cali_str = '~%2.2f' % -y_offset
        pos = '%s ~%2.2f ~' % (cali_str,y_off)
        self.rotation = (270, 270)
        cmd_west = self.genSummonCommand120_caching(text_str)
        cmd_west = f'execute if block ~ ~ ~ {type}[rotation=12] positioned {pos}{protect_str} run {cmd_west}'

        sign.front_commands = [cmd_north, cmd_south, cmd_east, cmd_west]


        return sign.getCommand120(Facemodes.FRONT)