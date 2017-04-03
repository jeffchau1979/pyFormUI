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

    print windowHandler.sendMessage('id_custom_ctrl', 'get_message', '')
    windowHandler.sendMessage('id_custom_ctrl', 'set_message', 'message_para')
    #windowHandler.closeWindow()
builder.setCtrlHandler('id_ok', OkButtonHandler)


class CustomCtrl(FormControlBase,wx.TextCtrl):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item)
        para = FormControlUtil.makeCommonPara(item,parent)
        if 'multi_line' in item.keys() and getItemValue(item, 'multi_line') == 'true':
            para['style'] = para['style'] | wx.TE_MULTILINE
        if 'password' in item.keys() and getItemValue(item, 'password') == 'true':
            para['style'] = para['style'] | wx.TE_PASSWORD
        para['value'] =  BuilderUtil.getItemValue(item, 'value', '')
        wx.TextCtrl.__init__(self, **para)

    def GetValue(self):
        return wx.TextCtrl.GetValue(self)

    def SetValue(self,value):
        wx.TextCtrl.SetValue(self,value)

    def onMessage(self, messageId, messagePara):
        if messageId == 'get_message':
            return  "message:" + self.item['control'].GetValue()
        elif messageId == "set_message":
            self.item['control'].SetValue(messageId + ":" + messagePara)
        return None
builder.registControlType('custom_ctrl', CustomCtrl)

#Show FormUI
formUI = FormUI(builder)
formUI.show()
