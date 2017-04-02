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
import threading
from Queue import *
import traceback

EVENT_TYPE_APP_CLOSE = 1
EVENT_TYPE_WINDOW_CONTROL = 2
EVENT_TYPE_SUB_FORM_CLOSE = 3

EVENT_WORKTHREAD_UPDATE = 1
EVENT_WORKTHREAD_CLOSE = 2
EVENT_WORKTHREAD_SHOW = 3
EVENT_WORKTHREAD_SHOW_ITEM = 4
EVENT_WORKTHREAD_ENABLE_ITEM = 5
EVENT_WORKTHREAD_HIGHLIGHT_ITEM = 6
EVENT_WORKTHREAD_MESSAGEBOX = 7
EVENT_WORKTHREAD_CONFIRM_MESSAGEBOX = 8
EVENT_UITHREAD_HANDLER_FINISH = 9
EVENT_WORKTHREAD_ENABLE_MENU = 10
EVENT_WORKTHREAD_ITEM_SET_VALUE = 11
EVENT_WORKTHREAD_SHOWFORM = 12
EVENT_WORKTHREAD_MESSAGE = 13

def workThreadRunnable(workQueue):
        thread_stop = False
        returnState = False
        valueList= {}
        while not thread_stop:
            try:
                task = workQueue.get(block=True)
            except Queue.Empty:
                thread_stop = True
                break
            eventType =  task[0]
            windowHandler = task[1]
            para = task[2]
            if eventType == EVENT_TYPE_WINDOW_CONTROL:
                try:
                    para.handler(windowHandler,para)
                except Exception,ex:
                    traceback.print_exc()
                    windowHandler.showWindow(False)
                    raw_input("Press Enter Key to continue:")
                    windowHandler.showWindow(True)
                    #windowHandler.taskDone()
                if windowHandler.windowClosed:
                    returnState = windowHandler.returnOk
                    valueList = para.valueList
            elif  eventType == EVENT_TYPE_APP_CLOSE:
                break
            else:
                continue

            workQueue.task_done()
        return  returnState, valueList

#The work Thread for Form shown by handler
class SubFormThread(threading.Thread):
    def __init__(self, waitQueue):
        threading.Thread.__init__(self)
        self.queue = Queue(30)
        self.returnState = False
        self.valueList = {}
        self.waitQueue = waitQueue
    def run(self):
        self.returnState, self.valueList = workThreadRunnable(self.queue)
        self.waitQueue.put([EVENT_TYPE_SUB_FORM_CLOSE, None, None], block=True, timeout=None)
