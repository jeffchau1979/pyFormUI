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

from FormControlBase import *
import wx.lib.scrolledpanel as scrolled
import wx.lib.filebrowsebutton


global gControlTypeRegister
gControlTypeRegister = {}

###########################
##FormCtrol should implement the interfaces listed below:
##    def GetValue(self):
##    def SetValue(self,value):
##    def Enable(self,bEnable):
##    def SetFocus(self):
##    def onMessage(self, messageId, messagePara):
###########################

class Static(wx.StaticText, FormControlBase):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        para['label'] = FormControlUtil.getLable(item)
        wx.StaticText.__init__(self,**para)

    def GetValue(self):
        return None

    def SetValue(self,value):
        pass
gControlTypeRegister['static'] = Static

class Choise(wx.Choice, FormControlBase):
    def __init__(self, item, parent, windowControl):
        para = FormControlUtil.makeCommonPara(item, parent)
        para['choices'] =  FormControlUtil.convertList(BuilderUtil.getItemValue(item, 'choices', []))
        itemCtrl = wx.Choice.__init__(self,**para)
        FormControlBase.__init__(self, item,parent)
        windowControl.registItemHandler(self, para['id'],wx.EVT_CHOICE,'evt_choice')

    def GetValue(self):
        choices = FormControlUtil.convertList(BuilderUtil.getItemValue(self.item, 'choices', []))
        return choices[wx.Choice.GetSelection(self)]

    def SetValue(self,value):
        choices = FormControlUtil.convertList(BuilderUtil.getItemValue(self.item, 'choices', []))
        index = choices.index(value)
        if index >= 0:
            wx.Choice.Select(self,index)

gControlTypeRegister['choise'] = Choise


class Text(FormControlBase,wx.TextCtrl):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        if 'multi_line' in item.keys() and BuilderUtil.getItemValue(item, 'multi_line') == 'true':
            para['style'] = para['style'] | wx.TE_MULTILINE
        if 'password' in item.keys() and BuilderUtil.getItemValue(item, 'password') == 'true':
            para['style'] = para['style'] | wx.TE_PASSWORD
        para['value'] =  BuilderUtil.getItemValue(item, 'value', '')
        wx.TextCtrl.__init__(self,**para)

gControlTypeRegister['text'] = Text


class StaticLine(StaticLineBase,FormControlBase):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item, parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        para['label'] = FormControlUtil.getLable(item)
        itemCtrl = StaticLineBase.__init__(self, **para)
        return itemCtrl

    def GetValue(self):
        return None

    def SetValue(self,value):
        pass
gControlTypeRegister['static_line'] = StaticLine

class CheckList(wx.CheckListBox,FormControlBase):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        choices = FormControlUtil.convertList(BuilderUtil.getItemValue(item, 'choices', []))
        para['choices'] = choices
        itemCtrl = wx.CheckListBox.__init__(self,**para)
        windowControl.registItemHandler(self, para['id'], wx.EVT_CHECKLISTBOX,'evt_checklistbox')

    def GetValue(self):
        checked_list = wx.CheckListBox.GetChecked(self)
        value = []
        choices = FormControlUtil.convertList(BuilderUtil.getItemValue(self.item, 'choices', []))
        for index in checked_list:
            value.append(choices[index])
        return value

    def SetValue(self,value):
        choices = FormControlUtil.convertList(BuilderUtil.getItemValue(self.item, 'choices', []))
        value = FormControlUtil.convertList(value)
        if len(choices) < 1:
            return
        default_check = []
        if value != '':
            for check_item in value:
                if check_item in choices:
                    index = choices.index(check_item)
                    default_check.append(index)
        wx.CheckListBox.SetChecked(self,default_check)
gControlTypeRegister['check_list'] = CheckList

class List(wx.ListBox, FormControlBase):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        choices = FormControlUtil.convertList(BuilderUtil.getItemValue(item, 'choices', []))
        para['choices'] = choices
        itemCtrl = wx.ListBox.__init__(self,**para)
        windowControl.registItemHandler(self, para['id'], wx.EVT_LISTBOX,'evt_listbox')
        windowControl.registItemHandler(self, para['id'], wx.EVT_LISTBOX_DCLICK, 'evt_listbox_dclick')

    def GetValue(self):
        return wx.ListBox.GetStringSelection(self)

    def SetValue(self, value):
        choices = FormControlUtil.convertList(BuilderUtil.getItemValue(self.item, 'choices', []))
        if value in choices:
            index = choices.index(value)
            wx.ListBox.SetSelection(self,index)
gControlTypeRegister['list'] = List

