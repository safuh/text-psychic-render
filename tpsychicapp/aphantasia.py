from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

#from django.conf.settings import BASE_DIR
import os
import language_tool_python
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.text import Tokenizer as Tk
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Flatten, Dense, Embedding, LSTM

def getDoc(url):
    LANGUAGE = "english"
    SENTENCES_COUNT = 10
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
    # parser = PlaintextParser.from_string("Check this out.", Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)
    ans=''
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print(sentence)
        ans += str(sentence)
    return ans
def spellcheck(text):
    my_tool = language_tool_python.LanguageToolPublicAPI('en-US')
    my_matches = my_tool.check(text)
    return my_matches
def autoco(my_text):
    my_matches=spellcheck(my_text)  
    myMistakes = []  
    myCorrections = []  
    startPositions = []  
    endPositions = []  
  
    # using the for-loop  
    for rules in my_matches:  
        if len(rules.replacements) > 0:  
            startPositions.append(rules.offset)  
            endPositions.append(rules.errorLength + rules.offset)  
            myMistakes.append(my_text[rules.offset : rules.errorLength + rules.offset])  
            myCorrections.append(rules.replacements[0])  
  
    # creating new object  
    my_NewText = list(my_text)   
  
    # rewriting the correct passage  
    for n in range(len(startPositions)):  
        for i in range(len(my_text)):  
            my_NewText[startPositions[n]] = myCorrections[n]  
            if (i > startPositions[n] and i < endPositions[n]):  
                my_NewText[i] = ""  
  
    my_NewText = "".join(my_NewText)
    return my_NewText

def sentimentModel():
    BASE_DIR=os.path.dirname(__file__)
    model = Sequential()
    model.add(Embedding(10000,32))
    model.add(LSTM(32,return_sequences=True))
    model.add(LSTM(32,return_sequences=True))
    model.add(LSTM(32,return_sequences=True))
    model.add(LSTM(32))
    model.add(Dense(1,activation='sigmoid'))
    model.compile(optimizer='rmsprop',loss='binary_crossentropy',metrics=['acc'])
    f=os.path.join(BASE_DIR,'12_model.h5')
    model.load_weights(f)
    return model
def sentimentAnalysis(text):
    tokenizer = Tk(num_words=10000)
    tokenizer.fit_on_texts(text.split())
    sequences=tokenizer.texts_to_sequences(text.split())
    print(sequences)
    word_index=tokenizer.word_index
    print(word_index)
    model=sentimentModel()
    print(model)
    seq=pad_sequences(sequences,maxlen=256)
    print(seq)
    ans=model.predict(seq)
    return ans
def textEmbeddings(text,max_features,dim):
    model = Sequential(max_features,dim)
    model.add(Embedding(max_features,dim))
    model.fit(text)
    ##model.load_wieghts
    return model
def tokenization(text,max_features,maxlen):
    tokenizer=Tk(num_words = max_features)
    sequences=tokenizer.text_to_sequences(text)
    word_index=tokenizer.word_index
    data = pad_sequences(sequences,maxlen=maxlen)
    return (data, word_index)
def pos():
    pass
def lemma():
    pass
def summary():
    pass
def text2image():
    pass
def headlinegen():
    pass
def blogpostgen():
    pass
