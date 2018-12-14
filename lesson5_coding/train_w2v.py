# coding=utf-8
import os
import jieba
import time
import hanziconv
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import pickle


# a = '我是一个中国人'
# b = list(jieba.cut(a))
# print(type(b), '\n', b)
# f = open(data_name, 'wb')
# pickle.dump(a, f)
# f.close()
# del a
# print(b)


def token_f(file_in, file_out):
    for line in file_in:
        words_l = list(jieba.cut(line))
        file_out.writelines(' '.join(words_l))


start = time.time()
files = os.listdir()
for file_name in files:
    if not file_name.startswith('wiki'):
        continue
    with open('simple' + file_name, 'w', encoding='utf-8') as simple_file:
        for line in open(file_name, encoding='utf-8'):
            line_new = hanziconv.HanziConv.toSimplified(line)
            simple_file.writelines(line_new)
        simple_file.close()
end = time.time()
print('simple time: %f' % ((end - start) / 3600))

start = time.time()
files = os.listdir()
with open('pre_word2vec.txt', 'w', encoding='utf-8') as file_output:
    for file_name in files:
        if not file_name.startswith('simplewiki'):
            continue
        with open(file_name, encoding='utf-8') as file_in:
            token_f(file_in, file_output)
            file_in.close()
        print(file_name)
    file_output.close()
end = time.time()
print('time: %f' % ((end - start) / 3600))

start = time.time()
min_model = Word2Vec(LineSentence('pre_word2vec.txt'), min_count=1, size=20)
end = time.time()
print('time: %f' % ((end - start) / 3600))
data_name = 'min_model.data'
f = open(data_name, 'wb')
pickle.dump(min_model, f)
f.close()

data_name = 'min_model.data'
f = open(data_name, 'rb')
b = pickle.load(f)
assert isinstance(b.most_similar, object)
print(b.most_similar('简单'))
