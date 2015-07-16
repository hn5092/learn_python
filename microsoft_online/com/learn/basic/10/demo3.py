#coding=utf-8
'''
Created on 2015年6月22日

@author: Administrator
'''
while True:
    re = raw_input("enter text:")
    if re == 'stop' :
        break
    elif not re.isdigit() :
        print("bad!" *8)
    else:
        print int(re) **2
print ('bye')
    