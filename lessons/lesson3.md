# 第3课 Nuke中的GUI编程

## 第一部分：PythonPanel实例：Auto Write Path
**nukescripts.PythonPanel**

PythonPanel完全使用nuke内置的GUI控件，其界面制作方法与Gizmo制作中的Add Knob是一样的思路和方法，请对比以下代码与Gizmo制作中手动添加Custom Knob的异同。

```python
self.projectKnob = nuke.String_Knob('proj','Project:')
self.sequenceKnob = nuke.String_Knob('seq','Sequence:')
self.sequenceKnob.clearFlag(nuke.STARTLINE)
self.shotKnob = nuke.String_Knob('shot','Shot:')
self.shotKnob.clearFlag(nuke.STARTLINE)
self.taskKnob = nuke.String_Knob('task','Task Type:')
self.versionKnob = nuke.String_Knob('version','Version:')
self.versionKnob.clearFlag(nuke.STARTLINE)
self.formatKnob = nuke.Enumeration_Knob('format','File Type:',['exr', 'jpg', 'mov'])
self.formatKnob.clearFlag(nuke.STARTLINE)
self.nameKnob = nuke.String_Knob('name','File Name:')
self.pathKnob = nuke.File_Knob('path','Write Path:')
self.formatKnob.setValue('exr')

self.addKnob(self.projectKnob)
self.addKnob(self.sequenceKnob)
self.addKnob(self.shotKnob)
self.addKnob(self.taskKnob)
self.addKnob(self.versionKnob)
self.addKnob(self.formatKnob)
self.addKnob(self.nameKnob)
self.addKnob(self.pathKnob)

self.projectKnob.setEnabled(False)
self.sequenceKnob.setEnabled(False)
self.shotKnob.setEnabled(False)
self.taskKnob.setEnabled(False)
self.versionKnob.setEnabled(False)
```

### knobChanged函数
在修改完一个控件的值或状态后触发，会自动将该控件作为knob参数传入。

**注意：** 只有当鼠标切换到另一个控件时才会认为当前控件的修改已经完成，才会触发knobChanged函数。

### showModalDialog函数
PythonPanel中的`OK`和`Cancel`按钮是自带的，Modal即指的是独占模式的对话框，显示后无法再做别的事情。

### 一个很好用的测试正则表达式的网站
http://regex101.com

### 用字典批量为字符串pattern传值
```python
some_string_pattern.format(**a_dict)
```

## 第二部分：MVC编程实例：Element Loader
通过Qt自带的各种AbstractModel和AbstractView所构成的代码还不能称之为完全自主实现的MVC模式，因为Controller部分完全由Qt底层的C++接管。

真正的MVC设计模式中，Model、View、Controller三个类完全独立，互相不知道其他类的存在及实现方细节，也不存在互相Import的情况，而是在运行
时将Model实例和View实例传入Controller实例，由Controller实例控制View实例和Model实例进行互通，例如从View拿界面输入的数据，放入Model
进行计算处理，再将处理结果写回View。需要注意的是，Model通常包含数据相关的函数，可以作为一个独立的非Qt类而存在，Controller通常包含逻辑、
调度和操作相关的函数，同样不直接包含QtGui成分。

**难点：** 继承实现的自定义控件，以及动态添加的控件，如何在Controller中进行控制。

参考cases/lesson3/element_loader