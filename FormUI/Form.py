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
#from CommonCtrl import *
import wx.lib.filebrowsebutton
import Queue
from ControlRegister import  *

EVENT_TYPE_APP_CLOSE = 1
EVENT_TYPE_WINDOW_CONTROL = 2

EVENT_WORKTHREAD_UPDATE = 1
EVENT_WORKTHREAD_CLOSE = 2
EVENT_WORKTHREAD_SHOW = 3
EVENT_WORKTHREAD_SHOW_ITEM = 4
EVENT_WORKTHREAD_ENABLE_ITEM = 5
EVENT_WORKTHREAD_HIGHLIGHT_ITEM = 6
EVENT_WORKTHREAD_HANDLER_FINISH = 7
EVENT_WORKTHREAD_MESSAGEBOX = 8
EVENT_WORKTHREAD_CONFIRM_MESSAGEBOX = 9
EVENT_UITHREAD_HANDLER_FINISH = 10
EVENT_WORKTHREAD_ENABLE_MENU = 11
EVENT_WORKTHREAD_ITEM_SET_VALUE = 12

class WindowControl():
    def __init__(self, handlerMap, window):
        self.window = window
        self.handlerMap = handlerMap
        self.eventId2IdMap = {} #windowID: item_Id
        self.id2EventIdMap = {}
        self.id2CtrlMap = {}
        self.id2ItemMap = {}
        self.valueItems = []

    def registItem(self, id, eventId, item, control):
        if item is not None:
            if id not in self.id2ItemMap.keys():
                self.id2ItemMap[id] = []
            self.id2ItemMap[id].append(item)
            #if item['type'] != 'static' and item['type'] != 'static_line' and item['type'] != 'button':
            self.valueItems.append(item)

        if id not in self.id2CtrlMap.keys():
            self.id2CtrlMap[id] = []
        self.id2CtrlMap[id].append(control)

        if eventId is not None:
            self.eventId2IdMap[eventId] = id
            self.id2EventIdMap[id] = eventId

    def registItemHandler(self, ctrl, eventType, eventId):
        ctrl.Bind(eventType, self.OnItemEvent, id = eventId)

    def updateResult(self, resultList):
        global gControlRegister
        for item in self.valueItems:
            if item['type'] in gControlRegister.keys():
                item['value'] = gControlRegister[item['type']].onGetValue(item)
                if item['value'] is not None:
                    resultList[item['id']] = {'value':item['value'], 'type':item['type']}

    def setItemValue(self,itemId, value):
        if itemId not in self.id2CtrlMap.keys():
            return

        itemList = self.id2CtrlMap[itemId]
        for item in itemList:
            global gControlRegister
            if item['type'] in gControlRegister.keys():
                gControlRegister[item['type']].onSetValue(item, value)

    def enableCtrl(self,itemId, bEnable):
        if itemId in self.id2CtrlMap.keys():
            ctrlList =self.id2CtrlMap[itemId]
            for ctrl in ctrlList:
                ctrl.Enable(bEnable)

    def updateLayout(self, ctrl):
        if hasattr(ctrl, 'Layout'):
            ctrl.Layout()
        if isinstance(ctrl, PanelCtrl) or isinstance(ctrl,wx.Frame):
            return
        if hasattr(ctrl, 'parent'):
            self.updateLayout(ctrl.parent)

    def showCtrl(self,itemId, bShow):
        if itemId in self.id2CtrlMap.keys():
            ctrlList =self.id2CtrlMap[itemId]
            for ctrl in ctrlList:
                ctrl.Show(bShow)
                self.updateLayout(ctrl)
        #self.window.Layout()

    def highlightItem(self,itemId):
        if not itemId in self.id2CtrlMap.keys():
            return
        ctrlList = self.id2CtrlMap[itemId]
        for ctrl in ctrlList:
            if isinstance(ctrl, PanelCtrl):
                ctrl.noteboolCtrl.SetSelection(ctrl.panelIndex)
                break
            elif isinstance(ctrl, LineCtrl):
                panel = ctrl.parent
                if isinstance(panel, PanelCtrl):
                    panel.noteboolCtrl.SetSelection(panel.panelIndex)
                ctrl.highLight()
                break
            elif isinstance(ctrl, wx.Notebook):
                pass
            else:
                line = ctrl.parent
                panel = line.parent
                if isinstance(panel, PanelCtrl) and panel.panelIndex != None:
                    panel.noteboolCtrl.SetSelection(panel.panelIndex)
                ctrl.SetFocus()

    def makeReturnPara(self, id):
        para = {}
        para['id'] = id
        resultList = {}
        self.updateResult(resultList)
        para['result_list'] = resultList
        para['handler'] = None
        if para['id'] in self.handlerMap.keys():
           para['handler'] = self.handlerMap[para['id']]
        return  para

    def OnItemEvent(self, event):
        if event.Id in self.eventId2IdMap.keys():
            id = self.eventId2IdMap[event.Id]
            if id != None and id != '':
                self.window.CallFormHandler(id)

