#!/bin/python
import sys

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

    words = set()

    with open(vocab_file, 'r') as f:
        for line in f:
            word = line.strip()
            words.add(word)
    with open(pruned_glove_file, 'w') as fwrite:
        with open(glove_file, 'r') as fread:
            for line in fread:
                word = line.strip().split()[0]
                if word not in words:
                    continue
                fwrite.write(line)

    print "Pruned glove generated successfully!"
