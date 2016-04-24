# -*- coding: UTF-8 -*-
import json
import os
import sys
import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

STEMMER = PorterStemmer()
STOPWORDS = stopwords.words('english')
VOCAB_FILE = 'comment/vocab'
GLOVE_FILE = 'asr/glove/glove.6B.300d.txt'
PRUNED_GLOVE_FILE = 'comment/glove.pruned.300d.txt'


def get_videos(phase, target_cat):
    video_ids = []
    with open('list/pruned_{0}'.format(phase), 'r') as f:
        for line in f:
            tokens = line.strip().split('\t')
            video_id = tokens[0]
            cat = tokens[1]
            if cat != target_cat:
                continue
            video_ids.append(video_id)
    return video_ids


def tokenize(text):
    words = []

    text = text.lower()
    tokens = nltk.word_tokenize(text)
    for token in tokens:    
        #  token = STEMMER.stem(token)
        #  if token in STOPWORDS:
        #      continue
        words.append(token)
    return words


def stem(word):
    word = word.lower()
    word = STEMMER.stem(word)
    return word, word in STOPWORDS


def read_word2vec(glove_file):
    word2vec = {}
    with open(glove_file, 'r') as f:
        for line in f:
            tokens = line.strip().split()
            word = tokens[0]
            vector = np.array([float(token) for token in tokens[1:]])
            word2vec[word] = vector
    return word2vec


def get_features(word2vec):
    vectors = {}
    json_dirs = ['SenTube/automobiles_EN/', 'SenTube/tablets_EN/']
    for json_dir in json_dirs:
        for json_file in os.listdir(json_dir):
            if '.json' not in json_file:
                continue
            with open("{0}{1}".format(json_dir, json_file)) as fread:
                data = json.load(fread)
            video_id = data['video_id']
            vector = np.array([0] * 300)
            for comment in data['comments']:
                text = comment["text"]
                words = tokenize(text)
                for word in words:
                    if word not in word2vec:
                        continue
                    vector = vector + word2vec[word]
            norm = np.linalg.norm(vector)
            if norm > 0:
                vector = vector / norm
            vectors[video_id] = vector
    return vectors


def create_vocab(vocab_file):
    word_count = {}
    json_dirs = ['SenTube/automobiles_EN/', 'SenTube/tablets_EN/']
    for json_dir in json_dirs:
        for json_file in os.listdir(json_dir):
            if '.json' not in json_file:
                continue
            with open("{0}{1}".format(json_dir, json_file)) as fread:
                data = json.load(fread)
            for comment in data['comments']:
                text = comment["text"]
                words = tokenize(text)
                for word in words:
                    if word not in word_count:
                        word_count[word] = 0
                    word_count[word] += 1
    with open(vocab_file, 'w') as f:
        for word, count in word_count.items():
            f.write("%s\n" % word.encode('UTF-8'))


def create_glove(vocab_file, glove_file, pruned_glove_file):
    vocab = set()
    with open(vocab_file, 'r') as f:
        for line in f:
            word = line.strip()
            vocab.add(word)
    with open(pruned_glove_file, 'w') as fwrite:
        with open(glove_file, 'r') as fread:
            for line in fread:
                word = line.strip().split()[0]
                if word not in vocab:
                    continue
                fwrite.write(line)


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print "Usage: command {0}".format(sys.argv[0])
        exit(1)

    create_vocab(VOCAB_FILE)
    create_glove(VOCAB_FILE, GLOVE_FILE, PRUNED_GLOVE_FILE)
