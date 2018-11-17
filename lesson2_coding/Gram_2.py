# -*- coding: UTF-8 -*-
import json
import re
from collections import Counter
from functools import reduce
from operator import mul

# dic = {'a': 1, 'b': 3, 'c': 10}
# print dict(dic.items()[:2])

filename = '80k_articles.txt'
all_content = (open(filename).read()).decode("utf-8")

#s = '新华社华盛顿4月13日电（记者林小春）寻找外星生命，目前最理想的地点可能是土星卫星土卫二上的冰封小世界。美国航天局13日宣布，“卡西尼”探测器在土卫二喷出的羽流中探测到氢气，这意味着土卫二具备生命存在的几乎所有已知要素。\\n\u3000\u3000这项发表在美国《科学》杂志上的研究显示，土卫二羽流中98%是水，约1%是氢气，其余是二氧化碳、甲烷和氨等组成的混合物。\\n\u3000\u3000“卡西尼”项目科学家琳达·施皮尔克当天在网'.decode("utf-8")

pair = u"""前天晚上吃晚饭的时候
前天晚上吃早饭的时候""".split('\n')

pair2 = u"""正是一个好看的小猫
真是一个好看的小猫""".split('\n')

pair3 = u"""我无言以对，简直
我简直无言以对""".split('\n')

pairs = [pair, pair2, pair3]


def tokenize(string):
    return ''.join(re.findall(u'[\w|\d|\u4e00-\u9fa5]+', string))


ALL_CHARACTER = tokenize(all_content)
print ALL_CHARACTER[:100]
all_character_counts = Counter(ALL_CHARACTER)


def get_probability_from_counts(count):
    all_occurences = sum(count.values())
    dict0 = {k: float(v) / float(all_occurences) for k, v in dict(count).items()}
    return dict0




gram_length = 2
two_gram_counts = Counter(ALL_CHARACTER[i:i+gram_length] for i in range(len(ALL_CHARACTER) - gram_length))
print 'counter中频率最高前20：\n', json.dumps(two_gram_counts.most_common()[:20], encoding='UTF-8', ensure_ascii=False)
get_pair_prob = get_probability_from_counts(two_gram_counts)
print '概率字典频率最高前20：\n', json.dumps(dict(get_pair_prob.items()[:20]), encoding='UTF-8', ensure_ascii=False)


def get_char_probability(char):
    all_occurences = sum(all_character_counts.values())
    return float(all_character_counts[char]) / float(all_occurences)


def prob_of_string(string):
    return reduce(mul, [get_char_probability(c) for c in string])


def get_2_gram_prob(word, prev):
    if get_pair_prob.has_key(prev + word):
        return get_pair_prob[prev + word] / get_char_probability(prev)
    else:
        return get_char_probability(word)


def get_2_gram_string_prob(string):
    probablities = []
    for i, c in enumerate(string):
        prev = '' if i == 0 else string[i - 1]
        probablities.append(get_2_gram_prob(c, prev))
    return reduce(mul, probablities)


def get_probability_prefromance(language_model_func, pairs):
    for (p1, p2) in pairs:
        print('*'*18)
        print(u'\t\t {} with probability {}'.format(p1, language_model_func(tokenize(p1))))
        print(u'\t\t {} with probability {}'.format(p2, language_model_func(tokenize(p2))))


get_probability_prefromance(get_2_gram_string_prob, pairs)#prob_of_string


