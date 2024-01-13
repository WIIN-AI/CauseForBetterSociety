import os
import json

from rootdir import ROOT_DIR

# Store images in a file manager
image_storage_path = os.path.join(ROOT_DIR, "image_storage")
# Create image storage directory if it doesn't exist
if not os.path.exists(image_storage_path):
    os.makedirs(image_storage_path)

# Store comments in a file manager
comments_storage_path = os.path.join(ROOT_DIR, "comments")
comments_file = os.path.join(comments_storage_path, "comments.json")
# Create Comments storage directory if it doesn't exist
if not os.path.exists(comments_storage_path):
    os.makedirs(comments_storage_path)

try:
    with open(comments_file, "r") as f:
        pass
except FileNotFoundError:
    # Create an empty comments file if it doesn't exist
    if not os.path.exists(comments_file):
        with open(comments_file, "w") as f:
            json.dump({}, f)
