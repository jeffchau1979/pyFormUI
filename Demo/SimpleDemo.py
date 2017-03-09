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

from FormUI import *

#Load layout xml file
builder = Builder()
builder.loadLayout('SimpleDemo.xml')

#Setup Handler
def OkButtonHandler(windowHandler, para):
    resultList = para['result_list']
    print resultList['id_text']['value']
    windowHandler.closeWindow()
builder.setCtrlHandler('id_ok', OkButtonHandler)

#Show FormUI
formUI = FormUI(builder)
formUI.show()
