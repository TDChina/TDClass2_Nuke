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

## 第二部分：如何用python操作Nuke节点树

### Script Editor
* 按钮功能

### 如何获取节点类型
```python
node.Class()
```

### 控件操作
```python
k = node['knob_name']
type(k)
k.value() # node['knob_name'].value()
k.setValue(value)
```

### 工程相关
```python
nuke.Root().name()
# 设置节点默认值
nuke.knobDefault()
```

### 节点树操作常用函数

获取某个节点
```python
nuke.selectedNode()
nuke.selectedNodes()
nuke.toNode()
```

创建节点
```python
# 两者区别请参考文档
nuke.createNode('node_class') 
nuke.nodes().NodeClass()
```

连接节点
```python
node.setInput(index, pre_node)
```

获取上游节点
```python
node.input(index)
```

Write节点渲染
```python
nuke.execute('Write_node_name', first, last, step)
```

### 综合案例
用Python快速导入想要的东西

## 第三部分：Nuke中写代码的位置
### 表达式
* tcl表达式
* python表达式

### Custom knob
* Tcl Script Button
* Python Script Button
* Python Custom

## 第四部分：tcl学习及实例 *（重点）*
### 字符串操作
如何用tcl语句从文件路径中裁切出所需的内容
* value
* file tail
* split
* lindex
* replace

### 与python联用
* message
* Add expression

## 第五部分：nuke命令行执行

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

## 第六部分：Gizmo制作

### Add Knob
### Pick knob
### 在gizmo内部获取主界面knob的值
```tcl
parent.knob_name
```