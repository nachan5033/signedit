from lxml import etree

def isMakeSense(cmd : str) -> bool:
    return (not cmd.isspace()) and cmd != ""

def makecommand(cmd : str) -> str:
    cmd = cmd.replace("\'","\\'")
    cmd = cmd.replace("\"","\\\\\"")
    return cmd

def makegive(type : str, text : str, command : str, name : str) -> str:
    cmdbase = "/give @p minecraft:%s_sign{BlockEntityTag:{Text1:\'%s\',Text2:\'%s\',Text3:\'%s\',Text4:\'%s\'},dispaly:{Name:\'{\"text\":\"%s\"}\'}}"

    html = etree.HTML(text)
    lines = html.xpath("//p")
    

    count = 0
    texts = ['','','','']
    commands = command.split("\n") + ["","","",""]
    for line in lines:
        result = "["
        head = line.xpath("./text()")    
        result += ("\"" + str(head)[2:-2] + "\"")

        for sub in line.xpath("./span"):
            inside = str(sub.xpath("./text()"))[2:-2]
            subtext = ",{\"text\":\"%s\"" % inside
            style = sub.get("style")#str(sub.xpath("@style"))[2:-2]
            if "italic" in style:
                subtext += ",\"italic\":\"true\""
            if "font-weight:600" in style:
                subtext += ",\"bold\":\"true\""
            if isMakeSense(inside):
                if "underline" in style:
                    subtext += ",\"underlined\":\"true\""
                if "line-through" in style:
                    subtext += ",\"strikethrough\":\"true\""
                if "color:#" in style:
                    colorindex = style.find("color:#")
                    subtext += ",\"color\":\"%s\"" % style[colorindex + 6:colorindex + 13]
            subtext += "}"
            result += subtext
            if len(sub.xpath("./br")):
                if isMakeSense(commands[count]):
                    append_command = ",{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"%s\"}}"
                    result += append_command % makecommand(commands[count])
                result += "]"
                texts[count] = result
                count += 1
                result = "["
                continue
        
        if isMakeSense(commands[count]):
            append_command = ",{\"text\":\"\",\"clickEvent\":{\"action\":\"run_command\",\"value\":\"%s\"}}"
            result += append_command % makecommand(commands[count])

        result += "]"
        texts[count] = result
        count += 1
        if count >= 4:
            break
    
    return cmdbase % (type,texts[0],texts[1],texts[2],texts[3],name)

    #print(text)
    #print(command)