class CtrlBase():
    def __init__(self,windowControl,form):
        self.windowControl = windowControl
        self.form = form
        pass
    def createLine(self, line):
        lineSizer = LineCtrl(self, self.windowControl)
        self.windowSizer.AddSpacer(Builder.DEFAULT_LINE_HEIGHT_SPACE)
        lineSizer.initCtrls(self, line)
        flag = 0
        if line.align == 'center':
            flag = flag | wx.ALIGN_CENTER
        elif line.align == 'right':
            flag = flag | wx.ALIGN_RIGHT
        elif line.align == 'left':
            flag = flag | wx.ALIGN_LEFT
        self.windowSizer.AddWindow(lineSizer, 0, border=0, flag=flag)
#        if line.lineId != "":
#            self.idLineMap[line.lineId] = lineSizer
        if line.visible == False:
            lineSizer.Show(False)
    def createPanel(self,panel):
        eventId =  wx.NewId()
        panelControl = PanelCtrl(id=eventId, name=panel.panelId,
                                  parent=self,
                                  pos=wx.Point(0, 0),
                                  size=wx.Size(self.form.windowWidth, panel.height),
                                  lines=panel.getLines(),form=self.form,
                                  style=wx.TAB_TRAVERSAL, windowControl=self.windowControl
                                  )
        self.windowControl.registItem(panel.panelId, eventId, None, panelControl)
        self.windowSizer.AddWindow(panelControl, 0, border=0, flag=0)
        if panel.visible is False:
            panelControl.Show(False)
        if panel.enable is False:
            panelControl.Enable(False)
        panelControl.panelIndex = None
        panelControl.id = panel.panelId
        return panelControl
    def createNotebook(self, notebook):
        eventId = wx.NewId()
        notebookCtrl = wx.Notebook(id=eventId, name=notebook.id,
                                    parent=self,
                                    pos=wx.Point(0, 0), size=wx.Size(self.form.windowWidth, notebook.height),
                                    style=0)
        self.windowControl.registItem(notebook.id, eventId, None, notebookCtrl)
        self.windowSizer.AddWindow(notebookCtrl, 0, border=0, flag=0)
        panels = notebook.getPanels()
        panelIndex = 0
        for panel in panels:
            eventId = wx.NewId()
            panelControl = PanelCtrl(id=eventId, name=panel.panelId,
                                      parent=notebookCtrl,
                                      pos=wx.Point(0, 0),
                                      size=wx.Size(self.form.windowWidth, notebook.height),
                                      lines=panel.getLines(),form=self.form,
                                      style=wx.TAB_TRAVERSAL, windowControl=self.windowControl
                                      )
            self.windowControl.registItem(panel.panelId, eventId, None, panelControl)
            #self.idPanelMap[panel.panelId] = panelControl
            if panel.visible is False:
                panelControl.Show(False)
            if panel.enable is False:
                panelControl.Enable(False)
            notebookCtrl.AddPage(panelControl, panel.panelName)
            panelControl.panelIndex = panelIndex
            panelControl.noteboolCtrl = notebookCtrl
            panelIndex += 1
            panelControl.id = panel.panelId
            #self.panelList.append(panelControl)

    def showWindow(self,lines):
        edge = 5
        self.lineHeight = 29

        self.lines = lines
        self.windowSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.viewHeight = edge
        self.lineNum = 0
        for line in self.lines:
            if isinstance(line, Builder.Line):
                self.createLine(line)
            if isinstance(line, Builder.Panel):
                self.createPanel(line)
            if isinstance(line, Builder.Notebook):
                self.createNotebook(line)
        self.SetSizer(self.windowSizer)
        self.SetAutoLayout(1)
        if isinstance(self, PanelCtrl):
            self.SetupScrolling()


    def showMenu(self):
        menubarInfo = self.form.menubar
        if menubarInfo is None:
            return
        self.menuBar = wx.MenuBar()
        self.menuIdCtrlmap = {}
        self.menuCtrlIdMap = {}
        for submenuInfo in menubarInfo.subMenus:
            menu, type = self.createMenu(None, submenuInfo)
            self.menuBar.Append(menu, submenuInfo.title)

        self.menuBar.Show()
        self.SetMenuBar(self.menuBar)

        for submenuInfo in menubarInfo.subMenus:
            self.updateMenuEnable(submenuInfo)

    def createMenu(self, currentMenu, menuInfo):
        eventId = wx.NewId()
        if len(menuInfo.subMenus) > 0 or currentMenu == None:
            menu = wx.Menu()
            for submenuInfo in menuInfo.subMenus:
                submenu,type=self.createMenu(menu, submenuInfo)
                if type == 'menu':
                    menu.AppendMenu(eventId,submenuInfo.title,submenu)
                    self.windowControl.registItem(menuInfo.id, eventId, None, None)
                else:
                    menu.AppendItem(submenu)
            return menu,'menu'
        else:
            menuItem = wx.MenuItem(currentMenu, eventId, menuInfo.title, menuInfo.hint)
            self.windowControl.registItem(menuInfo.id, eventId, None, menuItem)
            self.windowControl.registItemHandler(self, wx.EVT_MENU, eventId)
            return menuItem,'item'

    def updateMenuEnable(self, menuInfo):
        if len(menuInfo.subMenus) > 0:
            if menuInfo.enable == False and menuInfo.id != '':
                if menuInfo.id in self.windowControl.id2EventIdMap.keys():
                    self.menuBar.Enable(self.windowControl.id2EventIdMap[menuInfo.id], False)
            for subMenuInfo in menuInfo.subMenus:
                self.updateMenuEnable(subMenuInfo)
        else:
            if menuInfo.enable == False:
                if menuInfo.id in self.windowControl.id2EventIdMap.keys():
                    self.menuBar.Enable(self.windowControl.id2EventIdMap[menuInfo.id], False)

