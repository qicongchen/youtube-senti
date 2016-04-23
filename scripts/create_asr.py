#!/bin/python
import numpy as np
import os
import sys
from comment_analysis import stem

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: {0} glove_file, file_list".format(sys.argv[0])
        print "glove_file -- path to the pruned glove file"
        print "file_list -- the list of videos"
        exit(1)

    glove_file = sys.argv[1]
    file_list = sys.argv[2]

    word2vec = {}
    with open(glove_file, 'r') as f:
        for line in f:
            tokens = line.strip().split()
            word = tokens[0]
            vector = np.array([float(token) for token in tokens[1:]])

    vectors = {}
    with open(file_list, "r") as fread:
        for line in fread:
            video_id = line.replace('\n', '')
            asr_path = "asr/" + video_id + ".ctm"
            if os.path.exists(asr_path) is False:
                continue
            vector = np.array([0]*300)
            with open(asr_path, "r") as fread_asr:
                for line_asr in fread_asr.readlines():
                    tokens = line_asr.strip().split(' ')
                    word = stem(tokens[4])
                    vector = vector + word2vec[word]
            vector = vector/np.linalg.norm(vector)
            vectors[video_id] = vector

    for video_id, vector in vectors.items():
        line = ';'.join([str(v) for v in vector])
        feat_path = "asr_feat/"+video_id+".feat"
        with open(feat_path, "w") as f:
            f.write(line + '\n')

    print "ASR features generated successfully!"
