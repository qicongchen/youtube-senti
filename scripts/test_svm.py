#!/bin/python 

import numpy
import os
import cPickle
import sys
from ranking import RankSVM

if __name__ == '__main__':
    if len(sys.argv) != 9:
        print "Usage: {0} event_name model_file feat_dir feat_suffix feat_type feat_dim output_file index_file".format(sys.argv[0])
        print "event_name -- name of the event (P001, P002 or P003 in Homework 1)"
        print "model_file -- path of the trained svm file"
        print "feat_dir -- dir of feature files"
        print "feat_suffix -- suffix of feature files, eg: spbof"
        print "feat_type -- type of feature files, dense|sparse"
        print "feat_dim -- dim of features"
        print "output_file -- path to save the prediction score"
        print "index_file -- path to save the video indexes in rank order"
        exit(1)

    event_name = sys.argv[1]
    model_file = sys.argv[2]
    feat_dir = sys.argv[3]
    feat_suffix = sys.argv[4]
    feat_type = sys.argv[5]
    feat_dim = int(sys.argv[6])
    output_file = sys.argv[7]
    index_file = sys.argv[8]

    # load the kmeans model
    svm = cPickle.load(open(model_file, "rb"))

    video_ids = []
    # read in labels
    label_file = "list/pruned_test"
    fread_label = open(label_file, 'r')
    fwrite = open("list/"+event_name+"_test_label", "w")
    for line in fread_label.readlines():
        tokens = line.strip().split('\t')
        video_id = tokens[0]
        cat = tokens[1]
        label = float(tokens[2])
        if cat != event_name:
            continue
        video_ids.append(video_id)
        fwrite.write("%g\n" % label)
    fwrite.close()
    fread_label.close()

    # read in features
    features = []
    for video_id in video_ids:
        feat_path = "{0}{1}.{2}".format(feat_dir, video_id, feat_suffix)
        feature = [0]*feat_dim
        if feat_type == 'dense':
            feature = numpy.genfromtxt(feat_path, delimiter=';')
        else:
            line = numpy.genfromtxt(feat_path, delimiter=' ', dtype=str)
            if len(line.shape) == 0:
                line = numpy.array([line])
            for item in line:
                if len(item) == 0:
                    continue
                tokens = item.split(':')
                key = int(tokens[0])-1
                value = float(tokens[1])
                if key < feat_dim:
                    feature[key] = value
        features.append(feature)

    # test svm
    features = numpy.array(features)
    scores, indexes = svm.predict(features)
    # dump result
    fwrite = open(output_file, 'w')
    for score in scores:
        fwrite.write("%s\n" % str(score))
    fwrite.close()
    fwrite = open(index_file, 'w')
    for index in indexes:
        fwrite.write("%s\n" % str(index))
    fwrite.close()
