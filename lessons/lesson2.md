# 第2课 Nuke菜单管理

## 第一部分：Nuke的两个Python入口脚本
Nuke启动的时候会自动加载两个默认的Python脚本：`init.py`和`menu.py`，其中`menu.py`仅在GUI模式下会被加载。
这两个文件默认存放在用户文件夹下的.nuke文件夹内，也可以放置到其他地方去，并通过`NUKE_PATH`环境变量指向目标文件夹来实现自动加载。
所有包含在这两个入口脚本中的Python代码都会在启动Nuke时被执行，因此必须确保代码无Bug，否则会导致Nuke启动时报错打不开。
通常也不建议直接在这两个入口脚本中定义函数、执行业务操作，普遍情况下，`init.py`被用于设置运行环境、设置节点默认值，加载额外的模块，而`menu.py`被用于添加自定义菜单。

## 第二部分：Nuke的三个加载路径
针对Nuke中用到的插件、脚本和Gizmo，有三个需要注意的加载路径

### NUKE_PATH
`NUKE_PATH`是一个环境变量，可以像`PATH`或`PYTHONPATH`一样添加多条路径，Nuke在启动时会依次搜索这些路径，并执行这些路径下所有的`init.py`和`menu.py`

### sys.path
这是Python标准的模块加载路径，所有包含于`sys.path`所列路径中的Python模块都可以直接import，作用与`PYTHONPATH`等同

### nuke.pluginPath()
这是Nuke内部用于加载插件、节点、Gizmo和图标的路径列表，所有包含在这些路径中的插件、节点、Gizmo都可以通过`nuke.createNode()`等方法来直接调用
对应的添加路径的函数式nuke.pluginAddPath()

## 第三部分：Nuke添加菜单的命令
注意添加菜单的层级结构，Command必须在Menu下

执行命令的两种方式：
* 字符串
* lambda
```python
m = nuke.menu('Nuke')
m.addMenu('Toolkit')
m.addCommand('Toolkit/test/test_command', "nuke.message(\'hello nuke\')", 'alt+o')

n = nuke.menu('Nodes')
c = n.addMenu('Custom')
c.addComamnd('Test Tool', lambda: func(args))
```

### 菜单相关的其他函数
```python
m.name()
m.findItem(sub_menu)
m.items()
m.removeItem(sub_menu)
```

## 第四部分：User工具箱制作
代码参见cases/lesson2