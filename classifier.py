#classification function
import utili.nb_sql
import utili.kb_sql
import numpy as np
import nb_with_k

def classifier(posts_list):

    po = []
    na = []
    k_po = []
    k_na = []

    for i in range(0,len(posts_list)):
        w = posts_list[i]

        po.append([utili.nb_sql.search(word=w, word_class=0)])
        na.append([utili.nb_sql.search(word=w, word_class=1)])
        k_po.append(utili.kb_sql.get_weights(word=w, word_class=0,conflict=0))
        k_na.append(utili.kb_sql.get_weights(word=w, word_class=1,conflict=0))


    mat = np.array(po)
    mat2 = np.array(na)

    #防止为空
    if len(mat) == 0:
        return 1

    re = nb_with_k.kb_classifier(mat, k_po, mat2, k_na)
    return re

# p = ["a","b"]
# print(classifier(p))