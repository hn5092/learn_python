#coding=utf-8
'''
Created on Aug 26, 2015

@author: imad
'''
##一定要对齐  对齐之后才能识别 尤其是-  和 :交叉使用的时候
import yaml
obj = yaml.load("""
- 1
- 2
- 3
- 4
""")
print obj


obj2 = yaml.load("""
-
 - 1
 - 2
 - 3
-
 - a
 - b
 - c
""")
print obj2

obj3 = yaml.load("""
hero:
  hp: 34
  sp: 8
  level: 11
orc:
  hp:11
  sp:12
  level:13
  """)
print obj3

obj4 = yaml.load("""
- hero:
   hp:34
   sp:8
   level:11
- orc:   
   hp:11 
   sp:12
   level:13 
""")
print obj4