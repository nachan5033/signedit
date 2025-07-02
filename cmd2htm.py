#for version 1.16.5

import json
from mcedit import *

class NBT:  
    def __init__(self,nbt = '',tokens = [],fieldtype = 'block'):
        self.tags = dict()
        self.fields = [] #for fieldtype list
        self.fieldtype = fieldtype
        self.index = 0
        if tokens != []:
            self.buildTreeFromTokens(tokens)
        else:
            t = self.parseTokens(nbt)
            self.buildTreeFromTokens(t)
    
    def toStr(self,depth) -> str:
        result = ''
        if self.fieldtype == 'block':
            for n in self.fields:
                result += '\n'
                result += '\t'*depth + '{\n'
                result += n.toStr(depth + 1)
                result += '\n'
                result += '\t'*depth + '}\n'
        if self.fieldtype == 'array':
            for n in self.fields:
                result += '\n'
                result += '\t'*depth + '[\n'
                if type(n) == type(self):
                    result += n.toStr(depth + 1)
                else:
                    result += ('\t'*depth + f'{n}')
                result += '\n'
                result += '\t'*depth + ']'
                result += '\n'
        for k in self.tags.keys():
            v = self.tags[k]
            result += '\t'*depth
            if type(v) == str:
                result += (k + ': ' + '"' +v + '"\n')
            else:
                result += (k +':\n' + '\t'*depth + '{\n' + v.toStr(depth + 1) + '\t'*depth + '}')
        return result

    def __repr__(self) -> str:
        return self.toStr(0)
    def __str__(self) -> str:
        return self.__repr__()
    def __getitem__(self,index):
        if type(index) == type(''):
            return self.tags[index]
        else:
            return self.fields[index]
    
        
    def parseTokens(self,nbt:str) -> list:
        tokens = []

        i = 0 #token start pointer
        j = 0 #token end pointer
        strmode = False
        quotestr = '\'' #start of quote, can be ' or "
        str_tmp = ''

        for j in range(len(nbt)):
            if strmode:#string mode
                if nbt[j] == '\\':
                    pass
                if nbt[j] == '\'':
                    if nbt[j-1] != '\\': # not \', exit string mode
                        tokens.append('@' + nbt[i:j])#@: string indicator
                        i = j+1
                        strmode = False
                continue

            if nbt[j] == ':': # : token
                if i < j:# some token already scanned
                    tokens.append(nbt[i:j])
                tokens.append(':')
                i = j + 1

            if nbt[j] == '{': # { token
                if i < j:# some token already scanned
                    tokens.append(nbt[i:j])
                tokens.append('{')
                i = j + 1
            if nbt[j] == '}': # } token
                if i < j:# some token already scanned
                    tokens.append(nbt[i:j])
                tokens.append('}')
                i = j + 1
            if nbt[j] == '[': # [] token
                if i < j:# some token already scanned
                    tokens.append(nbt[i:j])
                tokens.append('[')
                i = j + 1
            if nbt[j] == ']': # ] token
                if i < j:# some token already scanned
                    tokens.append(nbt[i:j])
                tokens.append(']')
                i = j + 1
            
            if nbt[j] == ',': # , token
                if i < j:# some token already scanned
                    tokens.append(nbt[i:j])
                tokens.append(',')
                i = j + 1
            if nbt[j]== ' ' or nbt[j] == '\t':
                if i < j:#some token already scanned
                    tokens.append(nbt[i:j])
                    i = j + 1
                else:
                    i = j + 1#skip extra spaces
            if nbt[j] =='\n':#skip line feed
                if i < j:#some token already scanned
                    tokens.append(nbt[i:j])
                i = j + 1

            if nbt[j] == '\'': #start string mode
                strmode = True
                i  = j + 1


        if i < j:#scan last token
            tokens.append(nbt[i:j+1])

        return tokens
    
    def buildTreeFromTokens(self,tokens) -> int:
        t = 0
        while t < len(tokens):
            if tokens[t] == ',':
                t += 1
                continue
            if tokens[t] == '}':#nbt sub field end
                self.index = t
                return t
            if tokens[t] == '{':#nbt sub field start:
                n = NBT(tokens=tokens[t+1:],fieldtype='block')
                self.fields.append(n)
                t += (n.index + 3)
                continue
            if tokens[t] == ']':#nbt array end
                self.index = t
                return t

            if not tokens[t].startswith('@') and t+1 < len(tokens) and tokens[t+1] ==':': #tagged element
                if tokens[t + 2].startswith('@'):
                    self.tags[tokens[t]] = tokens[t+2][1:]#remove @ in the beginning of str
                    t += 2 #skip ':'
                    continue
                if tokens[t + 2].startswith('{'):#subfield
                    t += 3 #skip ':' and '{'
                    n = NBT(tokens=tokens[t:],fieldtype='block')
                    self.tags[tokens[t-3]] = n
                    t += (n.index+1)
                    continue

                if tokens[t + 2].startswith('['):#array
                    t += 3
                    n = NBT(tokens=tokens[t:],fieldtype='array')
                    self.tags[tokens[t-3]] = n
                    t += (n.index+1)
                    continue
                    
                else:
                    self.tags[tokens[t]] = tokens[t+2]
                    t += 2 #skip ':' and the tag
                    continue
            else:
                if tokens[t].startswith('@'):
                    tokens[t] = tokens[t][1:]
                self.fields.append(tokens[t])
                t += 1
        return t


