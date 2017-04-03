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

import  copy
import uuid
from xml.dom.minidom import parse
import xml.dom.minidom
import  wx
from BuilderUtil import *

class Form():
    def __init__(self):
        self.lines = []
        self.window_conf = {'width':300,'height': 400,
                             'title':"",'style':'default'}
        self.menubar = None
    def setWindowPara(self,windowConf):
        self.window_conf = dict(self.window_conf, **windowConf)

    def getWindowConfig(self,key):
        if key in self.window_conf.keys():
            return self.window_conf[key]
        else:
            return None

    def addLine(self,line):
        for lineCheck in self.lines:
            if lineCheck == line:
                return
        self.lines.append(line)

    def setCtrlAttribute(self, paraName, paraValue):
        self.window_conf[paraName] = paraValue

    def format(self, builder):
        self.windowWidth = int(self.getWindowConfig('width'))
        self.windowHeight = int(self.getWindowConfig('height'))
        self.windowPosX = self.getWindowConfig('pos_x')
        self.title = self.getWindowConfig('title')
        self.style = self.getWindowConfig('style')
        screenSize = wx.DisplaySize()
        if self.windowPosX == None:
            self.windowPosX =  (screenSize[0] - self.windowWidth)/2
        else:
            self.windowPosX = int(self.windowPosX)
        self.windowPosY = self.getWindowConfig('pos_y')
        if self.windowPosY == None:
            self.windowPosY =  (screenSize[1] - self.windowHeight)/2
        else:
            self.windowPosY = int(self.windowPosY)

class Notebook():
    def __init__(self, id):
        self.panels = []
        self.id = id
        self.height = -1
    def addPanel(self,panel):
        self.panels.append(panel)
    def getPanels(self):
        return self.panels
    def setCtrlAttribute(self, paraName, paraValue):
        if paraName == 'height':
            self.height = int(paraValue)
    def format(self,builder,lineWidth):
        for panel in self.panels:
            panel.format(builder, lineWidth)

class Panel():
    PANEL_EDGE_WIDTH = 1
    def __init__(self, panelId):
        self.panelId = panelId
        self.panelName = ""
        self.lines = []
        self.visible = True
        self.enable = True
        self.height = -1
        self.width = -1
    def addLine(self,line):
        self.lines.append(line)
    def getPanelName(self):
        return  self.panelName
    def setCtrlAttribute(self, paraName, paraValue):
        if paraName == 'name':
            self.panelName = paraValue
        elif paraName == 'visible':
            self.visible = BuilderUtil.convertBool(paraValue)
        elif paraName == 'enable':
            self.enable = BuilderUtil.convertBool(paraValue)
        elif paraName == 'height':
            self.height = int(paraValue)
    def getLines(self):
        return  self.lines
    def format(self,builder,lineWidth):
        if self.width == -1:
            self.width = lineWidth
        for line in self.lines:
            line.format(builder, self.width - Panel.PANEL_EDGE_WIDTH *2)

class Line():
    def __init__(self, lineId):
        self.items = []
        self.lineId = lineId
        self.visible = True
        self.enable = True
        self.align = 'left'
        self.expand = False
        self.height = 0

    def addItem(self,item):
        if item is not None:
            self.items.append(item)

    def setCtrlAttribute(self, paraName, paraValue):
        if paraName == 'align':
            self.align = str(paraValue)
        elif paraName == 'visible':
            self.visible = BuilderUtil.convertBool(paraValue)
        elif paraName == 'enable':
            self.enable = BuilderUtil.convertBool(paraValue)
        elif paraName == 'height':
            self.height = int(paraValue)
        elif paraName == 'expand':
            self.expand = BuilderUtil.convertBool(paraValue)

    def format(self,builder, lineWidth):
        for item in self.items:
            if 'height' not in item.keys():
                item['height'] = "%d" % Builder.DEFAULT_LINE_HEIGHT
            if int(item['height']) > self.height:
                self.height = int(item['height'])
            if 'visible' not in item.keys():
                item['visible'] = "true"

class Menu():
    def __init__(self, id):
        self.subMenus = []
        self.enable = True
        self.title = ""
        self.hint = ""
        self.id = id
    def addSubMenu(self, id, title, hint):
        subMenu = Menu(id)
        subMenu.title = title
        subMenu.hint = hint
        self.subMenus.append(subMenu)
        return subMenu
    def setCtrlAttribute(self, paraName, paraValue):
        if paraName == 'hint':
            self.hint = paraValue
        elif paraName == 'title':
            self.title = paraValue
        elif paraName == 'enable':
            self.enable = BuilderUtil.convertBool(paraValue)
