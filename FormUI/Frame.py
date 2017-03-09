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

def create(parent, builder, queue):
    return Frame(parent,builder, queue)

[wxID_DIALOG1BUTTONOK, wxID_DIALOG1BUTTONCANCEL] = [wx.NewId() for _init_ctrls in range(2)]

class Frame(wx.Frame,FormCtrl):
    def initWindowPara(self):
        self.form = self.builder.form

    def _init_ctrls(self, prnt):
        self.initWindowPara()
        self.windowInit = True
        #self.bCloseWindow = False
        self.notebook = None
        wx.Frame.__init__(self, id=wx.NewId(), name='', parent=prnt,
              pos=wx.Point(self.form.windowPosX, self.form.windowPosY), size=wx.Size(self.form.windowWidth, self.form.windowHeight),
              style=wx.DEFAULT_FRAME_STYLE & ~ wx.MAXIMIZE_BOX, title=self.form.title)
        self.SetClientSize(wx.Size(self.form.windowWidth, self.form.windowHeight))
        self.Center(wx.BOTH)
        self.update(None, True)
        self.windowHandler = WindowHandler(self)
        self.windowInit = False

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
        self.resultList = {}
        self.idPanelMap = {}
        self.initSuccess = True
        self.initDefaultSize(builder,parent)
        builder.format()
        self.builder = builder
        self.workQueue = workQueue
        self.uiQueue = Queue.Queue(30)
        self.handlerFinishQueue = Queue.Queue(1)
        self._init_ctrls(parent)
        EVT_RESULT(self, self.handlerWorkUIEvent)

    def updateDisplay(self, msg):
        """
        Receives data from thread and updates the display
        """
        t = msg.data
        if isinstance(t, int):
            self.displayLbl.SetLabel("Time since thread started: %s seconds" % t)
        else:
            self.displayLbl.SetLabel("%s" % t)
            self.btn.Enable()

    def showForm(self):
        self.SetTitle(self.form.title)
        self.SetPosition(wx.Point(self.form.windowPosX, self.form.windowPosY))
        self.SetSize(wx.Size(self.form.windowWidth, self.form.windowHeight))
        self.SetClientSize(wx.Size(self.form.windowWidth, self.form.windowHeight))
        FormCtrl.__init__(self, self.form, self.windowControl)

    def update(self, builder = None, updateWindow = False):
         if builder is not None:
            self.builder = builder
            if updateWindow:
                self.initWindowPara()
         if self.windowInit is False:
             self.DestroyForm()
         self.windowControl = WindowControl(self.builder.handlerMap, self)
         self.showForm()

    def CallFormHandler(self, id):
        if self.workQueue is not None:
            para = self.windowControl.makeReturnPara(id)

            if para['handler'] is not None or self.builder.defaultHandler is not None:
               if para['handler'] is not None:
                   self.workQueue.put([EVENT_TYPE_WINDOW_CONTROL, self.windowHandler, para], block=True, timeout=None)
               return True
        return False

    def handlerWorkUIEvent(self,msg):
       #waitting and deal the message from workThead
       para = msg.data
       eventType = para['event']
       if eventType == EVENT_WORKTHREAD_UPDATE:
            self.update(para['builder'], para['updateWindow'])
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
       elif eventType == EVENT_WORKTHREAD_HANDLER_FINISH:
            #if self.bCloseWindow:
            #    self.Close()
            return
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
