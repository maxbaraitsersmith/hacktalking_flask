#/bin/bash

timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
mkdir chunks/$timestamp
mv ../hacktalking_whisper/chunks/* chunks/$timestamp
python lib/savegraph.py $timestamp