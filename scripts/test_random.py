#!/bin/python
import sys
import random

# Apply the SVM model to the testing videos; Output the score for each video

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: {0} event_name output_file".format(sys.argv[0])
        print "event_name -- name of the event (P001, P002 or P003 in Homework 1)"
        print "output_file -- path to save the prediction score"
        exit(1)

    event_name = sys.argv[1]
    output_file = sys.argv[2]

    video_ids = []
    # read in labels
    label_file = "list/test"
    fread_label = open(label_file, 'r')
    for line in fread_label.readlines():
        tokens = line.strip().split('\t')
        video_id = tokens[0]
        cat = tokens[1]
        if cat != event_name:
            continue
        video_ids.append(video_id)
    fread_label.close()

    # read in features
    scores = []
    for video_id in video_ids:
        score = random.uniform(-1, 1)
        scores.append(score)

    # dump result
    fwrite = open(output_file, 'w')
    for score in scores:
        fwrite.write("%s\n" % str(score))
    fwrite.close()
