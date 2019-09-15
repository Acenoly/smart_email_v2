from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize
import string


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def features(content):
    line = content.lower()
    token = []
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
    no_punctuation = line.translate(remove_punctuation_map)
    token.extend(word_tokenize(no_punctuation))
    filtered = [w for w in token if not w in stopwords.words('english')]
    stemmer = PorterStemmer()
    stemmed = stem_tokens(filtered, stemmer)
    return stemmed

if __name__ == '__main__':
    print(features("Hey I am really horny want to chat or see me naked text hot to 69698 text charged at 150pm to unsubscribe text stop 69698"))