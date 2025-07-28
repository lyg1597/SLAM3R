import os
from pathlib import Path
from PIL import Image
import re

def reorder_and_rename_images(directory_path, new_image_dir):
    """
    Finds images named 'rgb_{%d}.{%d}.jpg', sorts them numerically,
    and saves them as 'frame_{idx:05d}.png'.

    Args:
        directory_path (str): The path to the folder containing the images.
    """
    image_dir = Path(directory_path)
    new_image_dir = Path(new_image_dir)
    if not image_dir.is_dir():
        print(f"Error: Directory not found at '{directory_path}'")
        return

    # 1. Find all files matching the initial pattern
    jpg_files = list(image_dir.glob('rgb_*.jpg'))

    # 2. Define a key for natural sorting (e.g., so 'rgb_2' comes before 'rgb_10')
    def natural_sort_key(filename):
        # Extracts all numbers from the filename and returns them as a list of integers
        return [int(c) for c in re.findall(r'\d+', filename.name)]

    # 3. Sort the files using the natural sort key
    sorted_files = sorted(jpg_files, key=natural_sort_key)
    
    if not sorted_files:
        print("No matching 'rgb_*.jpg' files were found.")
        return

    # 4. Iterate, convert, and rename
    print(f"Found {len(sorted_files)} images to process...")
    for idx, old_path in enumerate(sorted_files, start=1):
        try:
            # Define the new filename, zero-padded to 5 digits
            new_name = f"frame_{idx:05d}.png"
            new_path = new_image_dir / new_name

            # Open the original JPG and save it as a new PNG
            with Image.open(old_path) as img:
                img.save(new_path, 'PNG')

            print(f"Converted '{old_path.name}' -> '{new_path.name}'")
            
            # --- Optional: Uncomment the line below to delete the original JPG file ---
            # old_path.unlink()

        except Exception as e:
            print(f"Could not process {old_path.name}. Error: {e}")
            
    print("\nProcessing complete! ✨")


# --- HOW TO USE ---
if __name__ == "__main__":
    # IMPORTANT: Replace this with the actual path to your image folder
    target_folder = './data/small_big_room_rewrite' 
    src_folder = './data/sampled_big_room_undistort'
    
    reorder_and_rename_images(src_folder, target_folder)