#main enter
import nb_with_k
import numpy as np
import feature_filter
import NB_init_data
import utili.kb_sql
import utili.nb_sql
import NB_init_data
import pickle
import nltk

if __name__ == '__main__':
    file_object = open("./data/test.txt",encoding="utf-8")
    TokenArray = []
    LabelArray = []

    while True:

        line = file_object.readline()
        if not line:
            break
        line = line.replace("\n","")

        TokenArray.append(feature_filter.features(line))
        LabelArray.append(1)

    LabelArray[len(LabelArray)-1] = 0
    file_object.close()

    f = open('my_classifier.pickle', 'rb')
    corpus = pickle.load(f)
    f.close()

    for token in TokenArray:
        for w in token:
            print(w, end= " ")
            print(corpus.tf_idf(w, token))
        print("==============================================")
