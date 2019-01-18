import os
import jieba
from numpy import shape
import pickle

import numpy as np

# a = np.array([[30, 40, 70], [80, 20, 10], [50, 90, 60]])
# print(a[2])
# print(np.where([0, 1, 1, 0]))
# a = np.array([[1, 2, 3, 4, 5]])
# b = shape(a)
# c = a[0]
# d = shape(c)
news_corpus = 'C:\Files\study\machine learning\project\lesson7\Reduced'


def cut(string):
    return ' '.join(jieba.cut(string))


def file_name(file_dir):
    all_files = []
    for root, dirs, files in os.walk(file_dir):
        print('root_dir:', root)  # 当前目录路径
        print('sub_dirs:', dirs)  # 当前路径下所有子目录
        print('files:', files)  # 当前路径下所有非目录子文件
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files


def file_try_open(news):
    corpuss = []
    for f in news:
        try:
            corpus = cut(open(f, encoding='gb18030').read())
        except UnicodeDecodeError:
            print('error in open: eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee\n')
            continue
        else:
            print(f)
        corpuss.append(corpus)
    return corpuss


# corpuss = file_try_open(file_name(news_corpus))
# print(shape(corpuss))


data_name = 'buffer0.data'
# data = corpuss
# f = open(data_name, 'wb')
# pickle.dump(data, f)
# f.close()
f = open(data_name, 'rb')
data = pickle.load(f)
corpuss = data[0: int(len(data)/2)]

print('len(corpuss):\n', len(corpuss))
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(corpuss)
print('type(tfidf)\n', type(tfidf))
transposed_tfidf = tfidf.transpose()

# print(min(vectorizer.vocabulary_.values()))
# print(max(vectorizer.vocabulary_.values()))

import numpy as np
print('shape(transposed_tfidf):\n', shape(transposed_tfidf))
transposed_tfidf_array = transposed_tfidf.toarray()#np.array(transposed_tfidf)
print('transposed_tfidf:\n', transposed_tfidf)
print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
print('transposed_tfidf_array:\n', transposed_tfidf_array)

print('transposed_tfidf_array.shape:\n', transposed_tfidf_array.shape)
print('np.where(transposed_tfidf_array[6]):\n', np.where(transposed_tfidf_array[6]))
def get_word_id(word):
    return vectorizer.vocabulary_.get(word, None)

print(get_word_id('深圳'))

from functools import reduce
from operator import and_
import re


def get_candidates_ids(input_string):
    return [get_word_id(c) for c in cut(input_string).split()]


def get_candidates_pat(input_string):
    return '({})'.format('|'.join(cut(input_string).split()))


from scipy.spatial.distance import cosine


def search_enginer(query):
    candidates_ids = get_candidates_ids(query)
    v1 = vectorizer.transform([cut(query)]).toarray()[0]
    print(transposed_tfidf_array[_id][0] for _id in candidates_ids)
    candidates = [set(np.where(transposed_tfidf_array[_id])[0]) for _id in candidates_ids]

    merged_candidates = reduce(and_, candidates)

    pat = re.compile(get_candidates_pat(query))

    vector_with_id = [(tfidf[i], i) for i in merged_candidates]

    sorted_vector_with_ids = sorted(vector_with_id, key=lambda x: cosine(x[0].toarray(), v1))

    sorted_ids = [i for v, i in sorted_vector_with_ids]

    for c in merged_candidates:
        output = pat.sub(repl='** \g<1> ** ', string=corpuss[c])
        yield ''.join(output.split())


with open('sz_result.txt', 'w') as f:
    for i, document in enumerate(search_enginer('新能源')):
        f.write('## search result {}\n'.format(i))
        f.write(document+'\n')
    print('done!')
