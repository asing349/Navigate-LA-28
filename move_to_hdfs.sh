#!/bin/bash

# Define the base directory via an environment variable or use a default path
BASE_DIR=${DATASET_DIR:-"/datasets"}

# Define source file paths relative to the base directory
FILES=(
    "$BASE_DIR/all_places.csv"
    "$BASE_DIR/all_restrooms.csv"
    "$BASE_DIR/Parks_20241116.csv"
)

# Define the destination directory in HDFS
HDFS_DEST="/user/hdfs/uploads"

# Ensure the HDFS destination exists
echo "Creating HDFS directory if it does not exist..."
hdfs dfs -mkdir -p "$HDFS_DEST"

# Upload each file to HDFS
for FILE in "${FILES[@]}"; do
    if [ -f "$FILE" ]; then
        echo "Uploading $FILE to HDFS at $HDFS_DEST"
        hdfs dfs -put -f "$FILE" "$HDFS_DEST/"
        if [ $? -eq 0 ]; then
            echo "Successfully uploaded $FILE"
        else
            echo "Failed to upload $FILE"
        fi
    else
        echo "File $FILE not found, skipping..."
    fi
done

echo "File upload to HDFS completed."
