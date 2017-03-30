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
import wx
import wx.lib.masked.timectrl
import wx.lib.filebrowsebutton
from Builder import *
import os


def EnableSizer(item, bEnable):
    children = item.GetChildren()
    for child in children:
        widget = child.GetWindow()
        if widget is not None:
            widget.Enable(bEnable)
        elif isinstance(child, wx.SizerItem):
            EnableSizer(child.GetSizer(), bEnable)
'''
Todo:Add class ControlBase used as the base of all Customed Control
'''
class DateTime(wx.BoxSizer):
    ITEM_BORDER_WIDTH = 0
    def __init__(self,parent, pos, size,style=0,name='',id=''):
        wx.BoxSizer.__init__(self,wx.HORIZONTAL)
        self.m_datePicker = wx.DatePickerCtrl(parent, wx.NewId(), wx.DefaultDateTime,
                                               pos, wx.Size(0, size.height),
                                               wx.DP_DEFAULT)
        self.Add(self.m_datePicker, 1, wx.ALL|wx.EXPAND, self.ITEM_BORDER_WIDTH)

        self.m_time = wx.lib.masked.timectrl.TimeCtrl(display_seconds=True,
              fmt24hr=True, id=wx.NewId(),
              oob_color=wx.NamedColour('Yellow'), parent=parent,
              pos=pos,
              size=wx.Size(0, size.height),
              style=0, useFixedWidthFont=True)
        self.Add(self.m_time, 1, wx.ALL|wx.EXPAND, self.ITEM_BORDER_WIDTH)
    def GetValue(self):
        return self.m_datePicker.GetValue().FormatISODate() + " " + self.m_time.GetValue()
    def SetValue(self, value):
        valueList = value.split(" ")
        if len(valueList) > 1:
            dt = wx.DateTime()
            dt.ParseDate(valueList[0])
            self.m_datePicker.SetValue(dt)

            self.m_time.SetValue(valueList[1])
    def Enable(self, bEnable):
        EnableSizer(self, bEnable)
    def Show(self, bShow):
        self.ShowItems(bShow)
    def SetFocus(self):
        self.m_datePicker.SetFocus()

