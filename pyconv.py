#from unittest import result
from pypinyin import pinyin,lazy_pinyin

tsyan_J = "积唧疾挤集辑嫉即籍脊际剂霁济荠祭寂绩迹稷蒺跻鲚齑鲫尖箭煎剪荐贱尖戋笺翦饯戬谫溅歼僭鞯溅践湔牮渐将浆奖酱蒋匠桨虹\
    焦蕉椒礁鹪噍湫嚼鹪醮噍剿僬接节姐睫藉捷婕疖借截嗟啑津进尽浸晋烬荩缙赆溍精睛晶旌井靖阱菁靓净腈婧静酒就揪鹫僦蹴啾鬏疽狙且聚沮咀苴龃雎趄\
        朘睃镌隽绝嚼爵爝穱俊峻竣浚骏隽濬馂"

tsyan_Q = "七妻漆戚柒栖齐砌凄脐缉沏荠萋蛴葺嘁槭碛千签钎迁扦仟前钱潜浅倩佥芊阡茜堑枪墙抢呛蔷跄戗戕炝锵樯嫱锖锹悄瞧鞘雀峭樵憔谯愀诮劁俏\
    切且窃砌趄妾亲侵寝秦吣螓嗪沁锓清氰青情晴圊请箐蜻鲭亲秋楸鳅湫囚泅酋蝤遒煪娶蛆黢趋取趣觑悛全泉痊醛铨筌诠辁荃雀鹊碏皵踖逡夋踆"

tsyan_X = "西息惜昔媳腊玺洗袭细席熄锡膝夕悉粞矽晰硒铣析汐犀葸蟋徙屣习先鲜仙纤涎羡铣藓冼跹酰暹筅氙霰涎籼跣线腺相箱镶厢湘襄葙缃骧翔祥橡详庠蟓鲞想象像\
    消削销逍绡箫蛸萧宵肖硝霄筱潇啸小笑写楔些斜谢契屑邪榍榭绁卸泻泄燮躞亵新心芯薪锌辛寻莘信囟星腥猩惺省擤醒性姓修羞馐锈绣袖秀宿脩岫\
        须需戌徐绪恤糈蓿胥醑溆续序絮婿宣选癣漩璇镟旋渲瑄揎削薛鳕雪踅寻循殉浚旬巡询恂郇蕈荀徇汛浔讯迅逊巽驯"

ru_tone_K = "屋木竹目服福禄熟谷肉咒鹿腹菊陆轴逐牧伏宿读犊渎牍椟黩毂复粥肃育六缩哭幅斛戮仆畜蓄\
    叔淑菽独卡馥沐速祝麓镞蹙筑穆睦啄覆鹜秃扑鬻辐瀑竺簇暴掬濮郁矗复塾朴蹴煜谡碌毓舳柚蝠辘夙蝮匐觫囿苜茯髑副孰谷\
    沃俗玉足曲粟烛属录辱狱绿毒局欲束鹄蜀促触续督赎浴酷瞩躅褥旭欲渌逯告仆\
    觉角桷较岳乐捉朔数卓汲琢剥趵爆驳邈雹璞朴确浊擢镯濯幄喔药握搦学药薄恶略作乐落阁鹤爵若约脚雀幕洛壑索郭博错跃若缚酌托削铎灼凿却络鹊度诺\
    橐漠钥著虐掠获泊搏勺酪谑廓绰霍烁莫铄缴谔鄂亳恪箔攫涸疟郝骆膜粕礴拓蠖鳄格昨柝摸貉愕柞寞膊魄烙焯厝噩泽矍各猎昔芍踱迮\
    陌石客白泽伯迹宅席策碧籍格役帛戟璧驿麦额柏魄积脉夕液册尺隙逆画百辟赤易革脊获翮屐适剧碛隔益栅窄核掷责惜僻癖辟掖腋释\
    舶拍择摘射斥弈奕迫疫译昔瘠赫炙谪虢腊硕螫藉翟亦鬲骼鲫借啧蜴帼席貊汐摭咋吓剌百莫蝈绎霸霹\
    锡壁历枥击绩笛敌滴镝檄激寂翟逖籴析晰溺觅摘狄荻戚涤的吃霹沥惕踢剔砾栎适嫡阋觋淅晰吊霓倜\
    职国德食蚀色力翼墨极息直得北黑侧饰贼刻则塞式轼域殖植敕饬棘惑默织匿亿忆特勒劾仄稷识逼克蜮唧即拭弋陟测冒抑恻肋亟殛忒嶷熄穑啬匐鲫或愎翌"

ru_tone_T = "质日笔出室实疾术一乙壹吉秩密率律逸佚失漆栗毕恤蜜橘溢瑟膝匹黜弼七叱卒虱悉谧轶诘戌佶栉昵窒必侄蛭泌秫蟀嫉唧怵帅聿郅桎茁汨尼蒺\
    物佛拂屈郁乞掘讫吃绂弗诎崛勿熨厥迄不屹芴倔尉蔚月骨发阙越谒没伐罚卒竭窟笏钺歇突忽勃蹶筏厥蕨掘阀讷殁粤悖兀碣猝樾羯汨咄渤凸滑\
    孛核饽垡阏堀曰讦曷达末阔活钵脱夺褐割沫拔葛渴拨豁括聒抹秣遏挞萨掇喝跋獭撮剌泼斡捋袜适咄妲\
    黠札拔猾八察杀刹轧刖戛秸嘎瞎刮刷滑屑节雪绝列烈结穴说血舌洁别裂热决铁灭折拙切悦辙诀泄咽噎杰彻别哲设劣碣掣谲窃缀阅抉挈捩\
    楔蹩亵蔑捏竭契疖涅颉撷撤跌蔑浙澈蛭揭啜辍迭呐侄冽掇批橇"

