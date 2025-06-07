#!/bin/bash

LOCAL_DIR="$HOME/Pictures"
REMOTE_DIR="gdrive-test:"

for folder in "$LOCAL_DIR"/*
do 
    FOLDER_NAME=$(basename "$folder") 

    if [[ $FOLDER_NAME =~ ^[0-9]{8}$ ]]
    then 

        if ! rclone lsd $REMOTE_DIR | grep -w $FOLDER_NAME > /dev/null 
        then 
            rclone mkdir $FOLDER_NAME
            echo "mkdir $FOLDER_NAME" 
        fi

        rclone copy "$folder" "$REMOTE_DIR/$FOLDER_NAME" --transfers=3 --drive-chunk-size=16M --progress 
        rclone delete "$folder" 
    fi
done