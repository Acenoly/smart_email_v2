import csv

import numpy as np

import nb_with_k
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize
import string


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

if __name__ == '__main__':
    countList = []
    lables = []
    post = []
    with open("data/train_dataset.csv", "rt", encoding="utf-8") as vsvfile:
        reader = csv.reader(vsvfile)
        rows = [row for row in reader]
        i = 0
        TokenArray = []

        for row in rows:
            if (row[0] == "ham"):
                lables.append(0)
            else:
                lables.append(1)
            line = row[1].replace("\n", "")
            line = line.lower()
            token = []
            remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
            no_punctuation = line.translate(remove_punctuation_map)
            token.extend(word_tokenize(no_punctuation))

            filtered = [w for w in token if not w in stopwords.words('english')]
            stemmer = PorterStemmer()
            stemmed = stem_tokens(filtered, stemmer)
            TokenArray.append(stemmed)

    vocab_list = nb_with_k.create_vocabulary_list(TokenArray)
    print(TokenArray)
    print(vocab_list)

    trainset = []


    for post in TokenArray:
        traim = nb_with_k.wordsToVector(vocab_list, post)
        trainset.append(traim)
    pAbusive, positive, negative = nb_with_k.nb_train(trainset, lables)

    k_po = []
    k_na = []

    for i in range(0,len(vocab_list)):
        k_po.append(1)
        k_na.append(1)

    for i in range(len(TokenArray)):
        if i >= 5000 and i<5500:
            continue

        traim = nb_with_k.wordsToVector(vocab_list, TokenArray[i])
        K1 = []
        K2 = []
        Ki = []
        predictions = []
        po_train = []
        na_train = []
        for y in range(len(traim)):
            if traim[y] == 1:
                po_train.append([positive[y]])
                na_train.append([negative[y]])
                K1.append(k_po[y])
                K2.append(k_na[y])
                Ki.append(y)

        if lables[i] == 0:
            predictions.append([1, 0])
        else:
            predictions.append([0, 1])

        mat = np.array(po_train)
        mat2 = np.array(na_train)
        y = np.array(predictions)

        #防止为空
        if len(mat) == 0:
            continue

        k1, k2, Loss = nb_with_k.nbk_train(mat, K1, mat2, K2, y)

        for x in range(len(Ki)):
            k_po[Ki[x]] = k1[x]
            k_na[Ki[x]] = k2[x]
            w = vocab_list[Ki[x]]

    print(k_po)
    print(k_na)
    #这边就最为Test部分了，取10% 500个
    ac = 0

    for i in range(5000,5500):
        traim = nb_with_k.wordsToVector(vocab_list, TokenArray[i])
        K1 = []
        K2 = []
        Ki = []
        predictions = []
        po_train = []
        na_train = []
        for y in range(len(traim)):
            if traim[y] == 1:
                po_train.append([positive[y]])
                na_train.append([negative[y]])
                K1.append(k_po[y])
                K2.append(k_na[y])
                Ki.append(y)

        if lables[i] == 0:
            predictions.append([1, 0])
        else:
            predictions.append([0, 1])

        mat = np.array(po_train)
        mat2 = np.array(na_train)
        y = np.array(predictions)

        # 防止为空
        if len(mat) == 0:
            continue


        re = nb_with_k.kb_classifier(mat, K1, mat2, K2)

        if re == lables[i]:
            ac += 1

    print(ac/500)