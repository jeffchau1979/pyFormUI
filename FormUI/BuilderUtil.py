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
#from CommonCtrl import *
class BuilderUtil():
    def __init__(self):
        pass

    @staticmethod
    def convertStyle(style):
        ret = {}
        itemList = style.split(';')
        for item in itemList:
            keyValue = item.split(':')
            if len(keyValue) > 1:
                ret[keyValue[0]] = keyValue[1]
        return ret

    @staticmethod
    def convertBool(item):
        if isinstance(item, bool):
            return item
        return str(item).lower() == 'true'

    @staticmethod
    def getItemValue(item, key, defaultValue=""):
        if key in item.keys():
            return item[key]
        else:
            return defaultValue