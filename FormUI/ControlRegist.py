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
from ControlRegistBase import *

global gControlRegister
gControlRegister = {}
class StaticRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        para['label'] =  ControlRegistBase.getLable(item)
        itemCtrl = wx.StaticText(**para)
        return itemCtrl
gControlRegister['static'] = StaticRegist


class ChoiseRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item, parent)
        para['choices'] =  ControlRegistBase.convertList(BuilderUtil.getItemValue(item, 'choices', []))
        itemCtrl = wx.Choice(**para)
        value = BuilderUtil.getItemValue(item, 'value', '')
        windowControl.registItemHandler(itemCtrl, para['id'],wx.EVT_CHOICE,'evt_choice')
        return itemCtrl

    @staticmethod
    def onGetValue(item):
        choices = ControlRegistBase.convertList(BuilderUtil.getItemValue(item, 'choices', []))
        return choices[item['control'].GetSelection()]

    @staticmethod
    def onSetValue(item,value):
        choices = ControlRegistBase.convertList(BuilderUtil.getItemValue(item, 'choices', []))
        index = choices.index(value)
        if index >= 0:
            item['control'].Select(index)

gControlRegister['choise'] = ChoiseRegist


class TextRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        if 'multi_line' in item.keys() and BuilderUtil.getItemValue(item, 'multi_line') == 'true':
            para['style'] = para['style'] | wx.TE_MULTILINE
        if 'password' in item.keys() and BuilderUtil.getItemValue(item, 'password') == 'true':
            para['style'] = para['style'] | wx.TE_PASSWORD
        para['value'] =  BuilderUtil.getItemValue(item, 'value', '')
        itemCtrl = wx.TextCtrl(**para)
        return itemCtrl
gControlRegister['text'] = TextRegist


class StaticLineRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        para['label'] = ControlRegistBase.getLable(item)
        itemCtrl = StaticLine(**para)
        return itemCtrl
gControlRegister['static_line'] = StaticLineRegist


class CheckListRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        choices = ControlRegistBase.convertList(BuilderUtil.getItemValue(item, 'choices', []))
        para['choices'] = choices
        itemCtrl = wx.CheckListBox(**para)
        windowControl.registItemHandler(itemCtrl, para['id'], wx.EVT_CHECKLISTBOX,'evt_checklistbox')
        return itemCtrl
    @staticmethod
    def onGetValue(item):
        checked_list = item['control'].GetChecked()
        value = []
        choices = ControlRegistBase.convertList(BuilderUtil.getItemValue(item, 'choices', []))
        for index in checked_list:
            value.append(choices[index])
        return value
    @staticmethod
    def onSetValue(item,value):
        choices = ControlRegistBase.convertList(BuilderUtil.getItemValue(item, 'choices', []))
        value = ControlRegistBase.convertList(value)
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

class ListRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        choices = ControlRegistBase.convertList(BuilderUtil.getItemValue(item, 'choices', []))
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
        choices = ControlRegistBase.convertList(BuilderUtil.getItemValue(item, 'choices', []))
        if value in choices:
            index = choices.index(value)
            item['control'].SetSelection(index)
gControlRegister['list'] = ListRegist

class RadioBoxRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        choices = ControlRegistBase.convertList(BuilderUtil.getItemValue(item, 'choices', []))
        para['choices'] = choices
        para['majorDimension'] = int(BuilderUtil.getItemValue(item, 'columns', '1'))
        para['style'] = para['style'] | wx.RA_SPECIFY_COLS
        itemCtrl = wx.RadioBox(**para)
        windowControl.registItemHandler(itemCtrl, para['id'], wx.EVT_RADIOBOX,'evt_radiobox')
        return itemCtrl
    @staticmethod
    def onGetValue(item):
        return item['control'].GetStringSelection()
    @staticmethod
    def onSetValue(item,value):
        choices = ControlRegistBase.convertList(BuilderUtil.getItemValue(item, 'choices', []))
        if value in choices:
            index = choices.index(value)
            item['control'].SetSelection(index)
gControlRegister['radio_box'] = RadioBoxRegist


class CheckRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        para['label'] = ControlRegistBase.getLable(item)
        itemCtrl = wx.CheckBox(**para)
        windowControl.registItemHandler(itemCtrl, para['id'], wx.EVT_CHECKBOX,'evt_checkbox')
        return itemCtrl
    @staticmethod
    def onGetValue(item):
        return 'true' if item['control'].GetValue() else 'false'
    @staticmethod
    def onSetValue(item,value):
        if ControlRegistBase.conventBool(value):
            item['control'].SetValue(True)
        else:
            item['control'].SetValue(False)
