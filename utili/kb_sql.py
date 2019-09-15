import sqlite3

def add(word, weights, word_class,conflict):
    conn = sqlite3.connect('./KB')
    c = conn.cursor()
    purchases = (word, word_class,conflict)
    c.execute("SELECT * FROM  kb_words_performance WHERE word =? AND word_class=? AND conflict_time=?", purchases)
    w = c.fetchone()

    if w:
        purchases = (weights, word, word_class,conflict)
        c.execute("UPDATE kb_words_performance SET weights = ? WHERE word =? AND word_class=? AND conflict_time=?", purchases)

    else:
        purchases = (word, weights, word_class,conflict)
        c.execute("INSERT INTO kb_words_performance (word, weights, word_class, conflict_time) VALUES (?,?,?,?)",
                  purchases)
    conn.commit()
    conn.close()

    if w:
        return w[2]

    return -99

def change_weights(word, weights, word_class,conflict):
    conn = sqlite3.connect('./KB')
    c = conn.cursor()
    purchases = (word, word_class,conflict)
    c.execute("SELECT * FROM  kb_words_performance WHERE word =? AND word_class=? AND conflict_time=?", purchases)
    w = c.fetchone()

    if w:
        purchases = (weights, word, word_class,conflict)
        c.execute("UPDATE kb_words_performance SET weights = ? WHERE word =? AND word_class=? AND conflict_time=?", purchases)
    else:
        purchases = (word, weights, word_class,conflict)
        c.execute("INSERT INTO kb_words_performance (word, weights, word_class, conflict_time) VALUES (?,?,?,?)",
                  purchases)
    conn.commit()
    conn.close()

def get_weights(word, word_class, conflict):
    conn = sqlite3.connect('./KB')
    c = conn.cursor()

    if conflict < 0:
        purchases = (word, 1, word_class, conflict)
        c.execute("INSERT INTO kb_words_performance (word, weights, word_class, conflict_time) VALUES (?,?,?,?)", purchases)
        conn.commit()
        conn.close()
        return -99

    try:
        purchases = (word, word_class, conflict)
        c.execute("SELECT * FROM  kb_words_performance WHERE word =? AND word_class=? AND conflict_time=?", purchases)
        w = c.fetchone()
        weight = w[2]
        conn.commit()
        conn.close()
        return weight
    except:
        conn.commit()
        conn.close()

    return -99


def get_weights_with_conflict(word,word_class,conflict):
    weight = get_weights(word=word, word_class=word_class,conflict=conflict)
    if weight == -99:
        return get_weights(word,word_class,conflict-1)
    return weight