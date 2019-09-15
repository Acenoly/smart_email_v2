import sqlite3

def add(word, frequency):
    conn = sqlite3.connect('./KB')
    c = conn.cursor()
    purchases = (word)
    c.execute("SELECT * FROM  tfidf WHERE word =?", purchases)
    w = c.fetchone()

    if w:
        purchases = (frequency, word)
        c.execute("UPDATE tfidf SET frequency = ? WHERE word =?", purchases)
    else:
        purchases = (word, frequency)
        c.execute("INSERT INTO tfidf (word, frequency) VALUES (?,?)", purchases)

    conn.commit()
    conn.close()

def search(word):
    conn = sqlite3.connect('./KB')
    c = conn.cursor()
    purchases = (word)
    c.execute("SELECT * FROM  tfidf WHERE word =?", purchases)
    w = c.fetchone()
    if w:
        return w[2]

    return -99