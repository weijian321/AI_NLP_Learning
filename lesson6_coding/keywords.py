# encoding=utf-8
from time import sleep

import pandas as pd
import jieba
from collections import Counter
from tqdm import tqdm_notebook
import math
import pickle
import wordcloud
import matplotlib.pyplot as plt

path = 'C:\Files\study\machine learning\project\project1\sqlResult_1558435.csv'

content = pd.read_csv(path, encoding='gb18030')
content = content.fillna('')
print(content.columns.values)
content_xiaomi = content.iloc[0]['content']
print('content_xiaomi:\n', content_xiaomi)


def cut(str):
    return list(jieba.cut(str))


counter_xiaomi = Counter(cut(content.iloc[0]['content']))

print(counter_xiaomi)

all_news_content = content['content']
all_news_content_set = []
# for c in tqdm_notebook(all_news_content, total=len(all_news_content)):
#     all_news_content_set.append(set(cut(c)))

# data_name = 'all_news_content_set.data'
# f = open(data_name, 'wb')
# pickle.dump(all_news_content_set, f)
# f.close()

data_name = 'all_news_content_set.data'
f = open(data_name, 'rb')
all_news_content_set = pickle.load(f)


def idf(word):
    eps = 1e-10
    return math.log10(len(all_news_content_set) / (sum(1 for w in all_news_content_set if word in w) + eps))


def tf(word, content_counter):
    return content_counter[word] / sum(content_counter.values())


def tf_idf(word, content_counter):
    word_tf = tf(word, content_counter)
    word_idf = idf(word)
    return word_tf * word_idf


# print(tf('小米', counter_xiaomi))


print('tfidf of 的', tf_idf('的', counter_xiaomi))
print('tfidf of 小米', tf_idf('小米', counter_xiaomi))


data_name = 'test_news.txt'
f = open(data_name, 'rb')
test_news = pickle.load(f)


def get_words_important(cuted_words):
    words_importance = {w: tf_idf(w, Counter(cuted_words)) for w in set(cuted_words)}
    return sorted(words_importance.items(), key=lambda x: x[1], reverse=True)


# print(get_words_important(cut(test_news))[:10])

test_news_importance_list = get_words_important(cut(test_news))
importance_wordcloud = wordcloud.WordCloud(font_path='SimHei.ttf')


def plot_importance_wordcloud(words_impantance_list):
    plt.imshow(importance_wordcloud.generate_from_frequencies({w: fre for w, fre in words_impantance_list}))


plot_importance_wordcloud(test_news_importance_list)
plt.show()


