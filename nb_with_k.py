import math
import numpy as np
from matplotlib import pyplot as plt
from itertools import combinations


#------------------------------------------Naive Bayes--------------------------------------------------------------------------------
def create_vocabulary_list(dataset):
    # dataset 包含了多条邮件的文本
    vocabset = set([])
    for document in dataset:
        vocabset = vocabset | set(document)
    return list(vocabset)

def wordsToVector(vocabset, inputset):
    # vocabset 是词汇表， inputset 为要转化为向量的文本
    vector = [0]*len(vocabset)

    for word in inputset:
        if word in vocabset:
            vector[vocabset.index(word)] = 1
        else:
            print("The word: {} is not in my Vocabulary.".format(word))

    return vector

def nb_train(trainset,classes_list):

    num_vocab = len(trainset[0])
    num_train = len(trainset)

    pAbusive = sum(classes_list) / num_train
    # 计算负类的概率，负类的数量除以训练集的数目

    pnorm_vector = np.zeros(num_vocab)
    # 每个词汇出现在正类中的概率组成的向量
    pabu_vector = np.zeros(num_vocab)
    # 每个词汇出现在负类中的概率组成的向量

    pnorm_denom = 0
    # 正
    pabu_denom = 0
    # 负

    for i in range(len(classes_list)):
        if(classes_list[i] == 0):
            #positive
            pnorm_vector = pnorm_vector + trainset[i]
            pnorm_denom += 1
        else:
            #na
            pabu_vector = pabu_vector + trainset[i]
            pabu_denom += 1


    pnorm_vector = pnorm_vector / pnorm_denom
    pabu_vector = pabu_vector / pabu_denom

    pnorm_vector = pnorm_vector * (1 - pAbusive)/(pnorm_vector * (1 - pAbusive) + pabu_vector * pAbusive)
    pabu_vector = pabu_vector * pAbusive/(pnorm_vector * (1 - pAbusive) + pabu_vector * pAbusive)

    for i in range(len(pnorm_vector)):
        if (pnorm_vector[i] == 0.):
            pnorm_vector[i] = 0.01
        if (pnorm_vector[i] == 1.):
            pnorm_vector[i] = 0.99

    for i in range(len(pabu_vector)):
        if (pabu_vector[i] == 0.):
            pabu_vector[i] = 0.01
        if (pabu_vector[i] == 1.):
            pabu_vector[i] = 0.99

    return pAbusive, pnorm_vector,pabu_vector

def classifier(testVector,pAbusive,positive,negative):

    wordVector = testVector*positive
    Up = 1
    Down = 1

    for wordValue in  wordVector:
        if wordValue > 0:
            Up = wordValue * Up
            Down = Down * (1 - wordValue)

    P1 = Up*pAbusive/(Up*pAbusive + Down*(1-pAbusive))


    wordVector2 = testVector*negative
    Up = 1
    Down = 1
    for wordValue in  wordVector2:
        if wordValue > 0:
            Up = wordValue * Up
            Down = Down * (1 - wordValue)

    P2 = Up*pAbusive/(Up*pAbusive + Down*(1-pAbusive))

    if P1 > P2:
        return 0
    else:
        return 1

#0 positive 1 negative
def words_mul(W,K):
    return np.dot(W,K)

def sigmoid(x):
    # 直接返回sigmoid函数
    return 1. / (1. + np.exp(-x))

def sigmoid_derivative(x):
    sigmoid = 1.0/(1.0+np.exp(-x))
    return sigmoid * (1-sigmoid)

def softmax(X):
    exps = np.exp(X)
    p = exps/np.sum(exps)
    return p

def cross_entropy(X,y):
    m = y.shape[0]
    class_number = 2
    p = softmax(X)
    p = np.array([p])
    new_p = np.zeros(shape=(m,1))
    for i in range(m):
        for j in range(class_number):
            if y[i][j] == 1:
                break
        log_likelihood = math.log(p[i][j])
        new_p[i] = -log_likelihood
    return new_p


def delta_cross_entropy_softmax(p,y):
     p_m = p
     maxindex = np.argmax(p_m)
     i = maxindex
     maxJindex = np.argmax(y)
     j = maxJindex
     # if i==j:
     p[j] -= 1
     return p

