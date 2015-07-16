#coding=utf-8
'''
Created on 2015年7月16日

@author: Administrator
'''
#异常捕获
# l =[0, 1, 2, 3]
# for a in range(10):
#     try:
#         print l[a]
#     except IndexError,e:
#         try:
#             print g
#         except NameError,e:
#             print e
#         
#异常
l = [0, 1, 2, 3, 4]
for a in l:
    print a 
    if a == 3:
        raise IndexError,'下表越界'
#     print 'flag'
#final
# l =[0, 1, 2, 3]
# for a in range(10):
#     try:
#         print l[a]
#     except IndexError,e:
#         try:
#             print g
#         except NameError,e:
#             print e    
#         finally:print 'end'
#     
#else:    