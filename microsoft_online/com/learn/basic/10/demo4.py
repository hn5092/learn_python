#coding=utf-8
'''
Created on 2015年6月22日

@author: Administrator
'''
while True:
    re = raw_input("enter text:")
    if re == 'stop':break
    try:
        re=int(re)
    except:
        print('bad!' *8)
    else:
        print (re ** 2)
print ('bye')