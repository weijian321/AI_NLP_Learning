# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# from pyexpat import model

titanic_content = pd.read_csv(open('titanic_train.csv'))
# print titanic_content[:10]
titanic_content = titanic_content.dropna(axis=0)
age_with_fare = titanic_content[['Age', 'Fare']]
age_with_fare = age_with_fare[(age_with_fare['Age'] > 22) & (age_with_fare['Fare'] < 400) & (age_with_fare['Fare'] > 130)]
age = np.array(age_with_fare['Age'].tolist())
fare = np.array(age_with_fare['Fare'].tolist())
length = len(age)
print age

def loss(y_true, yhats): return np.mean(np.abs(y_true - yhats))


def model(x, a, b): return a * x + b
eps = 10
min_loss = float('inf')
num = 12
a = 1
b = 0
dir = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
count = 0
x_true = []
y_hats = []
learn_rate = 1e-2
while True:
    if min_loss < eps:
        break
    indexes = np.random.choice(range(len(age)), size=num)
    x_true = age[indexes]
    y_true = fare[indexes]
    for (da, db) in dir:
        if min_loss != float('inf'):
            a = _a + da * learn_rate * min_loss
            b = _b + db * learn_rate * min_loss
        y_hats = model(x_true, a, b)
        l = loss(y_true, y_hats)
        if l < min_loss:
            min_loss = l
            _a = a
            _b = b
            count += 1
            print('{} \t a = {}\t b = {}\t loss = {}\n'.format(count, _a, _b, min_loss))
    # if count == 13:
    #     break


plt.scatter(age, fare)
plt.plot(age, model(age, _a, _b))
plt.show()
