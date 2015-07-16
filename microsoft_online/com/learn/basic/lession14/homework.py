#coding = utf-8
'''
Created on 2015年7月8日

@author: Administrator
'''
file = open('d:\data.txt')
l = {}
for char in file.read():
    if char not in l:
        l[char] = 1
    else:
        l[char] += 1
else :
        print (l)