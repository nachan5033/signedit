from lxml import etree
from html.parser import HTMLParser
from json import JSONEncoder

from constants import Signtypes
from options import Options


def trim_command(command : str) -> str:
    '''
    Trim the command string so it will fit in command
    '''
    command = command.replace("'","\\'") # ' -> \'
    command = command.replace('"','\\\\"') # " -> \\"
    #command = command.replace('\\','\\\\"') #\ -> \\
    return command

def trim_text(text : str) -> str:
    '''
    Trim the text so it will fit in command
    '''
    text = text.replace('\\','\\\\') #\ -> \\\\
    text = text.replace("'","\\'")# ' -> \'
    text = text.replace('"','\\\\"')# " -> \\"

    return text

class MyHTMLParser(HTMLParser):
    tree : list #lines of a single face
    
    #current state of the text being processed
    current_color : str
    current_bold : bool
    current_italic : bool
    current_underline : bool
    current_strike : bool
    current_font : str
    
    current_line : list #a line in a single face
    in_content : bool #is here content? (rather than head)
    line_count: int #number of the current line
    
    commands : list #commands to be embedded in the json

    options : Options
    
    def reset_attr(self): #reset all attributes
        self.current_color = ''
        self.current_bold = False
        self.current_italic = False
        self.current_underline = False
        self.current_strike = False
        self.current_font = ''
    
    def __init__(self):
        super().__init__()
        self.tree = []
        self.reset_attr()
        self.line_count = 0
        self.commands = []
        
        self.in_content = False

    def trim_tree(self):
        '''
        Remove meaningless lists from tree
        '''
        try:
            if len(self.tree[0]) <= 0 and len(self.tree) <= 1: #only an empty line
                self.tree = []
        except:
            pass

    def parse(self, html : str):
        '''
        Parse html
        '''
        self.line_count = 0
        self.feed(html)
        self.trim_tree()

        if self.line_count < len(self.commands):
            #there are some command lines without text lines
            #so we will create empty text lines to embed commands
            for i in range(self.line_count, len(self.commands)):
                cmd = self.commands[i]
                if cmd != '': self.tree.append([{'command': cmd}])
    
    def set_command(self, commands : list):
        '''
        Set commands for the face
        :param commands: List of commands, one command per item
        '''
        self.commands = commands

    def set_options(self, options : Options):
        self.options = options

    def handle_starttag(self, tag, attrs):
        if tag == 'p': #start of a line     
            self.in_content = True #in content now, start processing data
            self.current_line = [] #create a new line
            
            #embed command
            if len(self.commands) > self.line_count: #there's a command to be embedded in this line
                cmd = self.commands[self.line_count]
                if cmd != '': # command makes sense
                    #cmd = trim_command(cmd)
                    self.current_line.append({'command' : cmd})
            
            self.tree.append(self.current_line) 
            self.reset_attr()
            self.line_count += 1
        
        if tag =='br': #nothing in this line
            pass
                
        if tag == 'span': #a text block with attributes
            if attrs == None:
                return
            for attr, value in attrs:
                #print('[%s]>%s'%(attr,value))
                if 'font-weight:600' in value:
                    self.current_bold = True
                if 'italic' in value:
                    self.current_italic = True
                if 'line-through' in value:
                    self.current_strike = True
                if 'underline' in value:
                    self.current_underline = True
                if 'color:#' in value:
                    pos = value.find('color:#')
                    self.current_color = value[pos + 6:pos +13]
                    #current_color should be like: #000000
                if 'font-family:' in value:
                    pos = value.find('font-family:')
                    pos += len('font-family:')
                    pos_end = value.find(';',pos)
                    font = value[pos:pos_end]

                    font = font.strip()
                    self.current_font = self.options.reverse_fontlist[font]
                    
    def handle_endtag(self, tag):
        self.reset_attr() #reset attributes after finishing processing the tag
    
    def handle_data(self, data):
        if self.in_content:
            if data != '\n' and data != '':#data makes sense
                text_part = {'text':data}
                if self.current_bold:
                    text_part['bold'] = True
                if self.current_italic:
                    text_part['italic'] = True
                if self.current_underline:
                    text_part['underline'] = True
                if self.current_strike:
                    text_part['strikethrough'] = True
                if self.current_color != '':
                    text_part['color']=self.current_color
                if self.current_font != '' and self.current_font != 'default':
                    text_part['font'] = self.current_font
                
                self.current_line.append(text_part)
                
    def result(self):
        return self.tree
    
    def clearHTML(self):
        self.tree.clear()
        self.reset_attr()
        self.in_content = False
        self.commands = []
        return super().reset()
    

