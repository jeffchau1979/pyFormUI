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
import os

builder = Builder()
builder.setWindowPara({'title': "Demo GUI", 'width': 500,'height':600,
                       'show_panel':True, 'show_system_button':True})

#Setup OK Handler
def OkButtonHandler(windowHandler, para):
    resultList = para['result_list']
    for k, v in resultList.iteritems():
        print "dict[%s]=" % k, v
    windowHandler.closeWindow()
builder.setOkButtonHandler(OkButtonHandler)

#Setup Form
builder.setPanelTitle("pid_nomal", "Normal")
builder.addItem("pid_nomal", "lid_0", {'id': 'id_type', 'title': "Title", 'type': 'static_line','align':'center'})
builder.addItem("pid_nomal", "lid_1", {'id': 'id_type11', 'title': "Type:", 'type': 'static'})

builder.addItem("pid_nomal", "lid_1", {'id': 'id_type21', 'title': "Type:", 'type': 'choise',
                 'choices': ['list', 'dump', 'package', 'remove', 'add', 'crunch', 's[ingleCrunch]'],
                 'value': 'dump'})
builder.addItem("pid_nomal", "lid_1", {'id': 'id_type1', 'title': "Type:", 'type': 'choise',
                 'choices': ['list', 'dump', 'package', 'remove', 'add', 'crunch', 's[ingleCrunch]'],
                 'value': 'dump'})
builder.addItem("pid_nomal", "lid_2", {'id': 'id_type2', 'title': "Type:", 'type': 'choise',
                 'choices': ['list', 'dump', 'package', 'remove', 'add', 'crunch', 's[ingleCrunch]'],
                 'value': 'dump'})
builder.addItem("pid_nomal", "lid_23", {'id': 'id_text','type': 'text',
                 'value': 'default text',
                 'multi_line':'true',
                 'password':'true',
                 'height':'100'})

builder.addItem("pid_nomal", "lid_3",{'id': 'id_check_list', 'title': "check list:", 'type': 'check_list',
                 'choices': ['list', 'dump', 'package', 'remove', 'add', 'crunch', 's[ingleCrunch]'],
                 'value': ['list', 'dump', 'package'],'height':'100'})
builder.addItem("pid_nomal", "lid_3",{'id': 'id_check_box', 'title': "check list:", 'type': 'radio_box',
                 'choices': ['list', 'dump', 'package', 'remove', 'add', 'crunch', 's[ingleCrunch]'],
                 'value': 'package','columns':'2'})
builder.addItem("pid_nomal", "lid_4",{'id': 'id_check', 'title': "Check:", 'type': 'check',
                 'value': 'true'})

builder.addItem("pid_nomal", "lid_5",{'id': 'id_combo_box', 'title': "combo_box:", 'type': 'combo_box',
                  'choices': ['list', 'dump', 'package', 'remove', 'add', 'crunch', 's[ingleCrunch]'],
                 'value': ''})

builder.addItem("pid_nomal", "lid_6",{'id': 'id_file', 'title': "File:", 'type': 'file',
                 'value': '/home',
                 'choices':['/home','/work'],'mark':"xls file(*.xls)|*.xls|Any File(*.*)|*.*"})

builder.addItem("pid_nomal", "test",{'id': 'id_multi_files', 'title': "File:", 'type': 'multi_files',
                 'value': '/home',
                 'height':'100'})

builder.addItem("pid_nomal", "lid_7",{'id': 'id_folder', 'title': "Select Folder:", 'type': 'folder',
                 'value': '/home',})

pid = FormUI.getUUIDString()
builder.setPanelTitle(pid, "Test")
#builder.setVisible(pid, False)
lid = FormUI.getUUIDString()
builder.addItem(pid, lid, {'id': 'id_date', 'title': "Select Date:", 'type': 'date',
                 'value': '2017-02-01','visible':'false'})
lid = FormUI.getUUIDString()
builder.addItem(pid, lid, {'id': 'id_time', 'title': "Select Date:", 'type': 'time',
                 'value': '10:01:01'})
lid = FormUI.getUUIDString()
builder.addItem(pid, lid, {'id': 'id_text_test', 'title': "Input Text:", 'type': 'text','value': 'default text'})
lid = FormUI.getUUIDString()
builder.addItem(pid, lid,{'id': 'id_datetime', 'title': "Select DateTime:", 'type': 'datetime','value': '2017-02-01 10:01:01'})

def button_handler(windowHandler, para):
    resultList = para['result_list']
    windowHandler.setValue('id_text', 'button onclick')
    ret = windowHandler.confirmMessageBox("ok button click", "title")
    print ret
lid = FormUI.getUUIDString()
builder.addItem(pid, lid,{'id': 'id_button', 'title': "Button", 'type': 'button','handler':button_handler})

#Setup Menu
builder.addMenuItem('File', '', 'id_menu_file')
def id_menu_file_handler(windowHandler, para):
    windowHandler.highlightItem('id_text')
builder.addMenuItem('MenuItem', 'MenuItem Help', 'id_menu_item','id_menu_file',id_menu_file_handler)

#Show FormUI
resultList = FormUI.loadCachedValue(os.path.expanduser('~') + "/.demo.cfg")
builder.updateValue(resultList)
formUI = FormUI(builder)
formUI.show()
formUI.saveCachedValue(os.path.expanduser('~') + "/.demo.cfg")
