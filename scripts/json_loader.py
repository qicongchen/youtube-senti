# -*- coding: UTF-8 -*-
import json
import os

json_dirs = ['SenTube/automobiles_EN/', 'SenTube/tablets_EN/']
count = 0
comment_keyset = set()
fwrite = open('list/all', 'w')
for json_dir in json_dirs:
    for json_file in os.listdir(json_dir):
        if '.json' not in json_file:
            continue
        with open(json_dir+json_file) as fread:
            data = json.load(fread)
        category = data['category']
        video_id = data['video_id']
# [u'category',
#  u'view_count',
#  u'video_id',
#  u'title',
#  u'avg_rating',
#  u'video_description',
#  u'video_type',
#  u'comments',
#  u'uploader',
#  u'published',
#  u'duration']
        pos = 0
        neg = 0
        for i, comment in enumerate(data['comments']):
            if 'annotation' in comment:
                #print "%s %d" % (json_dir+json_file, i)
                annotation = comment['annotation']
                if 'positive-video' in annotation:
                    if annotation['positive-video']=='1':
                        pos += 1
                if 'negative-video' in annotation:
                    if annotation['negative-video']=='1':
                        neg += 1
                for k in annotation.keys():
                    comment_keyset.add(k)
                count += 1
        if neg + pos == 0:
            continue
        else:
            score = (pos+0.0)/(pos+neg)
        fwrite.write("%s\t%s\t%g\n" % (video_id, category, score))
fwrite.close()
print "comment keyset:"
print comment_keyset
print "%d annotated comments in total" % count
