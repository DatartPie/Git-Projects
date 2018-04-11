# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 12:36:23 2018

@author: pratha
"""


#import csv
import pandas as pd
#import numpy as np
import string
import re
#import glob
#import os
#import operator
import nltk
print('The nltk version is {}.'.format(nltk.__version__))
from nltk.corpus import stopwords
from stemming.porter2 import stem
#from __future__ import print_function, unicode_literals
#from collections import defaultdict
#from nltk.classify.api import Classifier
#from nltk.probability import FreqDist

df = pd.read_csv('C:/Users/Pratha/Desktop/AGLESIS/text analysis.csv', sep=',')

good_comm = []
bad_comm = []

for index, row in df.iterrows():
    if row['Sentiment'] == "Good":
        good_tuple = tuple([row['SentimentText'], row['Sentiment']])
        good_comm.append(good_tuple)

for index, row in df.iterrows():
    if row['Sentiment'] == "Bad":
        bad_tuple = tuple([row['SentimentText'], row['Sentiment']])
        bad_comm.append(bad_tuple)

# Text processing #tweets=comnts
comnts = []
regex = re.compile('[%s]' % re.escape(string.punctuation))
sw = stopwords.words("english")

for (words, sentiment) in good_comm + bad_comm:
    words_removed = regex.sub(' ', words)
    words_lowered = [e.lower() for e in words_removed.split()]
    words_nonstopped = [w for w in words_lowered if w not in sw]
    words_stemmed = [stem(txt) for txt in words_nonstopped]
    comnts.append((words_stemmed, sentiment))
print(comnts)