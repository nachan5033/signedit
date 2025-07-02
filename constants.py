import platform
from enum import Enum

#colors
colors = ["#000000","#FF0000","#00FF00","#8B4513","#0000FF","#A020F0","#00FFFF","#D3D3D3","#808080","#FF69B4","#BFFF00","#FFFF00","#9AC0CD","#FF00FF","#FF681F","#FFFFFF"]
desp   = ["black","red","green","brown","blue","purple","aqua","light gray","gray","pink","lime","yellow","light blue","magenta","orange","white"]

#sign types
types = ["oak","oak_hanging","spruce","spruce_hanging","birch","birch_hanging","jungle","jungle_hanging","acacia","acacia_hanging",
         "dark_oak","dark_oak_hanging","mangrove","mangrove_hanging","cherry","cherry_hanging","bamboo","bamboo_hanging",
         "crimson","crimson_hanging","warped","warped_hanging"]
names = ["Oak","Oak Hanging","Spruce","Spruce Hanging","Birch","Birch Hanging","Jungle","Jungle Hanging",
         "Acacia","Acacia Hanging","Dark Oak","Dark Oak Hanging","Mangrove","Mangrove Hanging","Cherry","Cherry Hanging",
         "Bamboo","Bamboo Hanging","Crimson","Crimson Hanging","Warped","Warped Hanging"]

#chars
emoji_type_list = ['Humans','Animals','Plants','Foodstuff','Travel','Weather','Activities','Objects','Symbols','Computers']
char_type_list = ['Alphabets','Notations','Arrows','Mathematics','Shapes','CJK','Games']
type_list = [emoji_type_list,char_type_list]

emoji_list = []
char_list = []

special_char_list=[emoji_list,char_list]

emoji_icon = '👤🐂🌿🍰🚆🌧⚽💡★💻'
char_icon = 'A¶→√▉漢🃏'
icon_list = [emoji_icon,char_icon]

#special_chars = ["☚☛☜☝☞☟⇨↔↕↑↓→←↘↙⋮⋯⋰⋱❤❥♥♠♤♣♧★☆✦▅▆▇▌▐█▓▒░✚▣▧▨▤▥▦▩▲△▼♢♦▽Δ►◄◈◆◇◊◯●◕◐◑○◔⊙◎◘◙⁎⁑⁂⬖⬗⬘⬙⬟⬠⬡⬢⬣⬤╳▚▞◧◨◩◪",  #Shapes
#                 "㊚㊛㊣➀➁➂➃➄➅➆➇➈➉ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹⅺⅻ￡№¿½⅓⅔¼¾⅛⅜⅝⅞℅∆∇〰〽√∞",    #Special  chars
#                 "☹☻☺ツ✍✎✌❤❥♥♡♨☠☮☯☪☀☣☢☭☂☔☃☁☼☽☾❄♔♕♚۩♛✿❀❃❂❁♠♤♣♧⚜™®©₪★☆✮✯✪☄✦❉✧♱♰♂♀⋆⋇*✖✗✘✕✓✔✄✂☎☏✆✉♪♩♫♬♭۞⌘☐☑☒⚐⚑♻⚠⚡⚀⚁⚂⚃⚄⚅⌚⌛♿⚓✈☕"]    #Icons
#----Fonts----

def loadChars():
    global emoji_list, char_list
    char_dict = {}
    current_type = ''


    with open('./char.txt','r',encoding='utf-8') as f:
        line = f.readline()

        while line:
            if line.endswith('\n'): line = line[:-1]
            line = line.strip()
            if line == '':
                line = f.readline()
                continue
            elif line[0] in 'abcdefghijklmnopqrstuvwxyzC': #start of a category, cap C for CJK
                current_type = line
                char_dict[current_type] = ''
            else:
                char_dict[current_type] += line

            line = f.readline()

    emoji_list.append(char_dict['humans'])
    emoji_list.append(char_dict['animals'])
    emoji_list.append(char_dict['plants'])
    emoji_list.append(char_dict['foodstuff'])
    emoji_list.append(char_dict['travel'])
    emoji_list.append(char_dict['weather'])
    emoji_list.append(char_dict['activities'])
    emoji_list.append(char_dict['objects'])
    emoji_list.append(char_dict['symbols'])
    emoji_list.append(char_dict['computers'])

    char_list.append(char_dict['alphabets'])
    char_list.append(char_dict['notations'])
    char_list.append(char_dict['arrows'])
    char_list.append(char_dict['mathematics'])
    char_list.append(char_dict['shapes'])
    char_list.append(char_dict['CJK'])
    char_list.append(char_dict['games'])

class Fonts(Enum):
    NORMAL = 0
    FULL_SHAPE = 1
    SERIF_BOLD = 2
    SERIF_ITALIC = 3
    GOTHIC_HANDWRITTEN = 4
    GOTHIC_HANDWRITTEN_BOLD = 5
    HANDWRITTEN = 6
    HANDWRITTEN_BOLD = 7
    DOUBLE_LINE = 8
    SMALL_CAPS = 9
    TYPEWRITER  = 10

