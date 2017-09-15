========================================
pyFormUI -- A Simple Form GUI for python
========================================
pyFormUI provide the most easy way to show a Form Dialog for python,which is based on the cross-platform library wxPython.pyFormUI use xml file to design GUI, no any wxpython Knowledge is need when using pyFormUI.

<img src="https://github.com/jeffchau1979/pyFormUI/blob/master/screenshot/demo1.png">
<img src="https://github.com/jeffchau1979/pyFormUI/blob/master/screenshot/demo2.png">
<img src="https://github.com/jeffchau1979/pyFormUI/blob/master/screenshot/demo3.png">

Installation
------------
#### 1.install wxpython
```bash
  sudo apt-get install python-wxtools
```
#### 2.Download pyFormUI Source and Install pyFormUI from source:
```bash
cd pyFormUI_Source_Folder
python setup.py install
```

Simple Example:
------------
Please Find the code of this Example in files Demo/SimpleDemo.py and Demo/SimpleDemo.xml

<img src="https://github.com/jeffchau1979/pyFormUI/blob/master/screenshot/SimpleDemo.png">

#### 1.Create GUI by xml
```xml
<?xml version="1.0"?>
<form title="Demo GUI" width='500' height='100'>
   <line>
        <static title="Text:" width='50' />
        <text id='id_text'/>
   </line>
   <line align="right">
        <button id='id_ok' title='Ok'/>
   </line>
</form>
```
#### 2.Show GUI by xml layout
```python
from FormUI import *
builder = Builder()
builder.loadLayout('demo.xml')
formUI = FormUI(builder)
formUI.show()
```

#### 3.Add handler for button or other controls
```python
def OkButtonHandler(windowHandler, handlerPara):
    print handlerPara.getValue('id_text')
    windowHandler.closeWindow()
builder.setCtrlHandler('id_ok', OkButtonHandler)
```

More Demos
------------
Find more Demos in Demo Folder.

#### 1.Demo.py
```bash
  python Demo.py
```

  this demo show the basic control of pyFormUI

#### 2.FindGui.py
```bash
  python FindGui.py
```

  This Demo Implement the GUI for linux find cmd.
  
  <img src="https://github.com/jeffchau1979/pyFormUI/blob/master/screenshot/findgui.png">


#### 3.SimpleDemo.py
```bash
  python SimpleDemo.py
```

     A Simple Demo
   
#### 4.CustomControl.py
```bash
  python CustomControl.py
```

     A Demo Show how to add cutom control
     
      