class RadioBox(wx.RadioBox, FormControlBase):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        choices = FormControlUtil.convertList(BuilderUtil.getItemValue(item, 'choices', []))
        para['choices'] = choices
        para['majorDimension'] = int(BuilderUtil.getItemValue(item, 'columns', '1'))
        para['style'] = para['style'] | wx.RA_SPECIFY_COLS
        itemCtrl = wx.RadioBox.__init__(self,**para)
        windowControl.registItemHandler(self, para['id'], wx.EVT_RADIOBOX,'evt_radiobox')

    def GetValue(self):
        return wx.RadioBox.GetStringSelection(self)

    def SetValue(self,value):
        choices = FormControlUtil.convertList(BuilderUtil.getItemValue(self.item, 'choices', []))
        if value in choices:
            index = choices.index(value)
            wx.RadioBox.SetSelection(self,index)
gControlTypeRegister['radio_box'] = RadioBox


class Check(wx.CheckBox, FormControlBase):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        para['label'] = FormControlUtil.getLable(item)
        itemCtrl = wx.CheckBox.__init__(self,**para)
        windowControl.registItemHandler(self, para['id'], wx.EVT_CHECKBOX,'evt_checkbox')

    def GetValue(self):
        return 'true' if wx.CheckBox.GetValue(self) else 'false'

    def SetValue(self,value):
        if FormControlUtil.conventBool(value):
            wx.CheckBox.SetValue(self,True)
        else:
            wx.CheckBox.SetValue(self,False)
gControlTypeRegister['check'] = Check


class ComboBox(wx.ComboBox, FormControlBase):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        choices = FormControlUtil.convertList(BuilderUtil.getItemValue(item, 'choices', []))
        para['choices'] = choices
        itemCtrl = wx.ComboBox.__init__(self,**para)
        value = BuilderUtil.getItemValue(item, 'value', '')
        if FormControlUtil.conventBool(value):
            itemCtrl.SetValue(value)
        elif len(choices) > 0:
            wx.ComboBox.SetValue(self,choices[0])
gControlTypeRegister['combo_box'] = ComboBox

class Date(wx.DatePickerCtrl,FormControlBase):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        para['style'] = para['style'] | wx.DP_SHOWCENTURY | wx.DP_DEFAULT
        itemCtrl = wx.DatePickerCtrl.__init__(self,**para)

    def GetValue(self):
        return wx.DatePickerCtrl.GetValue(self).FormatISODate()

    def SetValue(self,value):
        if value != "":
            dt = wx.DateTime()
            dt.ParseDate(value)
            wx.DatePickerCtrl.SetValue(self,dt)
gControlTypeRegister['date'] = Date


class Time(wx.lib.masked.timectrl.TimeCtrl,FormControlBase):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        para['display_seconds'] = True
        para['fmt24hr'] = True
        para['oob_color'] = wx.NamedColour('Yellow')
        para['useFixedWidthFont'] = True
        wx.lib.masked.timectrl.TimeCtrl.__init__(self,**para)
gControlTypeRegister['time'] = Time


class DateTime(FormControlBase,DateTimeBase):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        DateTimeBase.__init__(self,**para)
gControlTypeRegister['datetime'] = DateTime


class Button(FormControlBase,wx.Button):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        para['label'] = FormControlUtil.getLable(item)
        wx.Button.__init__(self,**para)
        windowControl.registItemHandler(self, para['id'], wx.EVT_BUTTON,'evt_button')
    def GetValue(self):
        return None

    def SetValue(self,value):
        pass
gControlTypeRegister['button'] = Button


class File(FormControlBase,wx.lib.filebrowsebutton.FileBrowseButtonWithHistory):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        para['buttonText'] = 'Browse'
        para['dialogTitle'] = 'Choose a file'
        para['fileMask'] = BuilderUtil.getItemValue(item, 'mark', "*")
        para['labelText'] = FormControlUtil.getLable(item)
        para['style'] = para['style'] | wx.TAB_TRAVERSAL
        para['startDirectory'] = '.'
        para['fileMode'] = wx.FD_SAVE
        para['toolTip'] = 'Type filename or click browse to choose file'
        wx.lib.filebrowsebutton.FileBrowseButtonWithHistory.__init__(self,**para)
        self.SetHistory(FormControlUtil.convertList(BuilderUtil.getItemValue(item, 'choices')))
        windowControl.registItemHandler(self, para['id'],wx.EVT_BUTTON,'evt_button')
gControlTypeRegister['file'] = File


class Folder(FormControlBase,wx.lib.filebrowsebutton.DirBrowseButton):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        value = BuilderUtil.getItemValue(item, 'value', '')
        para['dialogTitle'] = 'Choose a folder'
        para['labelText'] = FormControlUtil.getLable(item)
        para['startDirectory'] = value
        para['style'] = para['style'] | wx.TAB_TRAVERSAL
        wx.lib.filebrowsebutton.DirBrowseButton.__init__(self,**para)
gControlTypeRegister['folder'] = Folder


class Folder(FormControlBase,wx.lib.filebrowsebutton.DirBrowseButton):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        value = BuilderUtil.getItemValue(item, 'value', '')
        para['dialogTitle'] = 'Choose a folder'
        para['labelText'] = FormControlUtil.getLable(item)
        para['startDirectory'] = value
        para['style'] = para['style'] | wx.TAB_TRAVERSAL
        wx.lib.filebrowsebutton.DirBrowseButton.__init__(self,**para)