gControlRegister['check'] = CheckRegist


class ComboBoxRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        choices = ControlRegistBase.convertList(BuilderUtil.getItemValue(item, 'choices', []))
        para['choices'] = choices
        itemCtrl = wx.ComboBox(**para)
        value = BuilderUtil.getItemValue(item, 'value', '')
        if ControlRegistBase.conventBool(value):
            itemCtrl.SetValue(value)
        elif len(choices) > 0:
            itemCtrl.SetValue(choices[0])
        return itemCtrl
gControlRegister['combo_box'] = ComboBoxRegist


class DateRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
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


class TimeRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        para['display_seconds'] = True
        para['fmt24hr'] = True
        para['oob_color'] = wx.NamedColour('Yellow')
        para['useFixedWidthFont'] = True
        itemCtrl =  wx.lib.masked.timectrl.TimeCtrl(**para)
        value = BuilderUtil.getItemValue(item, 'value', '')
        if value != "":
            itemCtrl.SetValue(value)
        return itemCtrl
gControlRegister['time'] = TimeRegist


class DateTimeRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        itemCtrl =  DateTime(**para)
        value = BuilderUtil.getItemValue(item, 'value', '')
        if value != "":
            itemCtrl.SetValue(value)
        return itemCtrl
gControlRegister['datetime'] = DateTimeRegist


class ButtonRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        para['label'] = ControlRegistBase.getLable(item)
        itemCtrl =  wx.Button(**para)
        windowControl.registItemHandler(itemCtrl, para['id'], wx.EVT_BUTTON,'evt_button')
        return itemCtrl
gControlRegister['button'] = ButtonRegist


class FileRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        para['buttonText'] = 'Browse'
        para['dialogTitle'] = 'Choose a file'
        para['fileMask'] = BuilderUtil.getItemValue(item, 'mark', "*.*")
        para['labelText'] = ControlRegistBase.getLable(item)
        para['style'] = para['style'] | wx.TAB_TRAVERSAL
        para['startDirectory'] = '.'
        para['fileMode'] = wx.SAVE
        para['toolTip'] = 'Type filename or click browse to choose file'
        if 'choices' in item.keys():
            itemCtrl =  wx.lib.filebrowsebutton.FileBrowseButtonWithHistory(**para)
            itemCtrl.SetHistory(ControlRegistBase.convertList(BuilderUtil.getItemValue(item, 'choices')))
        else:
            itemCtrl = wx.lib.filebrowsebutton.FileBrowseButton(**para)
        windowControl.registItemHandler(itemCtrl, para['id'],wx.EVT_BUTTON,'evt_button')
        return itemCtrl
gControlRegister['file'] = FileRegist


class FolderRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        value = BuilderUtil.getItemValue(item, 'value', '')
        para['dialogTitle'] = 'Choose a folder'
        para['labelText'] = ControlRegistBase.getLable(item)
        para['startDirectory'] = value
        para['style'] = para['style'] | wx.TAB_TRAVERSAL
        itemCtrl =   wx.lib.filebrowsebutton.DirBrowseButton(**para)
        return itemCtrl
gControlRegister['folder'] = FolderRegist


class FolderRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        value = BuilderUtil.getItemValue(item, 'value', '')
        para['dialogTitle'] = 'Choose a folder'
        para['labelText'] = ControlRegistBase.getLable(item)
        para['startDirectory'] = value
        para['style'] = para['style'] | wx.TAB_TRAVERSAL
        itemCtrl =   wx.lib.filebrowsebutton.DirBrowseButton(**para)

        return itemCtrl
gControlRegister['folder'] = FolderRegist


class MultiFilesRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        para['mask'] = BuilderUtil.getItemValue(item, 'mask', '*.*')
        para['bAddFile'] = True
        para['bAddFolder'] = False
        value = BuilderUtil.getItemValue(item, 'value', '')
        itemCtrl =  MultiFolderFile(**para)
        return itemCtrl
gControlRegister['multi_files'] = MultiFilesRegist


class MultiFoldersRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        para['mask'] = BuilderUtil.getItemValue(item, 'mask', '*.*')
        para['bAddFile'] = False
        para['bAddFolder'] = True
        value = BuilderUtil.getItemValue(item, 'value', '')
        itemCtrl =  MultiFolderFile(**para)
        return itemCtrl
