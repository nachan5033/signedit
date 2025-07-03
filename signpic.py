from constants import *

from PIL import Image
import sys
#▌:18 |:45

def openImage(imageName : str) -> Image.Image:
    try:
        img = Image.open(imageName)
        return img
    except:
        return None

def analyzeImage(img : Image.Image, resize = None, crop = None) -> str:
    
    command = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
<html>

<head>
    <meta name="qrichtext" content="1" />
    <style type="text/css">
        p,
        li {
            white-space: pre-wrap;
            font-size:#POINT_SIZEpx;
        }
    </style>
</head>

<body style=" font-family:mcprev','unimc'; font-size:#POINT_SIZEpx; font-weight:400; font-style:normal;letter-spacing:0;">""" 
    if resize is not None:img = img.resize(resize)
    if crop is not None:img = img.crop(crop)

    height = img.size[1]

    for i in range(0,height):
        command += createLine(i,img)
    
    return command + "</body></html>"

def createLine(line, image) -> str:
    command = """<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">"""
    width = image.size[0]

    for i in range(width):
        command += createPixel(image, (i,line))
    
    command += "</p>"
    return command


def createPixel(image, coord : tuple[int,int])->str:
    color = getColorHex(image.getpixel(coord))
    return "<span style=\" color:#%s;\">$</span>" % color

def getColorHex(color) -> str:
    return "%02x%02x%02x" % (color[0],color[1],color[2])

#Parament process