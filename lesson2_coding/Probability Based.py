# -*- coding: UTF-8 -*-
# from collections import Counter
#
# d = ['a', 'a', 'b', 'c', 'd', 'a']
# count = Counter(d)
# print count#.most_common()
# count1 = dict(count)
# print count1
# count2 = count1.items()
# print count2
# new_countsD = {k: v for k, v in count2}
# print new_countsD
import re
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.pyplot import yscale, xscale, title, plot
import time
import random
from functools import reduce
from operator import mul, add


def tokenize(string):
    return ''.join(re.findall(u'[\w|\d|\u4e00-\u9fa5]+', string))

filename = '80k_articles.txt'
all_content = (open(filename).read()).decode("utf-8")
ALL_CHARACTER = tokenize(all_content)
print len(ALL_CHARACTER)
# s = '新华社华盛顿4月13日电（记者林小春）寻找外星生命，目前最理想的地点可能是土星卫星土卫二上的冰封小世界。美国航天局１３日宣布，“卡西尼”探测器在土卫二喷出的羽流中探测到氢气，这意味着土卫二具备生命存在的几乎所有已知要素。\\n\u3000\u3000这项发表在美国《科学》杂志上的研究显示，土卫二羽流中98%是水，约1%是氢气，其余是二氧化碳、甲烷和氨等组成的混合物。\\n\u3000\u3000“卡西尼”项目科学家琳达·施皮尔克当天在网'.decode("utf-8")
# ss = tokenize(s)
# sss = Counter(ss.encode("gb2312"))#.encode("utf-8")
# print sss
# L = [1, 1, 2, 3, 4, 4, 4]
all_character_counts = Counter(ALL_CHARACTER)
print Counter(all_character_counts)
M = all_character_counts.most_common()[0][1]
yscale('log')
xscale('log')
title('Frequency of n-th most frequent word and 1/n line.')
plot([c for (w, c) in all_character_counts.most_common()])
plot([M / i for i in range(1, len(all_character_counts) + 1)])


# plt.show()


def get_probability_from_counts(count):
    all_occurences = sum(count.values())
    dict0 = {k: float(v) / float(all_occurences) for k, v in dict(count).items()}
    return dict0


get_char_prob = get_probability_from_counts(all_character_counts)
print 'char_prob:\n', get_char_prob


def get_char_probability(char):
    all_occurences = sum(all_character_counts.values())
    return float(all_character_counts[char]) / float(all_occurences)


# all_character_counts.get(u'魏', 1)
# get_char_prob(u'魏')
# def get_running_time(func, arg, times):
#     start_time = time.time()
#     # for _ in range(times):
#     print func(arg)
#     print('\t\t {} used time is {}'.format(func.__name__, time.time() - start_time))


#get_char_probability(u'神')
#random_chars = random.sample(ALL_CHARACTER, 1000)
#get_running_time(get_char_probability, u'神', 10000)
# get_running_time(get_char_prob, '神', 10000)
#reduce(add, range(1, 101))


def prob_of_string(string):
    return reduce(mul, [get_char_probability(c) for c in string])

#print prob_of_string(u'这是一个比较常见测试用例')


pair = u"""前天晚上吃晚饭的时候
前天晚上吃早饭的时候""".split('\n')

pair2 = u"""正是一个好看的小猫
真是一个好看的小猫""".split('\n')

pair3 = u"""我无言以对，简直
我简直无言以对""".split('\n')

pairs = [pair, pair2, pair3]


def get_probability_prefromance(language_model_func, pairs):
    for (p1, p2) in pairs:
        print('*'*18)
        print(u'\t\t {} with probability {}'.format(p1, language_model_func(tokenize(p1))))
        print(u'\t\t {} with probability {}'.format(p2, language_model_func(tokenize(p2))))


print pairs#.encode("utf-8")
get_probability_prefromance(prob_of_string, pairs)
