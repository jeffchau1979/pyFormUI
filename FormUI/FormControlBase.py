#!/usr/bin/env python
## Copyright 2012, En7788.com, Inc. All rights reserved.
##
## FormUI is a easy used GUI framwork for python, which is based on wxpython.
## FormUI is a free software: you can redistribute it and/or modify it under
## the terms of version 3 of the GNU Lesser General Public License as
## published by the Free Software Foundation.
##
## You should have received a copy of the GNU Lesser General Public License
## along with AndBug.  If not, see <http://www.gnu.org/licenses/>.

from ControlBase import *

import wx.lib.filebrowsebutton
class FormControlUtil():
    @staticmethod
    def makeCommonPara(item,parent):
        itemWidth = -1
        if 'width' in item.keys():
            itemWidth = int(item['width'])
        itemHeight = -1
        if 'height' in item.keys():
            itemHeight = int(item['height'])
        align = FormControlUtil.getAlign(item)

        para ={}
        para['size'] = wx.Size(itemWidth, itemHeight)
        para['pos'] = wx.Point(0, 0)
        para['name'] = BuilderUtil.getItemValue(item, 'id')
        para['parent'] = parent
        para['id'] = wx.NewId()
        item['event_id'] = para['id']
        para['style'] = align
        return  para

    @staticmethod
    def getLable(item):
        if 'label' in item.keys():
            labelText = BuilderUtil.getItemValue(item, 'lable', "")
        elif 'title' in item.keys():
            labelText = BuilderUtil.getItemValue(item, 'title', "")
            return labelText

    @staticmethod
    def convertList(item):
        if isinstance(item, list):
            return item
        retList = []
        if item is None:
            return retList
        strList = item.split(';')
        for str in strList:
            str = str.replace('[semicolon]', ';')
            str = str.replace('[bar]', '|')
            str = str.replace('[bracketleft]', '[')
            str = str.replace('[bracketright]', ']')
            retList.append(str)
        return  retList
    @staticmethod
    def conventBool(item):
        if isinstance(item,bool):
            return item
        return str(item).lower() == 'true'

    @staticmethod
    def getAlign(item):
        if 'align' in item.keys():
            align = BuilderUtil.getItemValue(item,'align','left')
            alignText = str(align)
            if alignText == 'center':
                return  wx.ALIGN_CENTER
            elif alignText == 'right':
                return  wx.ALIGN_RIGHT
            elif alignText == 'left' :
                return  wx.ALIGN_LEFT
            else:
                return align
        return 0

class FormControlBase():
    def __init__(self,item,parent):
        self.item = item
        item['control'] = self
        self.parent = parent
    def onMessage(self,messageId, messagePara):
        return None