class MultiFolderFile(wx.BoxSizer):
    ITEM_BORDER_WIDTH = 0
    ITEM_BORDER_BUTTON_SPACE = 1
    def __init__(self,parent, pos, size,mask,bAddFile,bAddFolder,style=0,name='',id=''):
        self.parent = parent
        self.mask = mask
        self.addFile = bAddFile
        self.addFolder = bAddFolder
        wx.BoxSizer.__init__(self,wx.HORIZONTAL)

        self.m_textCtrl = wx.TextCtrl(parent, wx.ID_ANY, wx.EmptyString, pos,
                                      wx.Size(0, size.height), wx.TE_MULTILINE|wx.HSCROLL)
        self.Add(self.m_textCtrl, 1, wx.ALL|wx.EXPAND, self.ITEM_BORDER_WIDTH)

        self.selectButtonSizer = self.createSelectButtons(pos)
        self.Add(self.selectButtonSizer, 0, wx.ALL, self.ITEM_BORDER_WIDTH)
    def createSelectButtons(self,pos):
        selectButtonSizer = wx.BoxSizer(orient=wx.VERTICAL)
        if self.addFile:
            selectFildId = wx.NewId()
            self.m_buttonSelectFile = wx.Button(self.parent, selectFildId, "Add File",
                                                pos,
                                                wx.Size(Builder.DEFAULT_BUTTON_WIDTH - self.ITEM_BORDER_WIDTH * 2 -self.ITEM_BORDER_BUTTON_SPACE,
                                                        Builder.DEFAULT_LINE_HEIGHT), 0)
            selectButtonSizer.Add(self.m_buttonSelectFile, 0, wx.ALL, self.ITEM_BORDER_BUTTON_SPACE)
            self.m_buttonSelectFile.Bind(wx.EVT_BUTTON, self.OnButtonSelectFile, id=selectFildId)
        if  self.addFolder:
            selectFolderId = wx.NewId()
            self.m_buttonSelectFolder = wx.Button(self.parent, selectFolderId, "Add Folder",
                                                pos,
                                                wx.Size(Builder.DEFAULT_BUTTON_WIDTH - self.ITEM_BORDER_WIDTH * 2 - self.ITEM_BORDER_BUTTON_SPACE,
                                                        Builder.DEFAULT_LINE_HEIGHT), 0)
            selectButtonSizer.Add(self.m_buttonSelectFolder, 0, wx.ALL, self.ITEM_BORDER_BUTTON_SPACE)
            self.m_buttonSelectFolder.Bind(wx.EVT_BUTTON, self.OnButtonSelectFolder, id=selectFolderId)
        return selectButtonSizer
    def GetValue(self):
        return self.m_textCtrl.GetValue()
    def SetValue(self, value):
        self.m_textCtrl.SetValue(value)

    def OnButtonSelectFile(self, event):
        fileList = self.m_textCtrl.GetValue()
        fileList = fileList.split("\n")
        defaultFile = ''
        if len(fileList) > 0:
            defaultFile = fileList[-1]
        dlg = wx.FileDialog(self.parent, message="Select Files",
                            defaultDir='.',
                            defaultFile=defaultFile,
                            wildcard=self.mask,
                            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            for path in paths:
                if not path in fileList:
                    fileList.append(path)
            self.SetValue("\n".join(fileList))

    def getPath(self,path):
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.dirname(path)
    def OnButtonSelectFolder(self, event):
        fileList = self.m_textCtrl.GetValue()
        fileList = fileList.split("\n")
        defaultFile = ''
        if len(fileList) > 0:
            defaultFile = fileList[-1]
        dlg = wx.DirDialog(self.parent, "Select Folder", style=wx.DD_DEFAULT_STYLE)
        if defaultFile != '':
            dlg.SetPath(self.getPath(defaultFile))
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            if not path in fileList:
               fileList.append(path)
            self.SetValue("\n".join(fileList))
    def Enable(self, bEnable):
        EnableSizer(self, bEnable)
    def Show(self, bShow):
        self.ShowItems(bShow)
        #ShowSizer(self, bShow)
        #ShowSizer(self.selectButtonSizer, bShow)
    def SetFocus(self):
        self.m_textCtrl.SetFocus()

class StaticLine(wx.BoxSizer):
    STATIC_LINE_TEXT_EDGE = 20
    ITEM_BORDER_WIDTH = 0
    def __init__(self,parent, pos, size, label, style = wx.ALIGN_LEFT,name='',id=''):
        self.parent = parent
        wx.BoxSizer.__init__(self,wx.HORIZONTAL)

        if label == "":
            self.leftLine = wx.StaticLine(parent, wx.NewId(), wx.Point(0, 0), size,
                                          wx.LI_HORIZONTAL)
            self.Add(self.leftLine, 0, wx.ALL, 0)
        else:
            self.staticText = wx.StaticText(id=wx.NewId(),
                          label=label, name='', parent=parent,
                          pos=wx.Point(0, 0), size=wx.Size(-1, -1),
                          style=0)
            textSize = self.staticText.GetSize()
            leftLineWidth = 0
            rightLineWidth = 0
            leftProportion = 1
            rightProportion = 1
            if style & wx.ALIGN_CENTER != 0:
                pass
            elif style & wx.ALIGN_RIGHT != 0:
                rightLineWidth = StaticLine.STATIC_LINE_TEXT_EDGE
                rightProportion = 0
            else:
                leftLineWidth = StaticLine.STATIC_LINE_TEXT_EDGE
                leftProportion = 0
            self.leftLine = wx.StaticLine(parent, wx.NewId(), wx.Point(0, 0), wx.Size(leftLineWidth, textSize.height),wx.LI_HORIZONTAL)
            self.rightLine = wx.StaticLine(parent, wx.NewId(), wx.Point(0, 0), wx.Size(rightLineWidth, textSize.height),wx.LI_HORIZONTAL)
            self.Add(self.leftLine, leftProportion, wx.ALL | wx.EXPAND, self.ITEM_BORDER_WIDTH)
            self.Add(self.staticText, 0, wx.ALL, self.ITEM_BORDER_WIDTH)
            self.Add(self.rightLine, rightProportion, wx.ALL | wx.EXPAND, 0)
    def Enable(self, bEnable):
        EnableSizer(self, bEnable)
