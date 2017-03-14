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

from FormUI import *
import os

builder = Builder()

#laod Layout

#builder.loadLayout('demo_menu.xml')
#builder.mergeLayout('demo_common.xml')
#builder.mergeLayout('demo_others.xml')
builder.loadLayout('demo.xml')

#Setup Handler
def OkButtonHandler(windowHandler, handlerPara):
    print(handlerPara.getEventId() + ":" + handlerPara.getEventType())
    valueList = handlerPara.valueList
    for k, v in valueList.iteritems():
        print "result[%s]=" % k, v
    windowHandler.update(builder,True)
    windowHandler.closeWindow()
builder.setCtrlHandler('id_ok', OkButtonHandler)

def cancelButtonHandler(windowHandler, handlerPara):
    windowHandler.closeWindow()
builder.setCtrlHandler('id_cancel', cancelButtonHandler)


def button_handler(windowHandler, handlerPara):
    #windowHandler.setValue('id_text', 'button onclick')
    #ret = windowHandler.confirmMessageBox("ok button click", "title")
    #windowHandler.enableCtrl('id_multi_files', False)
    #windowHandler.highlightItem('id_multi_files')
    #builder.setCtrlAttribute('id_text','width',100)
    builder.setCtrlAttribute('id_text', 'value', 'update builder')
    windowHandler.update(builder,True)
builder.setCtrlHandler('id_button', button_handler)

builderFind = Builder()
builderFind.loadLayout('findgui.xml')
def findOk(windowHandler, handlerPara):
    windowHandler.closeWindow()
builderFind.setCtrlHandler('id_btn_search', findOk)

def button_findgui_handler(windowHandler, handlerPara):
    state, valueList = windowHandler.showForm(builderFind,True)
    print valueList
builder.setCtrlHandler('id_button_findgui', button_findgui_handler)

def menu_handler(windowHandler, handlerPara):
    windowHandler.closeWindow()
builder.setCtrlHandler('id_menu', menu_handler)

def onlist(windowHandler, handlerPara):
    print(handlerPara.getEventType()+":" +handlerPara.getValue('id_list'))
builder.setCtrlHandler('id_list', onlist)

tableData = []
def AddTableLine(tableData, id, items):
    line = {}
    line['id'] = id
    line['items'] = items
    tableData.append(line)
AddTableLine(tableData,'1',"apple;1;red")
AddTableLine(tableData,'2',"orange;2;yellow")
AddTableLine(tableData,'3',"lemon;3;yellow")
AddTableLine(tableData,'4',"peach;4;pink")
builder.setCtrlAttribute('id_table','data', tableData)

def AddTreeNode(parent,id,title):
    node = {}
    node['id'] = id
    node['title'] = title
    node['subNodes'] = []
    if parent is not None:
        parent['subNodes'].append(node)
    return  node

treeData = AddTreeNode(None,'id_node','Node')
node1 = AddTreeNode(treeData, 'id_node1', 'Node1')
node2 = AddTreeNode(node1, 'id_node2', 'Node2')
node21 = AddTreeNode(node1, 'id_node21', 'Node21')
node22 = AddTreeNode(node1, 'id_node22', 'Node22')
node3 = AddTreeNode(node1, 'id_node3', 'Node3')
node4 = AddTreeNode(node3, 'id_node4', 'Node4')
node41 = AddTreeNode(node3, 'id_node41', 'Node41')
node42 = AddTreeNode(node3, 'id_node42', 'Node42')
builder.setCtrlAttribute('id_tree','data', treeData)

#Show FormUI
valueList = FormUI.loadCachedValue(os.path.expanduser('~') + "/.demo.cfg")
builder.updateValue(valueList)
formUI = FormUI(builder)
formUI.show()
formUI.saveCachedValue(os.path.expanduser('~') + "/.demo.cfg")
