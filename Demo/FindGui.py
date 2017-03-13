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
import sys
sys.path.append('../')

import wx
from FormUI import *
import subprocess
import os
import sys

builder = Builder()

#laod Layout
builder.loadLayout(os.path.split(os.path.realpath(__file__))[0] + os.path.sep + 'findgui.xml')

#setup Handler
def OkButtonHandler(windowHandler, handlerPara):    
    cmd = ""
    id_search = handlerPara.getValue('id_search')
    if handlerPara.getValue('id_search_type') == "Default":
        cmd = cmd + " -name "
    elif handlerPara.getValue('id_search_type') == "Ignore Case":
        cmd = cmd + " -iname "
    elif handlerPara.getValue('id_search_type') == "Full Path":
        cmd = cmd + " -path "
        if not '*' in handlerPara.getValue('id_search'):
            id_search = "*" + handlerPara.getValue('id_search') + '*'
    cmd = cmd + "'" + id_search + "'"

    if handlerPara.getValue('id_size_large') != "":
        cmd = cmd + " -size  +" + handlerPara.getValue('id_size_large') + handlerPara.getValue('id_size_large_unit')
    if handlerPara.getValue('id_size_small') != "":
        cmd = cmd + " -size  -" + handlerPara.getValue('id_size_small') + handlerPara.getValue('id_size_small_unit')

    if handlerPara.getValue('id_modify_after') != "":
        if handlerPara.getValue('id_modify_after_unit') == 'day':
            cmd = cmd + " -mtime +" + handlerPara.getValue('id_modify_after')
        elif handlerPara.getValue('id_modify_after_unit') == 'min':
            cmd = cmd + " -mmin +" + handlerPara.getValue('id_modify_after')

    if handlerPara.getValue('id_access_after') != "":
        if handlerPara.getValue('id_access_after_unit') == 'day':
            cmd = cmd + " -mtime +" + handlerPara.getValue('id_access_after')
        elif handlerPara.getValue('id_access_after_unit') == 'min':
            cmd = cmd + " -mmin +" + handlerPara.getValue('id_access_after')

    if handlerPara.getValue('id_type') != "any":
        valueMap = {}
        valueMap['file'] = 'f'
        valueMap['directory'] = 'd'

        cmd = cmd + " -type " + valueMap[handlerPara.getValue('id_type')]

    if handlerPara.getValue('id_excute') != "":
        cmd = cmd + " -exec "+handlerPara.getValue('id_excute')+" {} \;"

    if handlerPara.getValue('id_search_text') != "":
        cmd = cmd + " |xargs grep " + handlerPara.getValue('id_search_text')

    if handlerPara.getValue('id_save_file') != "":
        cmd = cmd + "  > " + handlerPara.getValue('id_save_file')

    windowHandler.closeWindow()
    paths = handlerPara.getValue('id_path')
    paths = paths.split('\n')
    for path in paths:
        if path != '':
            print('\033[1;31;40m' + "Path:" + path + '\033[0m')
            gCmdLine ="find " + path + " " + cmd
            print(gCmdLine)
            subprocess.call([gCmdLine], shell=True)
builder.setCtrlHandler('id_btn_search', OkButtonHandler)

def GuiFind():
    valueList = FormUI.loadCachedValue(os.path.expanduser('~') + ".findgui.cfg")
    builder.updateValue(valueList)
    #builder.setValue('id_search_text','')
    formUI = FormUI(builder)
    formUI.show()
    formUI.saveCachedValue(os.path.expanduser('~') + ".findgui.cfg")
    #return gCmdLine
GuiFind()