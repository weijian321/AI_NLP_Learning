# -*- coding: UTF-8 -*-
import math

num = 0
while num <= 0:
    num = int(raw_input('please input a int number:'))
if num > 1:
    m = math.ceil(math.sqrt(num))
    i = math.ceil((m + 1) / 2.0) #层
    j = (2 * (i - 1) - 1) ** 2
    x = num - j #离该层起点的距离
    y = abs(x % (2 * (i - 1) ) - (i - 1))#边上步进
    print 'total step:', y + i - 1
else:
    print 'total step:', 0