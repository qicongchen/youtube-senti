#!/bin/python
import os
import sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: {0} vocab_file, file_list".format(sys.argv[0])
        print "vocab_file -- path to the vocabulary file"
        print "file_list -- the list of videos"
        exit(1)

    vocab_file = sys.argv[1]
    file_list = sys.argv[2]

    word_count = {}

    fread = open(file_list, "r")
    for line in fread.readlines():
        video_id = line.replace('\n', '')
        asr_path = "asr/ctm/" + video_id + ".ctm"
        if os.path.exists(asr_path) is False:
            continue
        fread_asr = open(asr_path, "r")
        for line_asr in fread_asr.readlines():
            tokens = line_asr.strip().split(' ')
            word = tokens[4]
            if word not in word_count:
                word_count[word] = 0
            word_count[word] += 1
        fread_asr.close()

    with open(vocab_file, 'w') as f:
        for w, c in word_count.items():
            f.write("%s\n" % w)

    print "vocab generated successfully!"