gControlRegister['multi_folders'] = MultiFoldersRegist


class MultiFolersFilesRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        para['mask'] = BuilderUtil.getItemValue(item, 'mask', '*.*')
        para['bAddFile'] = True
        para['bAddFolder'] = True
        value = BuilderUtil.getItemValue(item, 'value', '')
        itemCtrl =  MultiFolderFile(**para)
        if value != "":
            itemCtrl.SetValue(value)
        return itemCtrl
gControlRegister['multi_folders_files'] = MultiFolersFilesRegist



class TableRegist(ControlRegistBase):
    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        para['style'] = para['style'] | wx.LC_REPORT | wx.BORDER_SUNKEN
        itemCtrl = wx.ListCtrl(**para)
        tableList = BuilderUtil.getItemValue(item, 'data', [])
        columnList = ControlRegistBase.convertList(BuilderUtil.getItemValue(item, 'columns', []))
        columnWidthList = ControlRegistBase.convertList(BuilderUtil.getItemValue(item, 'columns_width', []))
        columnIndex = 0
        for column in columnList:
            width = -1
            if columnIndex < len(columnWidthList):
                width = int(columnWidthList[columnIndex])
            itemCtrl.InsertColumn(columnIndex, column, width=width)
            columnIndex = columnIndex + 1
        item['indexMap'] = {}
        item['idMap'] = {}
        for line in tableList:
                index = itemCtrl.GetItemCount()
                item['indexMap'][index] = line['id']
                item['idMap'][line['id']] = str(index)
                lineItems = ControlRegistBase.convertList(line['items'])
                itemCtrl.InsertStringItem(index, '')
                columnIndex = 0
                for lineitem in lineItems:
                    itemCtrl.SetStringItem(index, columnIndex, lineitem)
                    columnIndex = columnIndex + 1
        windowControl.registItemHandler(itemCtrl, para['id'],wx.EVT_LIST_ITEM_SELECTED,'evt_list_item_selected')
        windowControl.registItemHandler(itemCtrl, para['id'],wx.EVT_LIST_ITEM_DESELECTED,'evt_list_item_deselected')
        return itemCtrl
    @staticmethod
    def onGetValue(item):
        select = item['control'].GetFirstSelected()
        if select < 0:
            return None
        ret = []
        while select >= 0:
            ret.append( item['indexMap'][select])
            select = item['control'].GetNextSelected(select)
        return ret
    @staticmethod
    def onSetValue(item,value):
        valueList = ControlRegistBase.convertList(value)
        for value in valueList:
            index = item['idMap'][str(value)]
            item['control'].SetItemState(long(index), wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
gControlRegister['table'] = TableRegist


class TreeRegist(ControlRegistBase):
    @staticmethod
    def AddTree(treeCtrl, parent,Node, idMap):
        if parent is None:
            nodeCtrl = treeCtrl.AddRoot(Node['title'])
        else:
            nodeCtrl = treeCtrl.AppendItem(parent, Node['title'])
        treeCtrl.SetItemData(nodeCtrl, wx.TreeItemData(Node['id']))
        idMap[Node['id']] = nodeCtrl
        if Node['subNodes'] != []:
            for subNode in Node['subNodes']:
                TreeRegist.AddTree(treeCtrl, nodeCtrl, subNode,idMap)

    @staticmethod
    def onCreate(item, parent, windowControl):
        para = ControlRegistBase.makeCommonPara(item,parent)
        para['style'] = para['style'] | wx.TR_HAS_BUTTONS | wx.TR_MULTIPLE
        itemCtrl = wx.TreeCtrl(**para)
        treeData = BuilderUtil.getItemValue(item, 'data', [])
        item['idMap'] = {}
        TreeRegist.AddTree(itemCtrl,None, treeData, item['idMap'])
        windowControl.registItemHandler(itemCtrl, para['id'],wx.EVT_TREE_SEL_CHANGED,'evt_tree_sel_changed')
        return itemCtrl
    @staticmethod
    def onGetValue(item):
        selects = item['control'].GetSelections()
        ret = []
        for select in selects:
            ret.append(item['control'].GetItemData(select).GetData())
        return ret
    @staticmethod
    def onSetValue(item,value):
        valueList = ControlRegistBase.convertList(value)
        for value in valueList:
            valueId = item['idMap'][str(value)]
            item['control'].SelectItem(valueId)
gControlRegister['tree'] = TreeRegist
