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
import Frame
import threading
import Queue
import  json
import uuid
modules ={u'Frame': [1, 'Main frame of Application', u'Frame.py']}

import warnings
warnings.filterwarnings("ignore",".*trying to remove*")

class FormDialogApp(wx.App):
    def __init__(self, parent, builder, queue):
        super(FormDialogApp, self).__init__(parent)
        self.main = Frame.create(None, builder, queue)
        if self.main.initSuccess:
            self.main.Show()
            self.SetTopWindow(self.main)

class UIThread(threading.Thread):
    def __init__(self, builder,queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.application = FormDialogApp(0, builder, queue)
    def run(self):
        self.application.MainLoop()
        self.queue.put([EVENT_TYPE_APP_CLOSE,None,None], block=True, timeout=None)

class FormUI():
    def __init__(self, builder):
        self.builder = builder
        self.returnOK = False
    def show(self):
        queue = Queue.Queue(30)
        uiThread = UIThread(self.builder, queue)
        uiThread.start()
        thread_stop = False
        while not thread_stop:
            try:
                task = queue.get(block=True)
            except Queue.Empty:
                thread_stop = True
                break
            eventType =  task[0]
            windowHandler = task[1]
            para = task[2]
            if eventType == EVENT_TYPE_WINDOW_CONTROL:
                if 'handler' in para.keys():
                    para['handler'](windowHandler,para)
                    #windowHandler.taskDone()
                    if windowHandler.windowClosed:
                        self.returnOK = windowHandler.returnOk
                        self.resultList = para['result_list']
                    else:
                        windowHandler.window.uiQueue.put([EVENT_WORKTHREAD_HANDLER_FINISH, None], block=True, timeout=None)
            elif  eventType == EVENT_TYPE_APP_CLOSE:
                break
            else:
                continue

            queue.task_done()

    @staticmethod
    def getUUIDString():
        return  "%s" % uuid.uuid1()

    @staticmethod
    def loadCachedValue(cachedValueFile):
        cachedValue = {}
        try:
            fileHandle = open(cachedValueFile)
            jsonContent = fileHandle.read()
            fileHandle.close()
            cachedValue = json.loads(jsonContent)
        except IOError as err:
            print "read value configure file fail!"
        return cachedValue

    def saveCachedValue(self, cachedValueFile, resultList = None):
        if resultList is None and self.returnOK:
            resultList = self.resultList
        if resultList is None:
            return
        try:
            jsonContent = json.dumps(resultList)
            fileHandle = open(cachedValueFile, 'w')
            fileHandle.write(jsonContent)
            fileHandle.close()
        except IOError as err:
            print "write value configure file fail"
