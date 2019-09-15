import nltk
from nltk.corpus import *
from nltk.tokenize import sent_tokenize
import os
import feature_filter
from nltk.text import TextCollection
import os
import pickle
#
#
# all_sents = []
#
# file_object = open("./data/test.txt", encoding="utf-8")
#
# while True:
#     line = file_object.readline()
#     if not line:
#         break
#     line = line.replace("\n", "")
#     all_sents.append(feature_filter.features(line))
#
# print("success")
#
#
# fileList = os.listdir("./data/IFIDF/neg")
# for file in fileList:
#     f = open('./data/IFIDF/neg/' + file)
#     line = f.read()
#     line = line.replace("<br /><br />", "")
#     arry = sent_tokenize(line)
#     for a in arry:
#        all_sents.append(feature_filter.features(a))
#     f.close()
#
# fileList = os.listdir("./data/IFIDF/pos")
#
# for file in fileList:
#     f = open('./data/IFIDF/pos/' + file)
#     line = f.read()
#     line = line.replace("<br /><br />", "")
#     arry = sent_tokenize(line)
#     for a in arry:
#        all_sents.append(feature_filter.features(a))
#
#     f.close()
#
#
# #
# # print(sent_tokenize(data))
# #
# #
# #
# print("open_finished")
# corpus = TextCollection(all_sents)
# #
# print(corpus.tf_idf('human', nltk.word_tokenize('human film this is sentence')))
# # print(corpus.tokens)
#
# #save in model
# f = open('my_classifier.pickle', 'wb')
# pickle.dump(corpus, f)
# f.close()
# print("finished")
#


#just using it!
import pickle
f = open('my_classifier.pickle', 'rb')
corpus = pickle.load(f)
f.close()

print(corpus.tf_idf('gucci', nltk.word_tokenize('gucci plu never confus movi sat watch')))
