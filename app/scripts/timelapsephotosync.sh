#!/bin/bash

LOCAL_DIR="$HOME/Pictures"
REMOTE_DIR="gdrive:"

for folder in "$LOCAL_DIR"/*; do
    if [ -d "$folder" ]; then
        foldername=$(basename "$folder")

        if [[ "$foldername" =~ ^[0-9]{8}$ ]]; then

            if ! rclone lsf "$REMOTE_DIR" | grep -w "$foldername/" > /dev/null; then
                echo "Uploading folder $foldername..."

                rclone mkdir "$REMOTE_DIR/$foldername"

                rclone copy "$folder" "$REMOTE_DIR/$foldername"

                if [ $? -eq 0 ]; then
                    echo "Upload completed. Deleting $foldername"
                    rm -rf "$folder"
                else
                    echo "Error: $foldername"
                fi
            else
                echo "$foldername existed. Deleting."
                rm -rf "$folder"
            fi
        fi
    fi
done

