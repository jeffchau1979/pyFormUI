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
from WorkThread import *
import Frame
import threading
import Queue
import  json
import uuid
modules ={u'Frame': [1, 'Main frame of Application', u'Frame.py']}

import warnings
warnings.filterwarnings("ignore",".*trying to remove*")

class FormDialogApp(wx.App):
    def __init__(self, parent, builder, workQueue):
        super(FormDialogApp, self).__init__(parent)
        self.main = Frame.create(None, builder, workQueue)
        if self.main.initSuccess:
            self.main.Show()
            self.SetTopWindow(self.main)

class UIThread(threading.Thread):
    def __init__(self, builder,workQueue):
        threading.Thread.__init__(self)
        self.workQueue = workQueue
        self.application = FormDialogApp(0, builder, workQueue)
    def run(self):
        self.application.MainLoop()

class FormUI():
    def __init__(self, builder):
        self.builder = builder
        self.returnState = False
    def show(self):
        queue = Queue.Queue(30)
        uiThread = UIThread(self.builder, queue)
        uiThread.start()
        self.returnState, self.valueList = workThreadRunnable(queue)

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

    def saveCachedValue(self, cachedValueFile, valueList = None):
        if valueList is None and self.returnState:
            valueList = self.valueList
        if valueList is None:
            return
        try:
            jsonContent = json.dumps(valueList)
            fileHandle = open(cachedValueFile, 'w')
            fileHandle.write(jsonContent)
            fileHandle.close()
        except IOError as err:
            print "write value configure file fail"

