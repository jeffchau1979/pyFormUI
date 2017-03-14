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
import sys
sys.path.append('../')

from FormUI import *

#Load layout xml file
builder = Builder()
builder.loadLayout('customcontrol.xml')

#Setup Handler
def OkButtonHandler(windowHandler, handlerPara):
    print handlerPara.valueList
    windowHandler.closeWindow()
builder.setCtrlHandler('id_ok', OkButtonHandler)


class CustomCtrlRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        if 'multi_line' in item.keys() and getItemValue(item, 'multi_line') == 'true':
            para['style'] = para['style'] | wx.TE_MULTILINE
        if 'password' in item.keys() and getItemValue(item, 'password') == 'true':
            para['style'] = para['style'] | wx.TE_PASSWORD
        para['value'] =  getItemValue(item, 'value', '')
        itemCtrl = wx.TextCtrl(**para)
        return itemCtrl
    @staticmethod
    def onGetValue(item):
        return item['control'].GetValue()
    @staticmethod
    def onSetValue(item,value):
        item['control'].SetValue(value)
builder.registControl('custom_ctrl', CustomCtrlRegist)

#Show FormUI
formUI = FormUI(builder)
formUI.show()