class LineCtrl(wx.BoxSizer):
    def __init__(self,parent, windowControl):
        wx.BoxSizer.__init__(self,wx.HORIZONTAL)
        self.windowControl =  windowControl
        self.parent = parent
    def addItem(self,item):
        #flag = wx.ALIGN_LEFT
        #wx.ALIGN_RIGHT
        #wx.ALIGN_CENTER_HORIZONTAL
        self.AddWindow(item, 0, border=0, flag=0)
    def createMultiFolderFileControl(self, item,value,itemWidth, itemHeight,bAddFile,bAddFolder):
        item['control'] = MultiFolderFile(parent=self.parent,
                                   pos=wx.Point(0, 0),
                                   size=wx.Size(itemWidth, itemHeight),
                                   mask=getItemValue(item, 'mask', '*.*'),
                                   bAddFile=bAddFile, bAddFolder=bAddFolder)
        if value != "":
            item['control'].SetValue(value)
        #self.valueItems.append(item)
    def getAlign(self,item):
        if 'align' in item.keys():
            alignText = getItemValue(item,'align','left')
            if alignText == 'center':
                return  wx.ALIGN_CENTER
            elif alignText == 'right':
                return  wx.ALIGN_RIGHT
            elif alignText == 'left' :
                return  wx.ALIGN_LEFT
        return 0
    def createItem(self, lineSizer, item):
        global gControlRegister
        if item['type'] in gControlRegister.keys():
            item['control'] = gControlRegister[item['type']].onCreate(item, self.parent,self.windowControl)

        if 'visible' in item.keys():
            if item['visible'] == 'false':
                item['control'].Show(False)
            else:
                item['control'].Show(True)

        if 'enable' in item.keys():
            if getItemValue(item, 'enable', 'true') == 'true':
                item['control'].Enable(True)
            else:
                item['control'].Enable(False)
        #if 'id' in item.keys():
        #    self.idItemMap[item['id']] = item
        item['parent'] = self
        lineSizer.AddWindow(item['control'])
        if 'id' in item.keys():
            self.windowControl.registItem(item['id'], item['event_id'], item, item['control'])
        return True
    def initCtrls(self, parent, line):
        self.parent = parent
        for item in line.items:
            self.createItem(self, item)
    def Enable(self, bEnable):
        EnableSizer(self, bEnable)
    def Show(self, bShow):
        self.ShowItems(bShow)
    def highLight(self):
        children = self.GetChildren()
        for child in children:
            widget = child.GetWindow()
            if isinstance(widget, wx.BoxSizer):
                continue
            elif not isinstance(widget,wx.StaticText) and not isinstance(widget,StaticLine):
                widget.SetFocus()

