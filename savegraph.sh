#/bin/bash

timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
mkdir data/$timestamp
mkdir data/$timestamp/chunks
cp ../hacktalking_whisper/chunks/* data/$timestamp/chunks
python lib/savegraph.py $timestamp
#scp misunderstandings@dc-max.local:/home/misunderstandings/Desktop/max/shared_understandings/exports/$timestamp.xml data/$timestamp/graph.xml