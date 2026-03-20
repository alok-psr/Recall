import os
from models.CLIP import recognize_objects


def process_folder_clip(folder_path,query='dust'):
    results = []
    clip_tags = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)        
    
        print(f"processing {filename}  ...")
        
        clip_tags = recognize_objects(file_path,query)
        
        results.append({
            "file_path": file_path,
            "clip_tags": clip_tags,
            # "score":
        })
        
        print(f"Done {filename}")
    
    
    return results
# print(process_folder_clip('/home/alok/my_files/projects/hackathon/test/'))