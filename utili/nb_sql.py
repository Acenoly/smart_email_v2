import sqlite3

def update(word, weights, word_class):
    conn = sqlite3.connect('./KB')
    c = conn.cursor()
    purchases = (word, word_class)
    c.execute("SELECT * FROM  nb_words WHERE word =? AND word_class=?", purchases)
    w = c.fetchone()
    if w:
        purchases = (weights, word, word_class)
        c.execute("UPDATE nb_words SET weights = ? WHERE word =? AND word_class=?", purchases)
    else:
        purchases = (word, weights, word_class)
        c.execute("INSERT INTO nb_words (word, weights, word_class) VALUES (?,?,?)", purchases)
    conn.commit()
    conn.close()

def search(word, word_class):
    conn = sqlite3.connect('./KB')
    c = conn.cursor()
    try:
        purchases = (word, word_class)
        c.execute("SELECT * FROM  nb_words WHERE word =? AND word_class=?", purchases)
        w = c.fetchone()
        weight = w[2]
        conn.commit()
        conn.close()
        return weight
    except:
        purchases = (word, 1, word_class)
        c.execute("INSERT INTO nb_words (word, weights, word_class) VALUES (?,?,?)", purchases)
    conn.commit()
    conn.close()
    return 1