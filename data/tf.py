def tfIdfData():

    file_object = open("./data/TFIDF", encoding="utf-8")
    lineArray = []
    while True:
        line = file_object.readline()
        if not line:
            break
        lineArray.append(line)

    return lineArray