ru_tone_P = "缉辑立集邑急入泣湿习给十拾什袭及级涩粒揖汁蛰笠执隰汲吸熠岌歙熠挹合塔答纳榻杂腊蜡匝阖蛤衲沓鸽踏飒拉盍搭溘嗑\
    叶帖贴牒接猎妾蝶箧涉捷颊楫摄蹑谍协侠荚睫慑蹀挟喋燮褶靥烨摺辄捻婕聂霎洽狭峡法甲业邺匣压鸭乏怯劫胁插押狎掐夹恰眨呷喋札钾"

def toPinyin(text : str)->str:
    global mode,is_start
    result = []
    i = 0
    while i < len(text):
        char = text[i]
        if i < len(text) - 1 and (text[i + 1] == "[" or text[i + 1] == '【'):
            pinyin = ""
            i += 2
            if i >= len(text):
                break
            while i < len(text) and text[i] != ']' and text[i] != '】':
                pinyin += str(text[i])
                i += 1
            result.append(translateForm(char,pinyin))
        elif char >= u'\u4e00' and char <=u'\u9fa5':# i is a Chinese character
            result.append(translateForm(char))
        else:
            result.append(char)
        i += 1
    return result

def translateForm(char, pinyin : str = "")->str:
    translated_list = []
    if pinyin == "":
        pinyin = lazy_pinyin(char)[0]
    i = 0

    if pinyin.startswith("yi"):#e.g. yin -> in
        translated_list.append(getRightMode("i"))
        i = 2
    elif pinyin.startswith("wu"):
        translated_list.append(getRightMode("u"))
        i = 2
    elif pinyin.startswith("ju"):
        translated_list.append(getRightMode("kyu"))
        i = 2
    elif pinyin.startswith("qu"):
        translated_list.append(getRightMode("chyu"))
        i = 2
    elif pinyin.startswith("xu"):
        translated_list.append(getRightMode("shyu"))
        i = 2

    length = len(pinyin)
    for i in range(i,length):
        letter = pinyin[i]
        if letter == 'j' or letter == 'q' or letter == 'x':
            translated_list.append(markTwantsyan(char,letter))
        elif letter == 'z':
            translated_list.append("c")
        elif letter == 'g' and i == 0:
            translated_list.append("k")
        elif letter == 'd':
            translated_list.append("t")
        elif letter == 'b':
            translated_list.append("p")
        elif letter == 'v':
            translated_list.append("yu")
        elif i + 1 < length and letter == 'o' and pinyin[i + 1] == 'n':
            translated_list.append("u")
        elif i + 1 < length and letter == 'u' and pinyin[i + 1] == 'n':
            translated_list.append("we")
        elif i + 1 < length and letter == 'i' and pinyin[i + 1] == 'u':
            translated_list.append("yo")
        elif i + 1 < length and letter == 'u' and pinyin[i + 1] == 'i':
            translated_list.append("we")
        elif i + 1 < length and letter == 'u' and pinyin[i + 1] == 'e' and pinyin[i - 1] != 'y':
            translated_list.append("yu")
        elif i + 1 < length and letter == 'u':
            translated_list.append("w")
        elif i + 1 < length and letter == 'i' and pinyin[i + 1] != 'n':
            translated_list.append("y")
        else:
            translated_list.append(letter)
    
    translated_list = markTone(char,translated_list)
    result = ""
    for i in translated_list:
        result += i
    return getRightMode(result)

def markTwantsyan(char,firstLetter):
    if char in tsyan_J:
        return "tz"
    if char in tsyan_Q:
        return "ts"
    if char in tsyan_X:
        return "s"
    else:
        if firstLetter == 'j':
            return "k"
        elif firstLetter == 'q':
            return "ch"
        elif firstLetter == 'x':
            return "sh"
        else:
            return str(firstLetter)

def markTone(char,list : list):
    if char in ru_tone_K:
        list.append("k")
    elif char in ru_tone_P:
        list.append("p")
    elif char in ru_tone_T:
        list.append("t")
    
    return list


def getRightMode(text : str):
    result = text
    return result

def showDemo():
    print("""
    ！有鳥 -> YOUNYAO\n
    勝利-！廣場-/地下通道 -> Shengli-KWANGCHANG-tishyatongtao\n
    奏樂[yue]堂 -> Couyuetang\n
    """)

def makeFullWidth(text : str):
    result = ""
    for i in text:
        if i != " ":
            result += chr(ord(i) + 0xfee0)
        else:
            result += i
    return result
#main
"""
result = ""

print("有鳥府大學院 有鳥音轉換程式")
print("+：首字母大寫（默認模式） !或！： 全部大寫 /：全部小寫 []或【】：標記多音字 ?或？：示例")

while 1:

    text = input(">")

    if text == "~":
        exit()
    elif text == "?":
        showDemo()
    else:
        res = toPinyin(text)
        for i in res:
            result += i
        print(result)
        print(makeFullWidth(result))

        result = ""
        is_start = 1
        mode = FIRST_CAPITAL"""
