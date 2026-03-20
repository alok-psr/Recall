import os # handle the file path stuff
from models.OCR import extract_text # extract the text


def process_folder_ocr(folder_path):
    results = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        print(f"processing {filename}  ...")
        ocr_text = extract_text(file_path)
        
        results.append({
            "file_path": file_path,
            "ocr_text": ocr_text,
        })
        
        print(f"Done {filename}")
    
    return results
# print(process_folder('/home/alok/my_files/projects/hackathon/test/'))