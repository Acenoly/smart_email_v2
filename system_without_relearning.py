# main enter
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


def initSystem():
    file_object = open("./data/test.txt", encoding="utf-8")
    TokenArray = []
    LabelArray = []

    while True:

        line = file_object.readline()
        if not line:
            break
        line = line.replace("\n", "")

        TokenArray.append(feature_filter.features(line))
        LabelArray.append(1)

    LabelArray[len(LabelArray) - 1] = 0

    file_object.close()
    NB_init_data.init_nb_database(TokenArray, LabelArray)

    for x in range(len(TokenArray)):
        NB_init_data.init_kb_database(TokenArray[x], LabelArray[x])


def runSystem():

    file_object = open("./data/test_p", encoding="utf-8")
    TokenArray = []
    LabelArray = []
    r_result = []

    # repetition threshold
    conflict_number = 0

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

        if classifier.classifier(filter_array) == int(lineSpArray[0]):
            pass
        else:
            conflict_number+=1

    print(conflict_number)



if __name__ == '__main__':
    # 初始化系统
    # initSystem()
    runSystem()

