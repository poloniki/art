from art.load_data import load_data
from art.clean import clean_data, get_most_common
import os
from sklearn.model_selection import train_test_split
import requests
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from functools import partial
from art.params import LOCAL_DATA_PATH  # Ensure this is properly imported


# Function to create subfolders for styles
def create_style_subfolders(base_folder, styles):
    for style in styles:
        style_folder = os.path.join(base_folder, style)
        os.makedirs(style_folder, exist_ok=True)


# Function to download a single image
def download_image(row, base_folder):
    style_folder = os.path.join(base_folder, row["Style"])
    image_path = os.path.join(style_folder, row["painting_name"] + ".jpg")
    if not os.path.exists(image_path):
        try:
            response = requests.get(row["image_url"], stream=True)
            if response.status_code == 200:
                with open(image_path, "wb") as out_file:
                    for chunk in response.iter_content(1024):
                        out_file.write(chunk)
        except Exception as e:
            print(f"Error downloading {row['image_url']}: {e}")


# Function to download images from a DataFrame in parallel
def download_images_parallel(df, base_folder):
    with Pool(cpu_count()) as pool:
        list(
            tqdm(
                pool.imap(
                    partial(download_image, base_folder=base_folder),
                    [row for _, row in df.iterrows()],
                ),
                total=df.shape[0],
            )
        )


def load_data_and_make_folders():
    # Load and clean data
    data = load_data(path="/Users/poloniki/code/melisa/art/label_list/label_list.csv")
    cleaned_data = clean_data(data)
    df = get_most_common(cleaned_data, "Style", 0.8)

    # Specify percentages
    train_percentage = 0.9
    validation_percentage = 0.08
    test_percentage = 0.02

    # Ensure the percentages sum to 1.0
    assert (
        train_percentage + validation_percentage + test_percentage == 1.0
    ), "The percentages must sum to 1.0"

    # Split the data
    train_df, temp_df = train_test_split(
        df, test_size=(1 - train_percentage), stratify=df["Style"], random_state=42
    )
    validation_df, test_df = train_test_split(
        temp_df,
        test_size=(test_percentage / (test_percentage + validation_percentage)),
        stratify=temp_df["Style"],
        random_state=42,
    )

    # Define the base directory for the data
    base_dir = LOCAL_DATA_PATH
    train_dir = os.path.join(base_dir, "train")
    validation_dir = os.path.join(base_dir, "validation")
    test_dir = os.path.join(base_dir, "test")

    # Create the folder structure
    for folder in [train_dir, validation_dir, test_dir]:
        create_style_subfolders(folder, df["Style"].unique())

    # Download images into the respective folders
    download_images_parallel(train_df, train_dir)
    download_images_parallel(validation_df, validation_dir)
    download_images_parallel(test_df, test_dir)


if __name__ == "__main__":
    load_data_and_make_folders()
