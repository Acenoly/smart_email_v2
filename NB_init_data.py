import utili.nb_sql
import utili.kb_sql
import nb_with_k
import numpy as np

#This function to init nb database
def init_nb_database(posts_list,classes_list):
    #post_list array of word sets
    vocab_list = nb_with_k.create_vocabulary_list(posts_list)
    print(vocab_list)
    trainset = []
    for post in posts_list:
        traim = nb_with_k.wordsToVector(vocab_list, post)
        trainset.append(traim)
    pAbusive, positive, negative = nb_with_k.nb_train(trainset, classes_list)
    print(positive)
    for i in range(0,len(vocab_list)):
        w = vocab_list[i]
        print(w)
        # utili.nb_sql.update(word=w, weights=positive[i], word_class=0)
        # utili.nb_sql.update(word=w, weights=negative[i], word_class=1)
        #数据量过小，目前都设置为1
        utili.nb_sql.update(word=w, weights=1, word_class=0)
        utili.nb_sql.update(word=w, weights=1, word_class=1)
    return 0

def init_kb_database(post_list, train_label_list):
    K1 = []
    K2 = []
    Ki = []
    predictions = []
    po_train = []
    na_train = []

    k_count = 0
    for w in post_list:
       po = utili.nb_sql.search(word=w, word_class=0)
       na = utili.nb_sql.search(word=w, word_class=1)
       po_train.append([po])
       na_train.append([na])
       K1.append(1)
       K2.append(1)
       Ki.append(k_count)
       k_count+=1

    if train_label_list == 0:
        predictions.append([1, 0])
    else:
        predictions.append([0, 1])

    mat = np.array(po_train)
    mat2 = np.array(na_train)
    y = np.array(predictions)

    # 防止为空
    if len(mat) == 0:
        return

    k1, k2, Loss = nb_with_k.nbk_train(mat, K1, mat2, K2, y)

    print(Loss)

    for x in range(len(post_list)):
        utili.kb_sql.change_weights(word=post_list[x], weights=K1[x], word_class=0, conflict=0)
        utili.kb_sql.change_weights(word=post_list[x], weights=K2[x], word_class=1, conflict=0)
