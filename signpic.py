from constants import *

from PIL import Image
import sys
#▌:18 |:45

def analyzeImage(imageName : str) -> tuple[int,str]:
    global point_size
    
    try:
        img = Image.open(imageName)
    except:
        return (-1,"")
    command = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html>

<head>
    <meta name="qrichtext" content="1" />
    <style type="text/css">
        p,
        li {
            white-space: pre-wrap;
        }
    </style>
</head>

<body style=" font-family:mcprev','unimc'; font-size:%dpx; font-weight:400; font-style:normal;letter-spacing:0;">""" %point_size

    width  = img.size[0]
    height = img.size[1]

    for i in range(0,height):
        command += createLine(i,img)
    
    #return command[:-1] + "}}"
    return (width,command + "</body></html>")

def createLine(line, image) -> str:
    #command = "Text%d:\'[\"\"" % (line + 1)
    command = """<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">"""
    width = image.size[0]

    for i in range(width):
        command += createPixel(image, (i,line))
    
    #command += "]\',"
    command += "</p>"
    return command


def createPixel(image, coord : tuple[int,int])->str:
    color = getColorHex(image.getpixel(coord))
    #return ",{\"text\":\"%s\",\"color\":\"#%s\"}" % (pixel,color)
    return "<span style=\" color:#%s;\">$</span>" % color

def getColorHex(color) -> str:
    return "%02x%02x%02x" % (color[0],color[1],color[2])

#Parament process