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
from ControlRegisterBase import *

global gControlRegister
gControlRegister = {}
class StaticRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        para['label'] =  CtrlRegistBase.getLable(item)
        itemCtrl = wx.StaticText(**para)
        return itemCtrl
gControlRegister['static'] = StaticRegist


class ChoiseRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item, parent)
        para['choices'] =  getItemValue(item, 'choices', [])
        itemCtrl = wx.Choice(**para)
        value = getItemValue(item, 'value', '')
        windowControl.registItemHandler(itemCtrl, para['id'],wx.EVT_CHOICE,'evt_choice')
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


class TextRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        if 'multi_line' in item.keys() and getItemValue(item, 'multi_line') == 'true':
            para['style'] = para['style'] | wx.TE_MULTILINE
        if 'password' in item.keys() and getItemValue(item, 'password') == 'true':
            para['style'] = para['style'] | wx.TE_PASSWORD
        para['value'] =  getItemValue(item, 'value', '')
        itemCtrl = wx.TextCtrl(**para)
        return itemCtrl
gControlRegister['text'] = TextRegist


class StaticLineRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        para['label'] = CtrlRegistBase.getLable(item)
        itemCtrl = StaticLine(**para)
        return itemCtrl
gControlRegister['static_line'] = StaticLineRegist


class CheckListRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        choices = getItemValue(item, 'choices', [])
        para['choices'] = choices
        itemCtrl = wx.CheckListBox(**para)
        windowControl.registItemHandler(itemCtrl, para['id'], wx.EVT_CHECKLISTBOX,'evt_checklistbox')
        return itemCtrl
    @staticmethod
    def onGetValue(item):
        checked_list = item['control'].GetChecked()
        value = []
        choices = getItemValue(item, 'choices', [])
        for index in checked_list:
            value.append(choices[index])
        return value
    @staticmethod
    def onSetValue(item,value):
        choices = getItemValue(item, 'choices', [])
        if len(choices) < 1:
            return
        default_check = []
        if value != '':
            for check_item in value:
                if check_item in choices:
                    index = choices.index(check_item)
                    default_check.append(index)
        item['control'].SetChecked(default_check)
gControlRegister['check_list'] = CheckListRegist

class ListRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        choices = getItemValue(item, 'choices', [])
        para['choices'] = choices
        itemCtrl = wx.ListBox(**para)
        windowControl.registItemHandler(itemCtrl, para['id'], wx.EVT_LISTBOX,'evt_listbox')
        windowControl.registItemHandler(itemCtrl, para['id'], wx.EVT_LISTBOX_DCLICK, 'evt_listbox_dclick')
        return itemCtrl
    @staticmethod
    def onGetValue(item):
        return item['control'].GetStringSelection()
    @staticmethod
    def onSetValue(item,value):
        choices = getItemValue(item, 'choices', [])
        if value in choices:
            index = choices.index(value)
            item['control'].SetSelection(index)
gControlRegister['list'] = ListRegist

class RadioBoxRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        choices = getItemValue(item, 'choices', [])
        para['choices'] = choices
        para['majorDimension'] = int(getItemValue(item, 'columns', '1'))
        para['style'] = para['style'] | wx.RA_SPECIFY_COLS
        itemCtrl = wx.RadioBox(**para)
        windowControl.registItemHandler(itemCtrl, para['id'], wx.EVT_RADIOBOX,'evt_radiobox')
        return itemCtrl
    @staticmethod
    def onGetValue(item):
        return item['control'].GetStringSelection()
    @staticmethod
    def onSetValue(item,value):
        choices = getItemValue(item, 'choices', [])
        if value in choices:
            index = choices.index(value)
            item['control'].SetSelection(index)
gControlRegister['radio_box'] = RadioBoxRegist


class CheckRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        para['label'] = CtrlRegistBase.getLable(item)
        itemCtrl = wx.CheckBox(**para)
        windowControl.registItemHandler(itemCtrl, para['id'], wx.EVT_CHECKBOX,'evt_checkbox')
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


class ComboBoxRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
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


class DateRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        para['style'] = para['style'] | wx.DP_SHOWCENTURY | wx.DP_DEFAULT
        itemCtrl = wx.DatePickerCtrl(**para)
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


class TimeRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
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


class DateTimeRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        itemCtrl =  DateTime(**para)
        value = getItemValue(item, 'value', '')
        if value != "":
            itemCtrl.SetValue(value)
        return itemCtrl
gControlRegister['datetime'] = DateTimeRegist


class ButtonRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        para['label'] = CtrlRegistBase.getLable(item)
        itemCtrl =  wx.Button(**para)
        windowControl.registItemHandler(itemCtrl, para['id'], wx.EVT_BUTTON,'evt_button')
        return itemCtrl
gControlRegister['button'] = ButtonRegist


class FileRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        para['buttonText'] = 'Browse'
        para['dialogTitle'] = 'Choose a file'
        para['fileMask'] = getItemValue(item, 'mark', "*.*")
        para['labelText'] = CtrlRegistBase.getLable(item)
        para['style'] = para['style'] | wx.TAB_TRAVERSAL
        para['startDirectory'] = '.'
        para['fileMode'] = wx.SAVE
        para['toolTip'] = 'Type filename or click browse to choose file'
        if 'choices' in item.keys():
            itemCtrl =  wx.lib.filebrowsebutton.FileBrowseButtonWithHistory(**para)
            itemCtrl.SetHistory(getItemValue(item, 'choices'))
        else:
            itemCtrl = wx.lib.filebrowsebutton.FileBrowseButton(**para)
        windowControl.registItemHandler(itemCtrl, para['id'],wx.EVT_BUTTON,'evt_button')
        return itemCtrl
gControlRegister['file'] = FileRegist


class FolderRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        value = getItemValue(item, 'value', '')
        para['dialogTitle'] = 'Choose a folder'
        para['labelText'] = CtrlRegistBase.getLable(item)
        para['startDirectory'] = value
        para['style'] = para['style'] | wx.TAB_TRAVERSAL
        itemCtrl =   wx.lib.filebrowsebutton.DirBrowseButton(**para)
        return itemCtrl
gControlRegister['folder'] = FolderRegist


class FolderRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        value = getItemValue(item, 'value', '')
        para['dialogTitle'] = 'Choose a folder'
        para['labelText'] = CtrlRegistBase.getLable(item)
        para['startDirectory'] = value
        para['style'] = para['style'] | wx.TAB_TRAVERSAL
        itemCtrl =   wx.lib.filebrowsebutton.DirBrowseButton(**para)

        return itemCtrl
gControlRegister['folder'] = FolderRegist


class MultiFilesRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        para['mask'] = getItemValue(item, 'mask', '*.*')
        para['bAddFile'] = True
        para['bAddFolder'] = False
        value = getItemValue(item, 'value', '')
        itemCtrl =  MultiFolderFile(**para)
        return itemCtrl
gControlRegister['multi_files'] = MultiFilesRegist


class MultiFoldersRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        para['mask'] = getItemValue(item, 'mask', '*.*')
        para['bAddFile'] = False
        para['bAddFolder'] = True
        value = getItemValue(item, 'value', '')
        itemCtrl =  MultiFolderFile(**para)
        return itemCtrl
gControlRegister['multi_folders'] = MultiFoldersRegist


class MultiFolersFilesRegist(CtrlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = CtrlRegistBase.makeCommonPara(item,parent)
        para['mask'] = getItemValue(item, 'mask', '*.*')
        para['bAddFile'] = True
        para['bAddFolder'] = True
        value = getItemValue(item, 'value', '')
        itemCtrl =  MultiFolderFile(**para)
        if value != "":
            itemCtrl.SetValue(value)
        return itemCtrl
gControlRegister['multi_folders_files'] = MultiFolersFilesRegist
