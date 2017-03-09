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

from CustomControl import *
import wx.lib.scrolledpanel as scrolled
import wx.lib.filebrowsebutton

global gControlRegister
gControlRegister = {}

class CtrlRegist():
    @staticmethod
    def makeCommonPara(item,parent):
        itemWidth = int(item['width'])
        itemHeight = int(item['height'])
        align = CtrlRegist.getAlign(item)

        para ={}
        para['size'] = wx.Size(itemWidth, itemHeight)
        para['pos'] = wx.Point(0, 0)
        para['name'] = getItemValue(item, 'id')
        para['parent'] = parent
        para['id'] = wx.NewId()
        item['event_id'] = para['id']
        para['style'] = align
        return  para

    @staticmethod
    def getLable(item):
        if 'label' in item.keys():
            labelText = getItemValue(item, 'lable', "")
        elif 'title' in item.keys():
            labelText = getItemValue(item, 'title', "")
            return labelText

    @staticmethod
    def getAlign(item):
        if 'align' in item.keys():
            alignText = getItemValue(item,'align','left')
            if alignText == 'center':
                return  wx.ALIGN_CENTER
            elif alignText == 'right':
                return  wx.ALIGN_RIGHT
            elif alignText == 'left' :
                return  wx.ALIGN_LEFT
        return 0

    @staticmethod
    def onGetValue(item):
        if hasattr(item['control'],'GetValue'):
            item['value'] = item['control'].GetValue()
            return item['value']
        else:
            return None
    def onSetValue(item, value):
        if hasattr(item['control'], 'SetValue'):
            item['control'].SetValue(value)
class StaticRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        para['label'] =  CtrlRegist.getLable(item)
        itemCtrl = wx.StaticText(**para)
        return itemCtrl
gControlRegister['static'] = StaticRegist

class ChoiseRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item, parent)
        para['choices'] =  getItemValue(item, 'choices', [])
        itemCtrl = wx.Choice(**para)
        value = getItemValue(item, 'value', '')
        index = getItemValue(item, 'choices', []).index(value)
        if index >= 0:
            itemCtrl.Select(index)
        windowControl.registItemHandler(itemCtrl, wx.EVT_CHOICE, para['id'])
        return itemCtrl

    @staticmethod
    def onGetValue(item):
        return item['choices'][item['control'].GetSelection()]

    @staticmethod
    def onSetValue(item,value):
        index = getItemValue(item, 'choices', []).index(value)
        if index >= 0:
            item['control'].Select(index)

gControlRegister['choise'] = ChoiseRegist

class TextRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        if 'multi_line' in item.keys() and getItemValue(item, 'multi_line') == 'true':
            para['style'] = para['style'] | wx.TE_MULTILINE
        if 'password' in item.keys() and getItemValue(item, 'password') == 'true':
            para['style'] = para['style'] | wx.TE_PASSWORD
        para['value'] =  getItemValue(item, 'value', '')
        itemCtrl = wx.TextCtrl(**para)
        return itemCtrl
gControlRegister['text'] = TextRegist


class StaticLineRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        para['label'] = CtrlRegist.getLable(item)
        itemCtrl = StaticLine(**para)
        return itemCtrl
gControlRegister['static_line'] = StaticLineRegist

class CheckListRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        choices = getItemValue(item, 'choices', [])
        para['choices'] = choices
        itemCtrl = wx.CheckListBox(**para)
        value = getItemValue(item, 'value', '')
        default_check = []
        for check_item in value:
            if check_item in choices:
                index = choices.index(check_item)
                default_check.append(index)
        itemCtrl.SetChecked(default_check)

        return itemCtrl
    @staticmethod
    def onGetValue(item):
        checked_list = item['control'].GetChecked()
        item['value'] = []
        choices = getItemValue(item, 'choices', [])
        for index in checked_list:
            item['value'].append(choices[index])
        return item['value']
    @staticmethod
    def onSetValue(item,value):
        choices = getItemValue(item, 'choices', [])
        if len(choices) < 1:
            return
        default_check = []
        for check_item in value:
            index = choices.index(check_item)
            if index >= 0:
                default_check.append(index)
        item['control'].SetChecked(default_check)
gControlRegister['check_list'] = CheckListRegist


class RadioBoxRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        choices = getItemValue(item, 'choices', [])
        para['choices'] = choices
        para['majorDimension'] = int(getItemValue(item, 'columns', '1'))
        para['style'] = para['style'] | wx.RA_SPECIFY_COLS
        itemCtrl = wx.RadioBox(**para)
        value = getItemValue(item, 'value', '')
        index = choices.index(value)
        itemCtrl.SetSelection(index)
        windowControl.registItemHandler(itemCtrl, wx.EVT_RADIOBOX, para['id'])
        return itemCtrl
    @staticmethod
    def onGetValue(item):
        return item['control'].GetStringSelection()
    @staticmethod
    def onSetValue(item,value):
        choices = getItemValue(item, 'choices', [])
        index = choices.index(value)
        item['control'].SetSelection(index)
gControlRegister['radio_box'] = RadioBoxRegist


class CheckRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        para['label'] = CtrlRegist.getLable(item)
        itemCtrl = wx.CheckBox(**para)
        value = getItemValue(item, 'value', '')
        if value == 'true':
            itemCtrl.SetValue(True)
        windowControl.registItemHandler(itemCtrl, wx.EVT_CHECKBOX, para['id'])
        return itemCtrl
    @staticmethod
    def onGetValue(item):
        return 'true' if item['control'].GetValue() else 'false'
    @staticmethod
    def onSetValue(item,value):
        if value == 'true':
            item['control'].SetValue(True)
        else:
            item['control'].SetValue(False)
