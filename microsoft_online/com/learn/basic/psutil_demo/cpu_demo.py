#coding=utf-8
'''
Created on 2015年7月27日

@author: Administrator
'''
import psutil
from psutil import net_io_counters
#cpu信息获取
#usertime 执行用户进程的时间百分比
print psutil.cpu_times()
#显示每个逻辑处理器的状况
print psutil.cpu_times(percpu=True)
#显示单项
print psutil.cpu_times().user
#物理处理器
print psutil.cpu_count(logical=False)
#逻辑处理器
print psutil.cpu_count()

#内存信息
print  psutil.virtual_memory()
print psutil.swap_memory()

#磁盘信息
print psutil.disk_io_counters(perdisk=True)
print psutil.disk_partitions()
print psutil.disk_io_counters()

#网络信息
print psutil.net_io_counters()
print psutil.net_io_counters(pernic=True)


#内存模块
print psutil.pids()