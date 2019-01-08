# -*- coding: UTF-8 -*-
import nuke
import time

# r1.setValue()

# r2 = nuke.nodes.Read(file="D:/TDclass/pipeline/aaa/shuchu.%04d.jpg" )
# r2['first'].setValue(100)
# r2['last'].setValue(500)

# 新建一个read节点，把素材导入进来，设好起始帧、结束帧
r1 = nuke.nodes.Read(file="D:/TDclass/pipeline/aaa/shuchu.%04d.jpg",first ='0100',last = '0500' )
#创建gizimao
#创建一个group
#在group中创建3个text，设置text内容
#连接group的输入输出
g = nuke.createNode('Group')
g.begin()
i = nuke.createNode('Input')
name = nuke.createNode('Text')
name['name'].setValue('name')
name['message'].setValue('[lindex [split [file tail [value Read1.file]] . ] 0 ]')
name['color'].setValue([0.0,0.0,0.0,0.0])
name['translate'].setValue([-250.0,-300.0])
name['box'].setValue([250.0,50.0,1024,768])
time1 = nuke.createNode('Text')
time1['name'].setValue('time1')
time1['message'].setValue('[python {time.strftime(\'%Y-%m-%d\')}]')
time1['color'].setValue([0.0,0.0,0.0,0.0])
time1['translate'].setValue([-40.0,-300.0])
time1['box'].setValue([250.0,50.0,1024,768])
time2 = nuke.createNode('Text')
time2['name'].setValue('timecode')
time2['message'].setValue('[metadata input/frame]')
time2['color'].setValue([0.0,0.0,0.0,0.0])
time2['translate'].setValue([300.0,-300.0])
time2['box'].setValue([250.0,50.0,1024,768])
o =nuke.createNode('Output')
g.end()
g.setInput(0,r1)
#创建输出节点，设置输出格式、输出位置、输出帧范围
w = nuke.createNode("Write")
w['file_type'].setValue('mov')
w['meta_codec'].setValue('mp4v')
w['file'].setValue('D:/TDclass/pipeline/aaa/aaa.mov')
w['create_directories'].setValue('True')
nuke.execute('Write1',100,400,1)


