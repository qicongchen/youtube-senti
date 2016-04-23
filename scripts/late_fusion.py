#!/bin/python 

import numpy
import sys


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage: {0} event_name output_file".format(sys.argv[0])
        print "event_name -- name of the event (P001, P002 or P003 in Homework 1)"
        print "output_file -- path to save the prediction score"
        print "index_file -- path to save the video indexes in rank order"
        exit(1)

    event_name = sys.argv[1]
    pred_file_suffix = event_name+"_pred"
    pred_files = ["mfcc_pred/"+pred_file_suffix, "cnn_pred/"+pred_file_suffix, "asr_pred/"+pred_file_suffix]
    output_file = sys.argv[2]
    index_file = sys.argv[3]

    # late fusion
    scores = []
    for pred_file in pred_files:
        vector = numpy.genfromtxt(pred_file)
        if len(scores) == 0:
            scores = [0]*len(vector)
        scores = numpy.add(scores, vector)
    scores = scores/len(pred_files)
    indexes = numpy.argsort(scores)[::-1]
    numpy.savetxt(output_file, scores)
    numpy.savetxt(index_file, indexes, fmt='%d')
