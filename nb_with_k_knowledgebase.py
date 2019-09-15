import utili.ltm_sql

def rightChoise(mistake,word_class):
    for w in mistake:
        utili.ltm_sql.updateRight(w, word_class)

def mistakeRepetition(mistake,word_class):
    for w in mistake:
        utili.ltm_sql.update(w, word_class)


def findRepetition(mistake,word_class):
    Repetition = []

    for w in mistake:
        Repetition.append(utili.ltm_sql.search(w, word_class))

    return Repetition

def relearning(token):
    pass