class Builder():
    DEFAULT_LINE_HEIGHT = -1
    DEFAULT_MENUBAR_HEIGHT = -1
    DEFAULT_BUTTON_WIDTH = 100
    DEFAULT_LINE_WIDTH_EDGE = 5
    DEFAULT_LINE_HEIGHT_SPACE = 5
    def __init__(self):
        self.form = Form()

        self.__menu_list = []
        self.all_menu_items = []
        self.bShowMenu = False

        self.handlerMap = {}
        self.defaultHandler = None

        self.__idMap = {}

        self.blockWhenIdError = True
        self.ctrlTypeRegist = {}

    def setDefaultHandler(self, handler):
        self.defaultHandler =handler

    def setCtrlAttribute(self, id, paraName, paraValue):
        if id in self.__idMap.keys():
            itemList = self.__idMap[id]
            for item in itemList:
                if isinstance(item, Line)  \
                    or isinstance(item, Panel) \
                    or isinstance(item, Notebook) \
                    or isinstance(item, Form) \
                    or isinstance(item, Menu):
                    item.setCtrlAttribute(paraName, paraValue)
                else:
                    item[paraName] = paraValue
                    '''
                    if isinstance(paraValue, bool):
                        item[paraName] = 'true' if paraValue else 'false'
                    elif isinstance(paraValue,list):
                        item[paraName] = ''
                        for itemCheck in paraValue:
                            item[paraName] = paraValue
                    else:
                        if paraName == 'choices':
                            item[paraName] = self.__getStrList(paraValue)
                        elif item['type'] == 'check_list' and paraName == 'value':
                            item[paraName] = self.__getStrList(paraValue)
                        else:
                            item[paraName] = str(paraValue)
                    '''

    def setCtrlHandler(self, Id, handler):
        self.handlerMap[Id] = handler

    def format(self):
        if len(self.__menu_list) > 0:
            self.bShowMenu = True
        self.form.format(self)

    def __addIdMap(self, id, item):
        if id in self.__idMap.keys():
            itemList = self.__idMap[id]
            for itemCheck in itemList:
                if itemCheck == item:
                    return
        else:
            self.__idMap[id] = []
        self.__idMap[id].append(item)
    def __getItem(self,id, type):
        ret = None
        if id in self.__idMap.keys():
            itemList = self.__idMap[id]
            for item in itemList:
                if isinstance(item, type):
                    ret = item
                    break
        return  ret
    def updateValue(self, valueList):
        for (k, v) in valueList.items():
            self.setCtrlAttribute(k,'value', v)

    def copy(self):
        return copy.deepcopy(self)

    def __xmlGetAttribute(self,node,attribute,default=""):
        if node.hasAttribute(attribute):
            return node.getAttribute(attribute)
        return default
    def __getStrList(self, str):
        strList = str.split(';')
        retList = []
        for item in strList:
            retList.append(item.replace('[semicolon]', ';'))
        return retList
    def __xmlItemNode2Item(self,itemNode):
        item = {}
        if itemNode.nodeName == '#text':
            return None
        item['type'] = itemNode.nodeName
        if itemNode.attributes is not None:
            for attr in itemNode.attributes._attrs:
                item[attr] = itemNode.getAttribute(attr)
                #if attr == 'choices':
                #    item[attr] = self.__getStrList(item[attr])
                #if item['type'] == 'check_list' and attr == 'value':
                #    item[attr] = self.__getStrList(item[attr])
        return item

    def __xmlAddMenu(self,menu, menuNode):
        if menuNode.nodeName == 'menu' or menuNode.nodeName == 'menubar':
            for item in menuNode.childNodes:
                if item.nodeName == 'menu':
                    menuId = self.__xmlGetAttribute(item, 'id', "%s" % uuid.uuid1())
                    title = self.__xmlGetAttribute(item, 'title', '')
                    hint = self.__xmlGetAttribute(item, 'hint', '')
                    subMenu = menu.addSubMenu(menuId, title, hint)
                    subMenu.enable = BuilderUtil.convertBool(self.__xmlGetAttribute(item, 'enable', True))
                    subMenu.visible = BuilderUtil.convertBool(self.__xmlGetAttribute(item, 'visible', True))
                    self.__addIdMap(menuId, subMenu)
                    self.__xmlAddMenu(subMenu,item)

    def __xmlParseLine(self, lineNode):
        lineId = self.__xmlGetAttribute(lineNode, 'id', "%s" % uuid.uuid1())
        line = self.__getItem(lineId, Line)
        if line is None:
            line = Line(lineId)
        self.__addIdMap(lineId, line)
        line.enable = BuilderUtil.convertBool(self.__xmlGetAttribute(lineNode, 'enable', True))
        line.visible = BuilderUtil.convertBool(self.__xmlGetAttribute(lineNode, 'visible', True))
        line.height = int(self.__xmlGetAttribute(lineNode, 'height', -1))
        line.align = str(self.__xmlGetAttribute(lineNode, 'align', 'align'))
        line.expand = BuilderUtil.convertBool(self.__xmlGetAttribute(lineNode, 'expand', False))
        for itemNode in lineNode.childNodes:
            item = self.__xmlItemNode2Item(itemNode)
            if item is not None:
                if 'id' in item.keys():
                    itemCheck = self.__getItem(item['id'], dict)
                    if itemCheck is not None \
                        and itemCheck['type'] != 'button' \
                        and  itemCheck['type'] != 'static' \
                        and itemCheck['type'] != 'static_line':
                            print('\033[1;31;40m' +"Error:Duplicated Id("+ item['id'] +"), Please fix it" + '\033[0m')
                            if self.blockWhenIdError:
                                raw_input("Press Enter key to continue...")
                    self.__addIdMap(item['id'], item)
                line.addItem(item)
        return line

    def __xmlParsePanel(self, panelNode):
        panelId = self.__xmlGetAttribute(panelNode, 'id', "%s" % uuid.uuid1())
        panel = self.__getItem(panelId, Panel)
        if panel is None:
            panel = Panel(panelId)
        self.__addIdMap(panelId, panel)
        panel.panelName = self.__xmlGetAttribute(panelNode, 'name')
        panel.height = int(self.__xmlGetAttribute(panelNode, 'height', -1))
        panel.width = int(self.__xmlGetAttribute(panelNode, 'width', -1))
        panel.enable = BuilderUtil.convertBool(self.__xmlGetAttribute(panelNode, 'enable', True))
        panel.visible = BuilderUtil.convertBool(self.__xmlGetAttribute(panelNode, 'visible', True))
        #self.panels.append(panel)
        for lineNode in panelNode.childNodes:
            if lineNode.nodeName == "line":
                panel.addLine(self.__xmlParseLine(lineNode))
        return panel

    def __xmlParseNotebook(self, notebookNode):
        id = self.__xmlGetAttribute(notebookNode, 'id', "%s" % uuid.uuid1())
        notebook = self.__getItem(id, Notebook)
        if notebook is None:
            notebook = Notebook(id)
        notebook.height = int(self.__xmlGetAttribute(notebookNode, 'height', -1))
        self.__addIdMap(id, notebook)
        for panelNode in notebookNode.childNodes:
            if panelNode.nodeName == "panel":
                notebook.addPanel(self.__xmlParsePanel(panelNode))
        return notebook

    def loadLayout(self, file):
        self.__init__()
        self.mergeLayout(file)

    def mergeLayout(self, file):
        DOMTree = xml.dom.minidom.parse(file)
        Data = DOMTree.documentElement
        if Data.nodeName == 'form':
            formNode = Data
            if formNode.attributes is not None:
                for attr in formNode.attributes._attrs:
                    self.form.window_conf[attr] = formNode.getAttribute(attr)

                for lineNode in formNode.childNodes:
                    if lineNode.nodeName == "line":
                        self.form.addLine(self.__xmlParseLine(lineNode))
                    elif lineNode.nodeName == "panel":
                        self.form.addLine(self.__xmlParsePanel(lineNode))
                    elif lineNode.nodeName == "notebook":
                        self.form.addLine(self.__xmlParseNotebook(lineNode))

        for menubarNode in Data.getElementsByTagName("menubar"):
            if self.form.menubar == None:
                self.form.menubar = Menu('')
            self.__xmlAddMenu(self.form.menubar, menubarNode)

    def registControlType(self, ctrlName, ctrlTypeRegist):
        self.ctrlTypeRegist[ctrlName] = ctrlTypeRegist