gControlTypeRegister['folder'] = Folder

class MultiFiles(FormControlBase,MultiFolderFileBase):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        para['mask'] = BuilderUtil.getItemValue(item, 'mask', "*")
        para['bAddFile'] = True
        para['bAddFolder'] = False
        value = BuilderUtil.getItemValue(item, 'value', '')
        MultiFolderFileBase.__init__(self,**para)
gControlTypeRegister['multi_files'] = MultiFiles


class MultiFolders(FormControlBase,MultiFolderFileBase):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        para['mask'] = BuilderUtil.getItemValue(item, 'mask', "*")
        para['bAddFile'] = False
        para['bAddFolder'] = True
        value = BuilderUtil.getItemValue(item, 'value', '')
        MultiFolderFileBase.__init__(self,**para)
gControlTypeRegister['multi_folders'] = MultiFolders


class MultiFolersFiles(FormControlBase,MultiFolderFileBase):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        para['mask'] = BuilderUtil.getItemValue(item, 'mask', "*")
        para['bAddFile'] = True
        para['bAddFolder'] = True
        MultiFolderFileBase.__init__(self,**para)
gControlTypeRegister['multi_folders_files'] = MultiFolersFiles

class Table(FormControlBase,wx.ListCtrl):
    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        para['style'] = para['style'] | wx.LC_REPORT | wx.BORDER_SUNKEN
        itemCtrl = wx.ListCtrl.__init__(self,**para)
        tableList = BuilderUtil.getItemValue(item, 'data', [])
        columnList = FormControlUtil.convertList(BuilderUtil.getItemValue(item, 'columns', []))
        columnWidthList = FormControlUtil.convertList(BuilderUtil.getItemValue(item, 'columns_width', []))
        columnIndex = 0
        for column in columnList:
            width = -1
            if columnIndex < len(columnWidthList):
                width = int(columnWidthList[columnIndex])
            self.InsertColumn(columnIndex, column, width=width)
            columnIndex = columnIndex + 1
        item['indexMap'] = {}
        item['idMap'] = {}
        for line in tableList:
                index = self.GetItemCount()
                item['indexMap'][index] = line['id']
                item['idMap'][line['id']] = str(index)
                lineItems = FormControlUtil.convertList(line['items'])
                self.InsertStringItem(index, '')
                columnIndex = 0
                for lineitem in lineItems:
                    self.SetStringItem(index, columnIndex, lineitem)
                    columnIndex = columnIndex + 1
        windowControl.registItemHandler(self, para['id'],wx.EVT_LIST_ITEM_SELECTED,'evt_list_item_selected')
        windowControl.registItemHandler(self, para['id'],wx.EVT_LIST_ITEM_DESELECTED,'evt_list_item_deselected')
    def GetValue(self):
        select = wx.ListCtrl.GetFirstSelected(self)
        if select < 0:
            return None
        ret = []
        while select >= 0:
            ret.append(self.item['indexMap'][select])
            select = wx.ListCtrl.GetNextSelected(self,select)
        return ret
    def SetValue(self,value):
        valueList = FormControlUtil.convertList(value)
        for value in valueList:
            index = self.item['idMap'][str(value)]
            wx.ListCtrl.SetItemState(self,long(index), wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
gControlTypeRegister['table'] = Table


class Tree(FormControlBase,wx.TreeCtrl):
    def AddTree(self, parent,Node, idMap):
        if parent is None:
            nodeCtrl = self.AddRoot(Node['title'])
        else:
            nodeCtrl = self.AppendItem(parent, Node['title'])
        self.SetItemData(nodeCtrl, wx.TreeItemData(Node['id']))
        idMap[Node['id']] = nodeCtrl
        if Node['subNodes'] != []:
            for subNode in Node['subNodes']:
                self.AddTree(nodeCtrl, subNode,idMap)

    def __init__(self, item, parent, windowControl):
        FormControlBase.__init__(self, item,parent)
        para = FormControlUtil.makeCommonPara(item,parent)
        para['style'] = para['style'] | wx.TR_HAS_BUTTONS | wx.TR_MULTIPLE
        itemCtrl = wx.TreeCtrl.__init__(self,**para)
        treeData = BuilderUtil.getItemValue(item, 'data', [])
        item['idMap'] = {}
        self.AddTree(None, treeData, item['idMap'])
        windowControl.registItemHandler(self, para['id'],wx.EVT_TREE_SEL_CHANGED,'evt_tree_sel_changed')
    def GetValue(self):
        selects = wx.TreeCtrl.GetSelections(self)
        ret = []
        for select in selects:
            ret.append(wx.TreeCtrl.GetItemData(self,select).GetData())
        return ret
    def SetValue(self,value):
        valueList = FormControlUtil.convertList(value)
        for value in valueList:
            valueId = self.item['idMap'][str(value)]
            wx.TreeCtrl.SelectItem(self,valueId)
gControlTypeRegister['tree'] = Tree