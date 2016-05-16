#!/bin/python 

import os
import sys


if __name__ == '__main__':
    if len(sys.argv) != 1:
        print "Usage: {0}".format(sys.argv[0])
        exit(1)

    feat_dirs = ["mfcc_feat/", "cnn_feat/", "asr_feat/"]

    with open('list/pruned_train', 'w') as fwrite:
        with open('list/train', 'r') as fread:
            for line in fread:
                video_id = line.strip().split('\t')[0]
                prune = False
                for feat_dir in feat_dirs:
                    if not os.path.exists("{0}{1}.feat".format(feat_dir, video_id)):
                        prune = True
                        break
                if not prune:
                    fwrite.write(line)

