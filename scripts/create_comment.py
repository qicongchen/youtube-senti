#!/bin/python
import sys
from comment_analysis import read_word2vec, get_features

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: {0} glove_file".format(sys.argv[0])
        print "glove_file -- path to the pruned glove file"
        exit(1)

    glove_file = sys.argv[1]

    word2vec = read_word2vec(glove_file)
    vectors = get_features(word2vec)

    for video_id, vector in vectors.items():
        line = ';'.join([str(v) for v in vector])
        feat_path = "comment_feat/{0}.feat".format(video_id)
        with open(feat_path, "w") as f:
            f.write(line + '\n')

    print "Comment features generated successfully!"
