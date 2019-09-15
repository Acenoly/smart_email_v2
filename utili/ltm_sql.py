import sqlite3
import datetime

def updateRight(feature, word_class):
    conn = sqlite3.connect('./KB')
    c = conn.cursor()
    purchases = (feature, word_class)
    c.execute("SELECT * FROM  mistakes WHERE feature = ? AND word_class = ?", purchases)
    w = c.fetchone()
    if w:
        repetition = w[2]-1
        if repetition < 0:
            repetition = 0

        purchases = (repetition,feature,word_class)
        c.execute("UPDATE mistakes SET repetition = ? WHERE feature = ? AND word_class= ?", purchases)
    else:
        dt = datetime.datetime.now()
        create_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        purchases = (feature, 0, create_time,word_class)
        c.execute("INSERT INTO mistakes (feature, repetition,create_time,word_class) VALUES (?,?,?,?)", purchases)
    conn.commit()
    conn.close()

def update(feature, word_class):
    conn = sqlite3.connect('./KB')
    c = conn.cursor()
    purchases = (feature, word_class)
    c.execute("SELECT * FROM  mistakes WHERE feature = ? AND word_class = ?", purchases)
    w = c.fetchone()
    if w:
        repetition = w[2]+1
        purchases = (repetition,feature,word_class)
        c.execute("UPDATE mistakes SET repetition = ? WHERE feature = ? AND word_class= ?", purchases)
    else:
        repetition = 1
        dt = datetime.datetime.now()
        create_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        purchases = (feature, repetition, create_time,word_class)
        c.execute("INSERT INTO mistakes (feature, repetition,create_time,word_class) VALUES (?,?,?,?)", purchases)
    conn.commit()
    conn.close()
    return repetition

def search(feature, word_class):
    conn = sqlite3.connect('./KB')
    c = conn.cursor()

    try:
        purchases = (feature, word_class)
        c.execute("SELECT * FROM  mistakes WHERE feature =? AND word_class =?", purchases)
        w = c.fetchone()
        weight = w[2]
        conn.commit()
        conn.close()
        return weight
    except:
        conn.commit()
        conn.close()
        return 0