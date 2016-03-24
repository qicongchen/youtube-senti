#!/bin/python 

import numpy
import os
import sys
from rank_metrics import *

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: {0} label_file index_file".format(sys.argv[0])
        print "label_file -- label for each video"
        print "index_file -- video index for each rank"
        exit(1)

    label_file = sys.argv[1]
    rank_file = sys.argv[2]

    labels = []
    fread_label = open(label_file, 'r')
    for line in fread_label.readlines():
        label = float(line.strip())
        labels.append(label)
    fread_label.close()

    indexes = []
    fread_index = open(index_file, 'r')
    for line in fread_index.readlines():
        index = int(line.strip())
        indexes.append(index)
    fread_index.close()

    scores = []
    for index in indexes:
        score = labels[index]
        scores.append(score)

    ndcg = ndcg_at_k(scores, len(scores))
    print 'ndcg: %.33f\n' % ndcg


