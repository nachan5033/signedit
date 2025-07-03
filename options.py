from PyQt5.QtGui import QFontDatabase
import json

def families_str(families: list[str]) -> str:
    '''
    Compose font families str
    '''
    s = ("'%s'")%families[0].strip()
    for family in families[1:]:
        s += (",'%s'")%family.strip()
    return s

class Options:
    def __init__(self):
        self.fontlist = {} # {minecraft font name : actual font name}
        self.reverse_fontlist = {} # {actual font name : minecraft font name}
        self.default_version = ''

    def loadoptions(self, path = './settings.json'):
        self.fontlist = {'default' : ['mcprev', 'unimc'],}
        self.reverse_fontlist = {"'mcprev','unimc'": 'default' }

        with open(path, 'r', encoding='utf-8') as f:
            opt = json.load(f)

            #load fonts
            fonts = opt['fonts']
            for font in fonts:
                try:
                    name = font['name']
                    family = font['family']

                    families = family.split(',')
                    for i in range(len(families)):
                        families[i] = families[i].strip()
                        #self.reverse_fontlist[families[i]] = name

                    self.reverse_fontlist[families_str(families)] = name
                    self.fontlist[name] = families
                except:
                    pass

            #load extra fonts
            extra_fonts = opt['extra_fonts']
            for i in extra_fonts:
                r = QFontDatabase.addApplicationFont(i)
                if r == -1:
                    print('Unable to load font: ' + i)
                else:
                    s = QFontDatabase.applicationFontFamilies(r)
                    print('Font family added:',end='')
                    for family in s:
                        print(' %s'%family,end='')
                    print('')

            #load default version
            self.default_version = opt['default_version']

            #load picture info
            self.max_pic_height = opt["max_pic_height"]
            self.max_pic_width  = opt["max_pic_width"]
            self.default_pic_path = opt["default_pic_path"]

global_options = Options()