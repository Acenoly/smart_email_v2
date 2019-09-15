#main enter
import nb_with_k
import numpy as np
import feature_filter
import NB_init_data
import utili.kb_sql
import utili.nb_sql
import utili.ltm_sql
import NB_init_data
import classifier
import pickle
import relearning
import system_without_relearning

def initSystem():
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
    NB_init_data.init_nb_database(TokenArray, LabelArray)


    for x in range(len(TokenArray)):
        NB_init_data.init_kb_database(TokenArray[x], LabelArray[x])

def runSystem():
    f = open('my_classifier.pickle', 'rb')
    corpus = pickle.load(f)
    f.close()

    file_object = open("./data/test_p", encoding="utf-8")
    TokenArray = []
    LabelArray = []
    r_result = []

    # repetition threshold
    threshold = 2
    mistake_times = 0

    # Relearning
    while True:

        line = file_object.readline()
        if not line:
            break

        lineSpArray = line.split("~")

        line = lineSpArray[1].replace("\n", "")

        filter_array = feature_filter.features(line)
        TokenArray.append(filter_array)
        r_result.append(lineSpArray[0])

        real_chonse = int(lineSpArray[0])

        if classifier.classifier(filter_array) == real_chonse:
            for w in filter_array:
                utili.ltm_sql.updateRight(w, real_chonse)
        else:
            mistake_times+=1
            # inconsistency
            # remember mistake
            repetitison = []
            mistakeWord = []
            for w in filter_array:
                f = corpus.tf_idf(w, filter_array)
                if f > 0.9:
                    repetitison.append(utili.ltm_sql.update(w,real_chonse))
                    mistakeWord.append(w)

            # Caculate mistake repetition
            relearning_lists = []

            for x in range(len(mistakeWord)):
                #Greater than threshold
                if(repetitison[x] > threshold):
                    #remember in relearning_lists
                    relearning_lists.append(mistakeWord[x])

            #relearning
            relearning.realearning(relearning_lists,real_chonse,10)

    print(mistake_times)

if __name__ == '__main__':
    #初始化系统
    print("init system")
    initSystem()
    print("Mistakes: ", end="")
    system_without_relearning.runSystem()
    print("Begin relearning")
    print("relearning times or conflict times: ", end="")
    runSystem()
    print("After relearning")
    print("Mistakes: ", end="")
    system_without_relearning.runSystem()