class Facemodes(Enum):
    FRONT = 0
    BACK = 1
    BOTH = 2

class Signtypes(Enum):
    OAK = 1
    OAK_HANGING = 2

    

fonts_name = [
    "Normal",
    "Ｆｕｌｌ－ｓｈａｐｅ",
    "𝐒𝐞𝐫𝐢𝐟 𝐁𝐨𝐥𝐝",
    "𝑆𝑒𝑟𝑖𝑓 𝐼𝑡𝑎𝑙𝑖𝑐",
    "𝔊𝔬𝔱𝔥𝔦𝔠 ℌ𝔞𝔫𝔡𝔴𝔯𝔦𝔱𝔱𝔢𝔫",
    "𝕲𝖔𝖙𝖍𝖎𝖈 𝕳𝖆𝖓𝖉𝖜𝖗𝖎𝖙𝖙𝖊𝖓 𝕭𝖔𝖑𝖉",
    "𝐻𝒶𝓃𝒹𝓌𝓇𝒾𝓉𝓉𝑒𝓃",
    "𝓗𝓪𝓷𝓭𝔀𝓻𝓲𝓽𝓽𝓮𝓷 𝓑𝓸𝓵𝓭",
    "𝔻𝕠𝕦𝕓𝕝𝕖 𝕃𝕚𝕟𝕖",
    "sᴍᴀʟʟ ᴄᴀᴘs",
    "𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛"
]

fonts_mapping = [
    """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789""",
    """ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ０１２３４５６７８９""",

"""𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗""",

"""𝒂𝒃𝒄𝒅𝒆𝒇𝒈𝒉𝒊𝒋𝒌𝒍𝒎𝒏𝒐𝒑𝒒𝒓𝒔𝒕𝒖𝒗𝒘𝒙𝒚𝒛𝑨𝑩𝑪𝑫𝑬𝑭𝑮𝑯𝑰𝑱𝑲𝑳𝑴𝑵𝑶𝑷𝑸𝑹𝑺𝑻𝑼𝑽𝑾𝑿𝒀𝒁0123456789""",

"""𝔞𝔟𝔠𝔡𝔢𝔣𝔤𝔥𝔦𝔧𝔨𝔩𝔪𝔫𝔬𝔭𝔮𝔯𝔰𝔱𝔲𝔳𝔴𝔵𝔶𝔷𝔄𝔅ℭ𝔇𝔈𝔉𝔊ℌℑ𝔍𝔎𝔏𝔐𝔑𝔒𝔓𝔔ℜ𝔖𝔗𝔘𝔙𝔚𝔛𝔜ℨ0123456789""",

"""𝖆𝖇𝖈𝖉𝖊𝖋𝖌𝖍𝖎𝖏𝖐𝖑𝖒𝖓𝖔𝖕𝖖𝖗𝖘𝖙𝖚𝖛𝖜𝖝𝖞𝖟𝕬𝕭𝕮𝕯𝕰𝕱𝕲𝕳𝕴𝕵𝕶𝕷𝕸𝕹𝕺𝕻𝕼𝕽𝕾𝕿𝖀𝖁𝖂𝖃𝖄𝖅0123456789""",

"""𝒶𝒷𝒸𝒹ℯ𝒻ℊ𝒽𝒾𝒿𝓀𝓁𝓂𝓃ℴ𝓅𝓆𝓇𝓈𝓉𝓊𝓋𝓌𝓍𝓎𝓏𝒜ℬ𝒞𝒟ℰℱ𝒢ℋℐ𝒥𝒦ℒℳ𝒩𝒪𝒫𝒬ℛ𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵0123456789""",

"""𝓪𝓫𝓬𝓭𝓮𝓯𝓰𝓱𝓲𝓳𝓴𝓵𝓶𝓷𝓸𝓹𝓺𝓻𝓼𝓽𝓾𝓿𝔀𝔁𝔂𝔃𝓐𝓑𝓒𝓓𝓔𝓕𝓖𝓗𝓘𝓙𝓚𝓛𝓜𝓝𝓞𝓟𝓠𝓡𝓢𝓣𝓤𝓥𝓦𝓧𝓨𝓩0123456789""",

"""𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡""",

"""ᴀʙᴄᴅᴇꜰɢʜɪᴊᴋʟᴍɴᴏᴘǫʀꜱᴛᴜᴠᴡxʏᴢABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789""",

"""𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"""
]

#----versions----
supported_versions = ['1.20','1.21','Raw','HTML']

point_size = 24
if platform.system() == 'Windows':
    point_size = 36
elif platform.system() == 'Darwin':
    point_size = 24
else:
    point_size = 24
win_width = 420
win_height = 220