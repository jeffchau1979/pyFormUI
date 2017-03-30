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

from Form import *
import Queue
from WorkThread import *
from Builder import *
from BuilderUtil import *

def create(parent, builder, workQueue):
    return Frame(parent,builder, workQueue)

[wxID_DIALOG1BUTTONOK, wxID_DIALOG1BUTTONCANCEL] = [wx.NewId() for _init_ctrls in range(2)]

class Frame(wx.Frame,FormCtrl):
    def initWindowPara(self):
        self.form = self.builder.form

    def _init_ctrls(self, prnt):
        self.initWindowPara()
        self.windowInit = True
        #self.bCloseWindow = False
        self.notebook = None
        self.style = BuilderUtil.convertStyle(self.form.style)
        stylePara = self.__makeStylePara()
        wx.Frame.__init__(self, id=wx.NewId(), name='', parent=prnt,
              pos=wx.Point(self.form.windowPosX, self.form.windowPosY), size=wx.Size(self.form.windowWidth, self.form.windowHeight),
              style=stylePara, title=self.form.title)
        self.SetClientSize(wx.Size(self.form.windowWidth, self.form.windowHeight))
        self.Center(wx.BOTH)
        self.update(self.builder, True)
        self.windowHandler = WindowHandler(self)
        self.windowInit = False

    def __makeStylePara(self):
        if 'default' not in self.style.keys():
            stylePara = wx.DEFAULT_FRAME_STYLE
        else:
            stylePara = 0

        styleMap = {}
        styleMap['default'] = wx.DEFAULT_FRAME_STYLE
        styleMap['minimize_box'] = wx.MINIMIZE_BOX
        styleMap['maximize_box'] = wx.MAXIMIZE_BOX
        styleMap['system_menu'] = wx.SYSTEM_MENU
        styleMap['resize_box'] = wx.RESIZE_BOX
        styleMap['resize_border'] = wx.RESIZE_BORDER
        styleMap['stay_on_top'] = wx.STAY_ON_TOP
        styleMap['close_box'] = wx.CLOSE_BOX
        styleMap['iconize'] = wx.ICONIZE

        for (k, v) in self.style.items():
            if k not in styleMap.keys():
                continue
            if BuilderUtil.convertBool(v):
                stylePara = stylePara | styleMap[k]
            else:
                stylePara = stylePara & ~ styleMap[k]

        return stylePara

    def initDefaultSize(self, builder,parent):
        if wx.VERSION[0] < 3:
            mesureButton = wx.Button(parent, -1, "Mesure")
            Builder.DEFAULT_LINE_HEIGHT = mesureButton.GetDefaultSize().y
            mesureButton.Destroy()
        else:
            Builder.DEFAULT_LINE_HEIGHT = wx.Button.GetDefaultSize().y
        menuBar = wx.MenuBar()
        Builder.DEFAULT_MENUBAR_HEIGHT = menuBar.GetSize().y
        menuBar.Destroy()

    def __init__(self, parent, builder,workQueue):
        self.valueList = {}
        self.idPanelMap = {}
        self.initSuccess = True
        self.initDefaultSize(builder,parent)
        builder.format()
        self.builder = builder
        self.workQueue = workQueue
        self.handlerFinishQueue = Queue(1)
        self._init_ctrls(parent)
        EVT_RESULT(self, self.handlerWorkUIEvent)
        self.Bind(wx.EVT_CLOSE, self.OnFrameClose)

    def showMainForm(self):
        self.SetTitle(self.form.title)
        self.SetPosition(wx.Point(self.form.windowPosX, self.form.windowPosY))
        self.SetSize(wx.Size(self.form.windowWidth, self.form.windowHeight))
        self.SetClientSize(wx.Size(self.form.windowWidth, self.form.windowHeight))
        size = self.GetSize()
        FormCtrl.__init__(self, self.form, self.windowControl)

    def update(self, builder = None, updateWindow = False):
         if builder is not None:
            self.builder = builder
            if updateWindow:
                self.initWindowPara()
         if self.windowInit is False:
             self.DestroyForm()
         for (k,v) in builder.ctrlRegist.items():
             gControlRegister[k] = v
         self.windowControl = WindowControl(self.builder.handlerMap, self)
         self.showMainForm()

    def onsubFormExit(self, workThread):
        pass

    def showForm(self, builder,workThread):
        form = create(None, builder, workThread.queue)
        if form.initSuccess:
            form.Show()
            wx.GetApp().SetTopWindow(form)
            workThread.start()

    def CallFormHandler(self, id,eventType):
        if self.workQueue is not None:
            ctrlHandler = None
            if id in self.windowControl.handlerMap.keys():
                ctrlHandler = self.windowControl.handlerMap[id]
            if ctrlHandler is not None or self.builder.defaultHandler is not None:
               if ctrlHandler is not None:
                   para = self.windowControl.makeReturnPara(id,eventType,ctrlHandler)
                   self.workQueue.put([EVENT_TYPE_WINDOW_CONTROL, self.windowHandler, para], block=True, timeout=None)
               if  self.builder.defaultHandler is not None:
                   para = self.windowControl.makeReturnPara(id,eventType,self.builder.defaultHandler)
                   self.workQueue.put([EVENT_TYPE_WINDOW_CONTROL, self.windowHandler, para], block=True, timeout=None)

               return True
        return False

    def handlerWorkUIEvent(self,msg):
       para = msg.data
       eventType = para['event']
       if eventType == EVENT_WORKTHREAD_UPDATE:
            self.update(para['builder'], para['updateWindow'])
       elif eventType == EVENT_WORKTHREAD_SHOWFORM:
           self.showForm(para['builder'], para['workThread'])
       elif eventType == EVENT_WORKTHREAD_CLOSE:
           self.Close()
       elif eventType == EVENT_WORKTHREAD_SHOW:
           self.Show(para['bShow'])
           wx.GetApp().SetTopWindow(self)
       elif eventType == EVENT_WORKTHREAD_ENABLE_ITEM:
           self.windowControl.enableCtrl(para['itemId'],para['bEnable'])
           wx.GetApp().SetTopWindow(self)
       elif eventType == EVENT_WORKTHREAD_SHOW_ITEM:
           self.windowControl.showCtrl(para['itemId'], para['bShow'])
           wx.GetApp().SetTopWindow(self)
       elif eventType == EVENT_WORKTHREAD_ITEM_SET_VALUE:
           self.windowControl.setItemValue(para['itemId'], para['value'])
       elif eventType == EVENT_WORKTHREAD_HIGHLIGHT_ITEM:
           self.windowControl.highlightItem(para['itemId'])
       elif eventType == EVENT_WORKTHREAD_MESSAGEBOX:
            style = wx.OK | wx.ICON_INFORMATION | wx.STAY_ON_TOP
            wx.MessageBox(message=para['message'], caption=para['caption'], style= style, parent=self)
       elif eventType == EVENT_WORKTHREAD_CONFIRM_MESSAGEBOX:
            style = wx.YES_NO | wx.ICON_INFORMATION | wx.STAY_ON_TOP
            if para['bWithCancelButton']:
                style = style | wx.CANCEL
            ret = wx.MessageBox(message=para['message'], caption=para['caption'], style= style, parent=self)
       else:
           pass
       if para and 'syncTask' in para.keys() and para['syncTask'] == True:
           self.handlerFinishQueue.put([EVENT_UITHREAD_HANDLER_FINISH], block=True, timeout=None)

    def OnFrameClose(self, event):
        self.workQueue.put([EVENT_TYPE_APP_CLOSE, None, None], block=True, timeout=None)
        event.Skip()
