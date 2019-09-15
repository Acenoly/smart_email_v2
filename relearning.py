#relearning part
import utili.nb_sql
import utili.kb_sql
import numpy as np
import nb_with_k
import classifier

def realearning_with_conflict(post_list, train_label_list, learning_rate, conflict):
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
       kpo = utili.kb_sql.get_weights_with_conflict(word=w, word_class=0,conflict=conflict)
       kna = utili.kb_sql.get_weights_with_conflict(word=w, word_class=1,conflict=conflict)

       po_train.append([po])
       na_train.append([na])
       K1.append(kpo)
       K2.append(kna)
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

    k1, k2, Loss = nb_with_k.nbk_train_with_n(mat, K1, mat2, K2, y, learning_rate)

    print(Loss)

    for x in range(len(post_list)):
        utili.kb_sql.change_weights(word=post_list[x], weights=K1[x], word_class=0, conflict=conflict+1)
        utili.kb_sql.change_weights(word=post_list[x], weights=K2[x], word_class=1, conflict=conflict+1)

def realearning(post_list, train_label_list, learning_rate):
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
       kpo = utili.kb_sql.get_weights(word=w, word_class=0, conflict=0)
       kna = utili.kb_sql.get_weights(word=w, word_class=1, conflict=0)

       po_train.append([po])
       na_train.append([na])
       K1.append(kpo)
       K2.append(kna)
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

    k1, k2, Loss = nb_with_k.nbk_train_with_n(mat, K1, mat2, K2, y, learning_rate)

    for x in range(len(post_list)):
        utili.kb_sql.change_weights(word=post_list[x], weights=K1[x], word_class=0, conflict=0)
        utili.kb_sql.change_weights(word=post_list[x], weights=K2[x], word_class=1, conflict=0)


# p = ["a", "b"]
# label = 1
# number = 1
# while label == 1:
#     realearning(p,0,1,0)
#     label = classifier.classifier(p)
#     print(number)
#     number+=1