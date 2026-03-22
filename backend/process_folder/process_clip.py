import os
from models.CLIP import recognize_objects

SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.tiff', '.bmp']

def process_folder_clip(folder_path, query='dust'):
    results = []

    for filename in os.listdir(folder_path):
        ext = os.path.splitext(filename)[1].lower()
        
        if ext not in SUPPORTED_EXTENSIONS:
            print(f"Skipping {filename}")
            continue

        file_path = os.path.join(folder_path, filename)
        print(f"Processing {filename}...")

        clip_tags = recognize_objects(file_path, query)

        results.append({
            "file_path": file_path,
            "clip_tags": clip_tags,
        })

        print(f"Done {filename}")

    return results
# print(process_folder_clip('/home/alok/my_files/projects/hackathon/test/'))