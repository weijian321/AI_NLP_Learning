# encoding=utf-8
import pandas as pd
import re
import jieba
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import pickle
from collections import defaultdict


path = 'C:\Files\study\machine learning\project\project1\sqlResult_1558435.csv'
content = pd.read_csv(path, encoding='gb18030')
content = content.fillna('')
all_content = ''.join(content['content'].tolist())


def cut(contents):
    return ' '.join(jieba.cut(contents))


def token(str):
    return ''.join(re.findall('[\w|\d]+', str))


with open('news_corpus.txt', 'w', encoding='utf-8') as f:
    f.write(cut(token(all_content)))

data_name = 'word2vec_model.data'

word2vec_model = Word2Vec(LineSentence('news_corpus.txt'), size=35, workers=8)
f = open(data_name, 'wb')
pickle.dump(word2vec_model, f)
f.close()

f = open(data_name, 'rb')
word2vec_model = pickle.load(f)
print(word2vec_model.most_similar('可能', topn=20))


def get_related_word(init_word):
    seen = defaultdict(int)
    unseen = [init_word]
    max_size = 1000
    while unseen and len(seen) < max_size:
        if len(seen) % 100 == 0:
            print('\ncount:  {}'.format(len(seen)))
        node = unseen.pop(0)
        new_nodes = [w for w, v in word2vec_model.most_similar(node, topn=20)]
        unseen += new_nodes
        seen[node] += 1
    return sorted(seen.items(), key=lambda x: x[1], reverse=True)


print(get_related_word('可能'))
