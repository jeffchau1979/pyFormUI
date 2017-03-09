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
def OkButtonHandler(windowHandler, para):
    resultList = para['result_list']
    cmd = ""
    if resultList['id_search_type']['value'] == "Default":
        cmd = cmd + " -name "
    elif resultList['id_search_type']['value'] == "Ignore Case":
        cmd = cmd + " -iname "
    elif resultList['id_search_type']['value'] == "Full Path":
        cmd = cmd + " -path "
        if not '*' in resultList['id_search']['value']:
            resultList['id_search']['value'] = "*" + resultList['id_search']['value'] + '*'
    cmd = cmd + "'" + resultList['id_search']['value'] + "'"

    if resultList['id_size_large']['value'] != "":
        cmd = cmd + " -size  +" + resultList['id_size_large']['value'] + resultList['id_size_large_unit']['value']
    if resultList['id_size_small']['value'] != "":
        cmd = cmd + " -size  -" + resultList['id_size_small']['value'] + resultList['id_size_small_unit']['value']

    if resultList['id_modify_after']['value'] != "":
        if resultList['id_modify_after_unit']['value'] == 'day':
            cmd = cmd + " -mtime +" + resultList['id_modify_after']['value']
        elif resultList['id_modify_after_unit']['value'] == 'min':
            cmd = cmd + " -mmin +" + resultList['id_modify_after']['value']

    if resultList['id_access_after']['value'] != "":
        if resultList['id_access_after_unit']['value'] == 'day':
            cmd = cmd + " -mtime +" + resultList['id_access_after']['value']
        elif resultList['id_access_after_unit']['value'] == 'min':
            cmd = cmd + " -mmin +" + resultList['id_access_after']['value']

    if resultList['id_type']['value'] != "any":
        valueMap = {}
        valueMap['file'] = 'f'
        valueMap['directory'] = 'd'

        cmd = cmd + " -type " + valueMap[resultList['id_type']['value']]

    if resultList['id_excute']['value'] != "":
        cmd = cmd + " -exec "+resultList['id_excute']['value']+" {} \;"

    if resultList['id_search_text']['value'] != "":
        cmd = cmd + " |xargs grep " + resultList['id_search_text']['value']

    if resultList['id_save_file']['value'] != "":
        cmd = cmd + "  > " + resultList['id_save_file']['value']

    windowHandler.closeWindow()
    paths = resultList['id_path']['value']
    paths = paths.split('\n')
    for path in paths:
        if path != '':
            print('\033[1;31;40m' + "Path:" + path + '\033[0m')
            gCmdLine ="find " + path + " " + cmd
            print(gCmdLine)
            subprocess.call([gCmdLine], shell=True)
builder.setCtrlHandler('id_btn_search', OkButtonHandler)

def GuiFind():
    resultList = FormUI.loadCachedValue(os.path.expanduser('~') + ".findgui.cfg")
    builder.updateValue(resultList)
    #builder.setValue('id_search_text','')
    formUI = FormUI(builder)
    formUI.show()
    formUI.saveCachedValue(os.path.expanduser('~') + ".findgui.cfg")
    #return gCmdLine
GuiFind()