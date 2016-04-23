# -*- coding: UTF-8 -*-
import json
import os
import sys


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
                words = text.split()
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
    if len(sys.argv) != 4:
        print "Usage: {0} vocab_file, glove_file, pruned_glove_file".format(sys.argv[0])
        print "vocab_file -- path to the vocabulary file"
        print "glove_file -- path to the Stanford glove word2vec file"
        print "pruned_glove_file -- path to the pruned Stanford glove word2vec file"
        exit(1)

    vocab_file = sys.argv[1]
    glove_file = sys.argv[2]
    pruned_glove_file = sys.argv[3]
    create_vocab(vocab_file)
    create_glove(vocab_file, glove_file, pruned_glove_file)
