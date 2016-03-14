#!/bin/bash

# Paths to different tools; 
opensmile_path=/home/ubuntu/tools/openSMILE-2.1.0/bin/linux_x64_standalone_static
speech_tools_path=/home/ubuntu/tools/speech_tools/bin
ffmpeg_path=/home/ubuntu/tools/ffmpeg-2.2.4
opencv_path=/home/ubuntu/tools/opencv-2.4.10
export PATH=$opensmile_path:$speech_tools_path:$ffmpeg_path:$PATH
export LD_LIBRARY_PATH=$ffmpeg_path/libs:$opensmile_path/lib:$LD_LIBRARY_PATH

# Two additional variables
video_path=../video   # path to the directory containing all the videos. In this example setup, we are linking all the videos to "../video"
cluster_num=200        # the number of clusters in k-means. Note that 50 is by no means the optimal solution.
                      # You need to explore the best config by yourself.

sort -R list/all > list/all_random
sed -n 1,89p list/all_random > list/train
sed -n 90,178p list/all_random > list/test
rm list/all_random
# Great! We are done!
echo "SUCCESSFUL COMPLETION"
