#coding=utf-8
'''
Created on 2015年7月16日

@author: Administrator
'''
#os
#sys.path
#sys.pathappend()
#
#time.strftime()

#!/usr/local/bin/python
#coding=utf-8
import os
cmd = os.popen('df').read().strip()
l = cmd.split()[6:]
print l
l1 = l[::6]
l2 = l[4::6]
print l1,l2
for (n,(k,v)) in enumerate(zip(l1,l2)):
        #print n,k,v
        if int(v[:-1]) > 30:
            print '%s磁盘的空间不足,目前使用%s' %(k,v)