def htmlToJsontext(htm: str):
    html = MyHTMLParser()
    html.feed(htm)
    print(html.tree)

def hasProperty(comp : dict,property : str):
    if property in comp.keys():
        if isinstance(comp[property],list):
            return len(comp[property]) > 0
        if isinstance(comp[property],dict):
            return not comp[property].isEmpty()
        return comp[property] != False and comp[property] is not None
    return False

def treeToJsonText120(tree : list | dict):
    '''
    Convert tree to jsontext
    Used in textdisplay
    '''
    i = 0
    result_commands = ''
    temp = "'[%s]'"
    if type(tree) == dict:
        tree = [tree]
    num_lines = len(tree)
    for i in range(num_lines):

        line = tree[i]
        if type(line) == dict:
            line = [line]
        line : list

        line_result ="%s"
        line_commands = ''
        comp_count = len(line) #num of parts in this line
        if comp_count == 0: #nothing in this line
            line_result = line_result%'""'
            result_commands += line_result
            if i < num_lines - 1: result_commands += ',"\\\\n",'#not the last line, append a line break
            continue
        for j in range(comp_count):
            comp_command = ''
            comp = line[j]
            comp : dict
            text = ''
            if 'text' in comp.keys():
                text = comp['text']
                text = trim_text(text)
            else:
                text = ''
            is_bold = hasProperty(comp, 'bold')
            is_italic = hasProperty(comp, 'italic')
            is_underline = hasProperty(comp, 'underline')
            is_strike = hasProperty(comp, 'strikethrough')
            is_color = hasProperty(comp, 'color')
            is_command = hasProperty(comp, 'command')
            is_font = hasProperty(comp, 'font')
            if not (is_bold or is_italic or is_underline or is_strike or is_color or is_command or is_font):
                #no property at all
                comp_command = '"%s"'
                comp_command = comp_command%trim_text(text)
                line_commands += comp_command
                if j < comp_count - 1: line_commands += ','  # not the last component
            else:
                if j == 0 and not is_command: #the first comp has some properties
                    line_commands += '"",'  #bug of MC
                comp_command = '{"text":"%s"' #no }
                comp_command = comp_command%trim_text(text)
                if is_bold: comp_command += ',"bold":true'
                if is_italic: comp_command += ',"italic":true'
                if is_underline: comp_command += ',"underlined":true'
                if is_strike: comp_command += ',"strikethrough":true'
                if is_color: comp_command += ',"color":"%s"'%comp['color']
                if is_font: comp_command += ',"font":"%s"'%comp['font']
                if is_command:
                    command_temp = ',"clickEvent":{"action":"run_command","value":"%s"}'
                    embedded_command = comp['command']
                    embedded_command = trim_command(embedded_command)
                    comp_command += command_temp %  embedded_command
                comp_command += '}'
                line_commands += comp_command
                if j < comp_count - 1: line_commands += ','  # not the last component
        line_result = line_result%line_commands
        result_commands += line_result
        if i < num_lines - 1: result_commands += ',"\\\\n",'#not the last line, append a line break
        continue
    return temp % result_commands

