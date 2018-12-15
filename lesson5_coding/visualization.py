# coding=utf-8
import time
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import pickle
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']
data_name = 'min_model.data'
f = open(data_name, 'rb')
b = pickle.load(f)
assert isinstance(b.most_similar, object)
# print(b.most_similar('简单'))


def tsne_plot(model):
    "Creates and TSNE model and plots it"
    labels = []
    tokens = []
    count = 0
    for word in model.wv.vocab:
        count += 1
        if count > 1000:
            break
        tokens.append(model[word])
        labels.append(word)

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])

    plt.figure(figsize=(16, 16))
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.annotate(labels[i],
                     xy=(x[i], y[i]),
                     xytext=(5, 2),
                     textcoords='offset points',
                     ha='right',
                     va='bottom')
    plt.show()


tsne_plot(b)


