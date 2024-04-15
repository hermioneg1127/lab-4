#!/bin/bash

# import NIST database of fingerprint images to folder /data/ to be used as training/testing data
# USE WITH CAUTION...

# controls

DEST_FOLDER="data/"

TORRENT_URL="https://academictorrents.com/download/"

TORRENT_NAME="d7e67e86f0f936773f217dbbb9c149c4d98748c6"

# grab torrent

wget "$TORRENT_URL$TORRENT_NAME"

# extract torrent (I use transmission on linux and macos, but qbit or utorrent are great as well... idk their cli tho)

# this only needs to be ran if you're running this for the first time
# transmission-daemon
# transmission-daemon --download-dir "$PWD/data"

# recomment this if you have transmission-cli installed... and trust the daemon config to send it to the right path lol
transmission-remote -a "$TORRENT_NAME"

rm -f "$TORRENT_NAME"

# wait for torrent to finish downloading

echo "DO NOT CONTINUE UNTIL TORRENT HAS FINISHED DOWNLOADING... this can be checked with 'transmission-remote -l' in another terminal."
echo "Press ENTER when transmission -l shows the torrent has finished downloading AND you can see the zip file in /data/..."
read

transmission-remote -t 1 -r

# unzip the files from data folder

unzip "data/NISTSpecialDatabase4GrayScaleImagesofFIGS" -d "$DEST_FOLDER"

echo "Database downloaded and extracted to $DEST_FOLDER..."