def htm(attr : str,color : str,content : str):
    '''
    Generate html via text and attributes
    attr: attributes, split by space
    color: minecraft color code
    '''
    result = content
    result = result.replace('<','&#60;')
    result = result.replace('>','&#62;')

    types = attr.split(' ')
    if 'bold' in types:
        result = '<b>' + result + '</b>'
    if 'it' in types:
        result = '<i>' + result + '</i>'
    if 'del' in types:
        result = '<s>' + result + '</s>'
    if 'u' in types:
        result = '<u>' + result + '</u>'
    if color != '':
        result = f'<span style=\"color:{color}\">' + result + '</span>'
    return result

def parseJsonText(text : str) -> tuple[str,str]:
    jsonstr = text
    if  text.startswith('\''):
        jsonstr = jsonstr[1:] #remove ' from start and end
    if  text.endswith('\''):
        jsonstr = jsonstr[:-1] 
    
    jsonstr = str.replace(jsonstr,'\\\\\"','&#34')#replace \\" with &quot to parse command
    jsonstr = str.replace(jsonstr,'\\\'','&#39')#replace \' with &apos to parse command
    result = ''
    command = ''
    

    j = json.loads(jsonstr)
    if type(j) == type([]):
        for s in j:
            part_text = ''
            part_attr = ''
            part_color = ''
            if 'text' in s:
                part_text = s['text']
                part_text = part_text.replace('\\u','\\&#x')

            if 'bold' in s and s['bold'] == True:
                part_attr += ' bold'
            if 'italic' in s and s['italic'] == True:
                part_attr += ' it'
            if 'underlined' in s and s['underlined'] == True:
                part_attr += ' u'
            if 'strikethrough' in s and s['strikethrough'] == True:
                part_attr += ' del'

            if 'color' in s:
                part_color = s['color']

            try: #parse command
                if command == '':
                    command = s['clickEvent']['value']
            except:
                pass
            result += htm(part_attr,part_color,part_text)
        command = str.replace(command,'&#34','\"')
        command = str.replace(command,'&#39','\'')
            
    else: #a single dict
        k = j.keys()
        part_text = ''
        part_attr = ''
        part_color = ''
        if 'text' in k:
            part_text = j['text']
            part_text = part_text.replace('\\u','&#x')
        if 'bold' in k and j['bold'] == True:
            part_attr += ' bold'
        if 'italic' in k and j['italic'] == True:
            part_attr += ' it'
        if 'underlined' in k and j['underlined'] == True:
            part_attr += ' u'
        if 'strikethrough' in k and j['strikethrough'] == True:
            part_attr += ' del'
        if 'color' in k:
            part_color = j['color']
        try: #parse command
            if command == '':
                command = j['clickEvent']['value']
        except:
            pass
        command = str.replace(command,'&#34','\"')
        command = str.replace(command,'&#39','\'')

        result = htm(part_attr,part_color,part_text)
    return result,command

def parseNBT(cmd:str) -> Sign:
    '''
    parse NBT part of a command
    @param cmd: NBT parts e.g. {front_text:...}
    @return: Sign object
    '''
    n = NBT(cmd)