def treeToCommand120(tree : dict):
    #/give @a oak_sign{BlockEntityTag:{front_text:
    # {messages:['["test"]','[""]','[""]','[""]']}},
    # display:{Name:'["",{"text":"test","italic":false}]'}}

    def treeToFace120(tree : list):
        i = 0
        temp = '{messages:[%s]}'
        result_commands = ''
        for i in range(4):
            if i >= len(tree): #no more lines
                line_result = "'[\"\"]'"
                result_commands += line_result
                if i < 3: result_commands += ','  # not the last line, append a ',' to command
                continue
            line = tree[i]
            line : list
            if i >= 4: break
            line_result ="'[%s]'"
            line_commands = ''

            comp_count = len(line)
            if comp_count == 0: #nothing in this line
                line_result = line_result%'""'
                result_commands += line_result
                if i < 3: result_commands += ','#not the last line, append a ',' to command
                continue

            for j in range(comp_count):
                comp_command = ''
                comp = line[j]
                comp : dict
                text = ''
                if 'text' in comp.keys():
                    text = comp['text']
                    text = trim_text(text)
                else:
                    text = ''

                is_bold = hasProperty(comp, 'bold')
                is_italic = hasProperty(comp, 'italic')
                is_underline = hasProperty(comp, 'underline')
                is_strike = hasProperty(comp, 'strikethrough')
                is_color = hasProperty(comp, 'color')
                is_command = hasProperty(comp, 'command')
                is_font = hasProperty(comp, 'font')
                if not (is_bold or is_italic or is_underline or is_strike or is_color or is_command or is_font):
                    #no property at all
                    comp_command = '"%s"'
                    comp_command = comp_command%trim_text(text)
                    line_commands += comp_command
                    if j < comp_count - 1: line_commands += ','  # not the last component

                else:
                    if j == 0 and not is_command:
                        line_commands += '"",'  #bug of MC
                    comp_command = '{"text":"%s"' #no }
                    comp_command = comp_command%trim_text(text)
                    if is_bold: comp_command += ',"bold":true'
                    if is_italic: comp_command += ',"italic":true'
                    if is_underline: comp_command += ',"underlined":true'
                    if is_strike: comp_command += ',"strikethrough":true'
                    if is_color: comp_command += ',"color":"%s"'%comp['color']
                    if is_font: comp_command += ',"font":"%s"'%comp['font']
                    if is_command:
                        command_temp = ',"clickEvent":{"action":"run_command","value":"%s"}'
                        embedded_command = comp['command']
                        embedded_command = trim_command(embedded_command)
                        comp_command += command_temp %  embedded_command
                    comp_command += '}'
                    line_commands += comp_command
                    if j < comp_count - 1: line_commands += ','  # not the last component

            line_result = line_result%line_commands
            result_commands += line_result
            if i < 3: result_commands += ','  # not the last line, append a ',' to command
            continue
        return temp % result_commands

    commandbase = "/give @p %s{BlockEntityTag:{%s%s%s},display:{Name:'{\"text\":\"%s\"}'}}"
    name = 'sign'
    signtype = 'oak_sign'
    waxed = ''
    try:
        name = tree['name']
        signtype = tree['type']
    except:
        pass

    front_temp = ''
    back_temp = ''
    if hasProperty(tree, 'front_text'):
        front_temp = 'front_text:%s'
        front_command = treeToFace120(tree['front_text'])
        front_temp = front_temp % front_command
    if hasProperty(tree, 'back_text'):
        back_temp = 'back_text:%s'
        if hasProperty(tree, 'front_text'):#has both side
            back_temp = ',' + back_temp
        back_command = treeToFace120(tree['back_text'])
        back_temp = back_temp % back_command
    if hasProperty(tree, 'waxed'):
        waxed = 'is_waxed:1'
        if hasProperty(tree, 'front_text') or hasProperty(tree, 'back_text'):
            waxed = ',is_waxed:1'
    commandbase = commandbase%(signtype,front_temp,back_temp,waxed,name)
    return commandbase


    #front and back text

if __name__ == '__main__':
    parser = MyHTMLParser()
    lines = []
    htm = ''
    with open('debug.htm', 'r') as f:
        lines = f.readlines()

    for line in lines:
        htm += line
    parser.feed(htm)
    tree = parser.tree
    t = treeToJsonText120(tree)
    print(t)