gControlRegister['check'] = CheckRegist


class ComboBoxRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        choices = getItemValue(item, 'choices', [])
        para['choices'] = choices
        itemCtrl = wx.ComboBox(**para)
        value = getItemValue(item, 'value', '')
        if value == 'true':
            itemCtrl.SetValue(value)
        elif len(choices) > 0:
            itemCtrl.SetValue(choices[0])
        return itemCtrl
gControlRegister['combo_box'] = ComboBoxRegist



class DateRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        para['style'] = para['style'] | wx.DP_SHOWCENTURY | wx.DP_DEFAULT
        itemCtrl = wx.DatePickerCtrl(**para)
        value = getItemValue(item, 'value', '')
        if value != "":
            dt = wx.DateTime()
            dt.ParseDate(value)
            itemCtrl.SetValue(dt)
        if value != "":
            dt = wx.DateTime()
            dt.ParseDate(value)
            itemCtrl.SetValue(dt)
        return itemCtrl
    @staticmethod
    def onGetValue(item):
        return item['control'].GetValue().FormatISODate()
    @staticmethod
    def onSetValue(item,value):
        if value != "":
            dt = wx.DateTime()
            dt.ParseDate(value)
            item['control'].SetValue(dt)
gControlRegister['date'] = DateRegist


class TimeRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        para['display_seconds'] = True
        para['fmt24hr'] = True
        para['oob_color'] = wx.NamedColour('Yellow')
        para['useFixedWidthFont'] = True
        itemCtrl =  wx.lib.masked.timectrl.TimeCtrl(**para)
        value = getItemValue(item, 'value', '')
        if value != "":
            itemCtrl.SetValue(value)
        return itemCtrl
gControlRegister['time'] = TimeRegist


class DateTimeRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        itemCtrl =  DateTime(**para)
        value = getItemValue(item, 'value', '')
        if value != "":
            itemCtrl.SetValue(value)
        return itemCtrl
gControlRegister['datetime'] = DateTimeRegist

class ButtonRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        para['label'] = CtrlRegist.getLable(item)
        itemCtrl =  wx.Button(**para)
        windowControl.registItemHandler(itemCtrl, wx.EVT_BUTTON, para['id'])
        return itemCtrl
gControlRegister['button'] = ButtonRegist

class FileRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        para['buttonText'] = 'Browse'
        para['dialogTitle'] = 'Choose a file'
        para['fileMask'] = getItemValue(item, 'mark', "*.*")
        para['labelText'] = CtrlRegist.getLable(item)
        para['style'] = para['style'] | wx.TAB_TRAVERSAL
        para['startDirectory'] = '.'
        para['fileMode'] = wx.SAVE
        para['toolTip'] = 'Type filename or click browse to choose file'
        if 'choices' in item.keys():
            itemCtrl =  wx.lib.filebrowsebutton.FileBrowseButtonWithHistory(**para)
            itemCtrl.SetHistory(getItemValue(item, 'choices'))
        else:
            itemCtrl = wx.lib.filebrowsebutton.FileBrowseButton(**para)
        windowControl.registItemHandler(itemCtrl, wx.EVT_BUTTON, para['id'])
        return itemCtrl
gControlRegister['file'] = FileRegist

class FolderRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        value = getItemValue(item, 'value', '')
        para['dialogTitle'] = 'Choose a folder'
        para['labelText'] = CtrlRegist.getLable(item)
        para['startDirectory'] = value
        para['style'] = para['style'] | wx.TAB_TRAVERSAL
        itemCtrl =   wx.lib.filebrowsebutton.DirBrowseButton(**para)

        if value != "":
            itemCtrl.SetValue(value)
        return itemCtrl
gControlRegister['folder'] = FolderRegist



class FolderRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        value = getItemValue(item, 'value', '')
        para['dialogTitle'] = 'Choose a folder'
        para['labelText'] = CtrlRegist.getLable(item)
        para['startDirectory'] = value
        para['style'] = para['style'] | wx.TAB_TRAVERSAL
        itemCtrl =   wx.lib.filebrowsebutton.DirBrowseButton(**para)

        if value != "":
            itemCtrl.SetValue(value)
        return itemCtrl
gControlRegister['folder'] = FolderRegist



class MultiFilesRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        para['mask'] = getItemValue(item, 'mask', '*.*')
        para['bAddFile'] = True
        para['bAddFolder'] = False
        value = getItemValue(item, 'value', '')
        itemCtrl =  MultiFolderFile(**para)
        if value != "":
            itemCtrl.SetValue(value)
        return itemCtrl
gControlRegister['multi_files'] = MultiFilesRegist


class MultiFoldersRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        para['mask'] = getItemValue(item, 'mask', '*.*')
        para['bAddFile'] = False
        para['bAddFolder'] = True
        value = getItemValue(item, 'value', '')
        itemCtrl =  MultiFolderFile(**para)
        if value != "":
            itemCtrl.SetValue(value)
        return itemCtrl
gControlRegister['multi_folders'] = MultiFoldersRegist



class MultiFolersFilesRegist(CtrlRegist):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegist.makeCommonPara(item,parent)
        para['mask'] = getItemValue(item, 'mask', '*.*')
        para['bAddFile'] = True
        para['bAddFolder'] = True
        value = getItemValue(item, 'value', '')
        itemCtrl =  MultiFolderFile(**para)
        if value != "":
            itemCtrl.SetValue(value)
        return itemCtrl
gControlRegister['multi_folders_files'] = MultiFolersFilesRegist