def parseCommand(cmd : str) ->tuple[str,tuple[str,list],tuple[str,list]]:
    '''
    parse give command
    returns:
    html, type of sign, cmd1, cmd2, cmd3, cmd4
    '''
    if cmd.startswith('/'):
        cmd = cmd[1:]

    i = cmd.find('give')
    if i == -1 : raise ValueError('Wrong command: no /give')
    cmd = cmd[i + 4:]

    i = cmd.find('minecraft')
    if i == -1 : raise ValueError('Wrong command: no sign type')
    j = cmd.find('{')
    signtype = cmd[i:j]
    cmd = cmd[j:]

    i = cmd.find('BlockEntityTag:')
    if i == -1 : raise ValueError('Wrong command: no BlockEntityTag')
    cmd = cmd[i:]

    i = cmd.find('{')
    if i == -1 : raise ValueError('Wrong command')

    nbt = cmd[i:-1]
    n = NBT(nbt)

    cmd_list1 = ''
    cmd_list2 = ''
    html1 = ''
    html2 = ''
    html1,cmd_list1 = parseCommand_singleface('front_text',n[0])
    html2,cmd_list2 = parseCommand_singleface('back_text',n[0])

    if signtype.startswith('minecraft:'):
        signtype = signtype[len('minecraft:'):]
    return signtype,(html1,cmd_list1),(html2,cmd_list2)

def parseCommand_singleface(face : str,nbt: NBT) -> tuple[str,str]:
    if face in nbt.tags.keys():
        t1 = ''
        t2 = ''
        t3 = ''
        t4 = ''
        try:
            t1 = nbt[face]['messages'][0]
            t2 = nbt[face]['messages'][1]
            t3 = nbt[face]['messages'][2]
            t4 = nbt[face]['messages'][3]
        except:
            pass
        h1, cmd1 = parseJsonText(t1) 
        h2, cmd2 = parseJsonText(t2) 
        h3, cmd3 = parseJsonText(t3) 
        h4, cmd4 = parseJsonText(t4) 

        #h = h1 + '<br/>' + h2 + '<br/>' + h3 + '<br/>' + h4
        #print("H1:%s" % h1)
        #print("H2:%s" % h2)
        h = """<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">%s</p>
        <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">%s</p>
        <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">%s</p>
        <p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">%s</p>""" % (h1, h2, h3, h4)
        return h,cmd1 + '\n' + cmd2 + '\n' + cmd3 +'\n' +  cmd4
    else:
        return '',''

def loadFromCommand(command : str) ->tuple[str,str,list[str],list[str]]:
    '''
    Load HTML from command
    @param command: command to load, in any versions
    @return:
        HTML on front and back, [commands] on front and back
    '''
    #if cmd.startswith('/'):
    #    cmd = cmd[1:]

def main():
    s = '''/give @p minecraft:cherry_hanging_sign{BlockEntityTag:{front_text:{messages:['[{"text":"","clickEvent":{"action":"run_command","value":"/a"}},{"text":""},{"text":"Test 1', '2???', '3"},{"text":"","clickEvent":{"action":"run_command","value":"/a"}}]','[,{"text":"???","italic":true,"bold":true,"color":"#bfff00"},{"text":"4???"},{"text":"","clickEvent":{"action":"run_command","value":"/b"}}]','[]','{"text":"","clickEvent":{"action":"run_command","value":"/d"}}']},back_text:{messages:['[{"text":"","clickEvent":{"action":"run_command","value":"/a"}},{"text":""},{"text":"Test 1', '2???', '3"},{"text":"","clickEvent":{"action":"run_command","value":"/a"}}]','[,{"text":"???","italic":true,"bold":true,"color":"#bfff00"},{"text":"4???"},{"text":"","clickEvent":{"action":"run_command","value":"/b"}}]','[]','{"text":"","clickEvent":{"action":"run_command","value":"/d"}}']}},display:{Name:'{"text":"Custom Sign"}'}}'''

    n = '''{front_text:{messages:['[{"text":"","clickEvent":{"action":"run_command","value":"/1"}},"test"]','[{"text":"","clickEvent":{"action":"run_command","value":"/2"}},"test"]','["test"]','[""]']}}'''

    n = NBT(n)
    print(n)

def rawJson2Htm_singleface(face : list, sign : Sign):
    for line in face:
        for item in line:
            cmd = ''
            bold = False
            italic = False
            strike = False
            underline = False
            color = ''
            text = ''

            try:
                text = item['text']
            except:
                pass


def rawJson2Htm(raw : str) -> Sign:
    j = json.loads(raw)
    sign = Sign()
    if 'front_text' in j.keys():
        pass

if __name__ == '__main__':
    main()