def updateK(W,K,back,sigmod_a,delte):
    for i in range(len(W)):
        Word_value = W[i][0]
        Sigmoid_derivative = sigmoid_derivative(sigmod_a)
        K[i] -= delte*back*Sigmoid_derivative*Word_value
    return K


def nbk_train(W1,K1,W2,K2,y):
    Sum_a_po = words_mul(K1, W1)
    Sum_a_na = words_mul(K2,W2)
    #第一层结束
    Sigmod_a_po = sigmoid(Sum_a_po[0])
    Sigmod_a_na = sigmoid(Sum_a_na[0])
    #第一层传播到softmax结算
    Before_soft_max_array = np.array([Sigmod_a_po,Sigmod_a_na])
    # print(Before_soft_max_array)
    Softmax = softmax(Before_soft_max_array)
    # print(Softmax)
    #经过了softmax层
    Loss = cross_entropy(Before_soft_max_array,y)
    # print(Loss)
    #计算loss
    #向后传播 back Propagating
    Back = delta_cross_entropy_softmax(Softmax,y)
    #第一类改变数值
    First = Back[0]
    k1 = updateK(W1,K1,First,Sigmod_a_po,0.01)
    #第二类改变数值
    Second = Back[1]
    k2 = updateK(W2,K2,Second,Sigmod_a_na,0.01)
    return k1,k2,Loss[0][0]

def kb_classifier(W1,K1,W2,K2):
    Sum_a_po = words_mul(K1, W1)
    Sum_a_na = words_mul(K2,W2)
    #第一层结束
    Sigmod_a_po = sigmoid(Sum_a_po[0])
    Sigmod_a_na = sigmoid(Sum_a_na[0])
    #第一层传播到softmax结算
    Before_soft_max_array = np.array([Sigmod_a_po,Sigmod_a_na])
    # print(Before_soft_max_array)
    Softmax = softmax(Before_soft_max_array)
    p_m = Softmax
    maxindex = np.argmax(p_m)
    i = maxindex
    if i == 1:
        return 1
    else:
        return 0

def relearning(W1, K1, W2, K2, y, rate):
    Sum_a_po = words_mul(K1, W1)
    Sum_a_na = words_mul(K2, W2)
    # 第一层结束
    Sigmod_a_po = sigmoid(Sum_a_po[0])
    Sigmod_a_na = sigmoid(Sum_a_na[0])
    # 第一层传播到softmax结算
    Before_soft_max_array = np.array([Sigmod_a_po, Sigmod_a_na])
    # print(Before_soft_max_array)
    Softmax = softmax(Before_soft_max_array)
    # print(Softmax)
    # 经过了softmax层
    Loss = cross_entropy(Before_soft_max_array, y)
    # print(Loss)
    # 计算loss
    # 向后传播 back Propagating
    Back = delta_cross_entropy_softmax(Softmax, y)
    # 第一类改变数值
    First = Back[0]
    k1 = updateK(W1, K1, First, Sigmod_a_po,rate)
    # 第二类改变数值
    Second = Back[1]
    k2 = updateK(W2, K2, Second, Sigmod_a_na,rate)
    #print(k1)
    # print(k2)
    return k1, k2, Loss[0][0]

def nbk_train_with_n(W1,K1,W2,K2,y,n):
    Sum_a_po = words_mul(K1, W1)
    Sum_a_na = words_mul(K2,W2)
    #第一层结束
    Sigmod_a_po = sigmoid(Sum_a_po[0])
    Sigmod_a_na = sigmoid(Sum_a_na[0])
    #第一层传播到softmax结算
    Before_soft_max_array = np.array([Sigmod_a_po,Sigmod_a_na])
    # print(Before_soft_max_array)
    Softmax = softmax(Before_soft_max_array)
    # print(Softmax)
    #经过了softmax层
    Loss = cross_entropy(Before_soft_max_array,y)
    # print(Loss)
    #计算loss
    #向后传播 back Propagating
    Back = delta_cross_entropy_softmax(Softmax,y)
    #第一类改变数值
    First = Back[0]
    k1 = updateK(W1,K1,First,Sigmod_a_po,n)
    #第二类改变数值
    Second = Back[1]
    k2 = updateK(W2,K2,Second,Sigmod_a_na,n)
    return k1,k2,Loss[0][0]