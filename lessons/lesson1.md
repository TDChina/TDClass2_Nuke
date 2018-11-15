# 第1课 Nuke Python API及Nuke控件

## 第一部分：Nuke的开发文档

### 英文技术支持首页
* https://support.foundry.com/hc/en-us

### 中文技术支持首页
* https://support.foundry.com/hc/zh-cn

### Nukepedia
* http://www.nukepedia.com/

### Python Develop：更多的是了解开发方法和步骤
* 在线：https://learn.foundry.com/nuke/developers/11.2/pythondevguide/
* 下载：https://www.foundry.com/products/nuke/developers
* 介绍：
  * 基本结构
  * 检索方法
  * 常用部分
    * node
    * menu
    * thread
    * render
    * curve
    * panel

### Python Reference：更多的是了解可用的函数
* 在线：https://learn.foundry.com/nuke/developers/11.2/pythonreference/
* 下载：https://www.foundry.com/products/nuke/developers
  * 基本结构
  * 检索方法
  * 常用部分
    * nuke.Node
    * 各类knob
    * callback
    * node graph相关
    * 工程文件相关

### tcl：
* 在线：http://www.tcl.tk/man/tcl8.6/TclCmd/contents.htm
* 中文教程：https://www.yiibai.com/tcl
* 下载：Nuke安装包内置

### Hiero：
* 在线：https://learn.foundry.com/hiero/developers/11.1/HieroPythonDevGuide/
* 下载：https://www.foundry.com/products/nuke/developers

### 进阶文档（不讲）
* Blink Kernel
* NDK

## 第二部分：Nuke的基本开发架构及开发特点

### 架构
* Nuke自带的重新编译过的python interpreter及python标准库
* nuke、nukescripts、pyside2、hiero
* NDK和Blink Script
* Nuke节点对应的动态链接库和tcl

### 特点
* API简单直观
* 文档脉络清晰，便于查询
* 报错信息详尽且多为Python Error

## 第三部分：Nuke中写代码的位置

### 表达式
* tcl表达式
* python表达式

### Script Editor
* 按钮功能

### Custom knob
* Tcl Script Button
* Python Script Button
* Python Custom

## 第四部分：tcl学习及实例

### 字符串操作

### 列表操作

### 与python联用

## 第五部分：nuke python节点相关操作

### 节点树操作常用函数

* 获取某个节点
```python
nuke.selectedNode()ianhaovfx-patch-1
nuke.toNode()
```

* 创建节点
```python
# 两者区别请参考文档
nuke.createNode('node_class') 
nuke.nodes().NodeClass()
```

* 获取某个控件的值
```python
node['knob_name'].value()
```

* 设置某个控件的值
```python
node['knob_name'].setValue(value)
```

* 连接节点
```python
node.setInput(index, pre_node)
```

* 获取上游节点
```python
node.input(index)
```

* 工程相关
```python
nuke.Root().name()
nuke.knobDefault()
```

## nuke常用控件

* 获取knob类型
```python
type(node['knob_name'])
```

## 第六部分：nuke命令行执行

### nuke python interpreter与内置PySide2
Nuke和Maya一样有自带的重新编译过的python解释器，以及各种标准库，其自带的PySide2也是重新编译过的。

### nuke的命令行模式及nuke模块
nuke和nukescripts模块可以在标准python环境下被导入并使用，但是需要注意跟Nuke GUI相关的函数无法使用，
且由于编译版本不匹配的原因可能会存在未知的冲突，因此官方建议使用Nuke自带的python解释器来执行nuke python脚本，
并且命令行模式下不应包含任何GUI相关的代码

使用命令行运行Nuke Python解释器：
```shell
>nuke主程序路径 -t python脚本路径 参数
```
例子：
```shell
C:\Users\tianhao>"C:\Program Files\Nuke10.5v1\Nuke10.5.exe" -t C:\Users\tianhao\Desktop\nuke_hello.py "Hello Nuke!"
Nuke 10.5v1, 64 bit, built Dec  6 2016.
Copyright (c) 2016 The Foundry Visionmongers Ltd.  All Rights Reserved.
Hello Nuke!
```

### nuke的命令行参数
* https://learn.foundry.com/nuke/11.2/content/comp_environment/configuring_nuke/command_line_operations.html


## 第七部分：Callback
* https://learn.foundry.com/nuke/developers/11.2/pythondevguide/callbacks.html
### Callback的概念
将某一函数A的指针（在Python中即为函数对象本身）作为参数传递给另一个函数B，以便在B函数中通过该参数调用A函数，则称A函数为回调函数。

### 回调函数的优点
* 解耦：由于回调函数是以参数的形式传入，所以可以按需配置，而无需像普通调用一样写死在处理函数中
* 异步：回调多用于异步编程，即将回调函数注册为处理函数的回调后就可以去做别的事情了，等到处理函数执行到特定时刻自然会去调用回调函数

### 回调函数的缺点
* 参数类型不定：由于传入的回调函数A是不定的，因此无法保证函数B能够在调用函数A时赋予其正确的参数
* 回调地狱：层级过深，运行顺序被打乱

### 与信号-槽对比
* 信号和槽的参数类型是严格对应的
* 信号和槽完全解偶，两者互不知道对方的存在
* 回调函数总是在处理函数所在的线程中执行，槽函数可以在调用方所在线程或其他线程中执行

### Nuke常用的Callback
* OnCreate
* OnUserCreate
* OnScriptLoad
* OnScriptSave
* OnScriptClose
* beforeRender
* afterRender
* knobChanged

## 第八部分：Gizmo制作

### 如何创建多个输入
### 如何pick knob
### 如何为主界面添加自定义knob
### 如何在gizmo内部获取主界面knob的值
### 如何编写knobChanged Callbac
### 如何动态配置Gizmo中的参数

## 作业：
1. 制作一个slate gizmo
2. 编写一个Python脚本读取一个配置文件（配置文件中至少包含一个序列帧路径及起始、结束帧号）
3. 以第一步的gizmo为基础制作一个nuke工程，在工程的Root中设置OnScriptLoad，调用第二步的脚本，为Read节点、Root节点设置参数
4. 以Nuke命令行形式执行第三步的nuke工程，渲染出mov文件
