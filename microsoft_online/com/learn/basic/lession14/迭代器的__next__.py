
'''
Created on 2015年7月6日

@author: Administrator
'''
# L = [1, 2, 3]
# I = iter(L)
# print(I.__next__())
# print(I.__next__())
# print(I.__next__())
# 
# #字典的內置迭代器
# D = {'a':1, 'b':2, 'c':3}
# for key in D.keys():
#     print (key,D[key])
# I = iter(D)
# print (next(I))
# print (next(I))

#range
# R = range(5)
# print(R)
# I = iter(R)
# print(next(I))
# print(next(I))
# print(next(I))


#enumerate
# E = enumerate('spam')
# I = iter(E)
# print(next(I))
# print(next(I))
# print(next(I))
# L = [1, 2, 3, 4, 5]
# for i in range(len(L)):
#     L[i] += 10
# print(L)
# L=[x+10 for x in L]  #运行速度更快 代码较少 是以C语言执行的
# print(L)

#在文件使用列表解析
# lines = [line.rstrip() for line in open('d:/data.txt')] #readlines 是全部读取到内存中再进行
# print(lines)
#  
# lines = [line.upper() for line in open('d:/data.txt')]
# print(lines)
# lines = [line.rstrip() for line in open('d:/data.txt') if line[0] == 'i'] #readlines 是全部读取到内存中再进行
# print(lines)

#多重的for语句
# l = [x+y for x in 'today' for y in 'qwert']
# print(l)
# l = [x+y for x in 'today' if x == 't' for y in 'qwert' if y =='w']
# print(l)

#map是一个可迭代对象
# m = map(str.upper, open('d:/data.txt'))
# print(map)
# list = [m]
# for i in m :
#     print( i)
# print(list)

#zip
# for i  in zip('abcd', 'efgh'):
#     print(i)

#一些常用的函数
# print (sum([3, 2, 4, 5, 6, 77, 12]))
# print(any(['', '', '1']))
# print(all(['1', '2', '3']))
# print(max([3, 2, 4, 5, 6, 77, 12]))
# print(min([3, 2, 4, 5, 6, 77, 12]))

# print(list(open('d:/data.txt')))
# print(tuple(open('d:/data.txt')))
# 'lie'.join(open('d:/data.txt'))
# a,*d = open('d:/data.txt')
# print(a)
# print(d)

# set(open('d:/data.txt'))

# print({key:value for key,value in enumerate(open('d:/data.txt'))})

#range区别 不是一个迭代器
# print(range(10))
# next(range(10))
#map zip D.keys D.values也是一样的 只生成了地址 没有生成所有的结果 节约内存空间

# d = {key:value for key,value in enumerate(open('d:/data.txt'))}
# print (d.keys)

