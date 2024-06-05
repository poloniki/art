from pathlib import Path
import os

LOCAL_DATA_PATH = Path.home().joinpath(".lewagon", "art_data")
if not os.path.exists(LOCAL_DATA_PATH):
    os.mkdir(LOCAL_DATA_PATH)

COLUMN_NAMES = [
    "author_name",
    "painting_name",
    "image_url",
    "Genre",
    "Style",
    "Nationality",
    "Painting School",
    "Art Movement",
    "Field",
    "Date",
    "Influenced by",
    "Media",
    "Influenced on",
    "Family and Relatives",
    "Tag",
    "Pupils",
    "Location",
    "Original Title",
    "Dimensions",
    "Series",
    "Teachers",
    "Friends and Co-workers",
    "Art institution",
    "Period",
    "Theme",
    "Path",
]