class PanelCtrl(scrolled.ScrolledPanel,CtrlBase):
    def __init__(self, parent, id, pos, size, style, name,lines,form,windowControl):
        #scrolled.ScrolledPanel.__init__(self, parent, -1)
        self.form = form
        CtrlBase.__init__(self, windowControl,form)
        scrolled.ScrolledPanel.__init__(self, style=style, name=name,
                          parent=parent, pos=pos, id=id,
                          size=size)
        self.parent = self
        self.showWindow(lines)

class FormCtrl(CtrlBase):
    def __init__(self,form, windowControl):
        CtrlBase.__init__(self, windowControl, form)
        self.menuBar = None
        self.showMenu()
        self.showWindow(form.lines)

    def DestroyForm(self):
        self.windowSizer.DeleteWindows()
        if self.menuBar != None:
            self.SetMenuBar(None)
        self.Layout()

class WindowHandler():
    def __init__(self, window):
        self.window = window
        self.windowClosed = False
        self.returnOk = False

    def __setWaitHandler(self,para):
        para['syncTask'] = True
        self.window.handlerReturn = None

    def __waitHandlerFinish(self):
        try:
            task = self.window.handlerFinishQueue.get(block=True)
        except Queue.Empty:
            return
        self.window.handlerFinishQueue.task_done()
        return self.window.handlerReturn

    def closeWindow(self, returnOk = True):
        self.windowClosed = True
        self.returnOk = True
        self.window.uiQueue.put([EVENT_WORKTHREAD_CLOSE, None], block=True, timeout=None)

    def showWindow(self, bShow):
        para = {}
        para['bShow'] = bShow
        self.window.uiQueue.put([EVENT_WORKTHREAD_SHOW, para], block=True, timeout=None)

    def enableCtrl(self, itemId, bEnable):
        para = {}
        para['itemId'] = itemId
        para['bEnable'] = bEnable
        self.window.uiQueue.put([EVENT_WORKTHREAD_ENABLE_ITEM, para], block=True, timeout=None)

    def showCtrl(self, itemId, bShow):
        para = {}
        para['itemId'] = itemId
        para['bShow'] = bShow
        self.window.uiQueue.put([EVENT_WORKTHREAD_SHOW_ITEM, para], block=True, timeout=None)

    def setValue(self,itemId, value):
        para = {}
        para['itemId'] = itemId
        para['value'] = value
        self.window.uiQueue.put([EVENT_WORKTHREAD_ITEM_SET_VALUE, para], block=True, timeout=None)

    def update(self, builder, updateWindow):
        builder.format()
        para = {}
        para['builder'] = builder
        para['updateWindow'] = updateWindow
        self.window.uiQueue.put([EVENT_WORKTHREAD_UPDATE, para], block=True, timeout=None)

    def messageBox(self,message, caption):
        para = {}
        para['message'] = message
        para['caption'] = caption
        self.__setWaitHandler(para)
        self.window.uiQueue.put([EVENT_WORKTHREAD_MESSAGEBOX, para], block=True, timeout=None)
        self.__waitHandlerFinish()

    def confirmMessageBox(self,message, caption, bWithCancelButton=False):
        para = {}
        para['message'] = message
        para['caption'] = caption
        para['bWithCancelButton'] = bWithCancelButton
        self.__setWaitHandler(para)
        self.window.uiQueue.put([EVENT_WORKTHREAD_CONFIRM_MESSAGEBOX, para], block=True, timeout=None)
        ret = self.__waitHandlerFinish()
        if ret ==  wx.ID_YES:
            return 'yes'
        elif ret ==  wx.ID_NO:
            return 'no'
        else:
            return 'cancel'

    def highlightItem(self,itemId):
        #self.window.highlightItem(itemId)
        para = {}
        para['itemId'] = itemId
        self.window.uiQueue.put([EVENT_WORKTHREAD_HIGHLIGHT_ITEM, para], block=True, timeout=None)

    def getBuilder(self):
        return  self.window.builder