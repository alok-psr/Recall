import os # handle the file path stuff
from backend.models.OCR import extract_text # extract the text
from backend.db.db_utils import save_file,get_all_files_path,update_file

def process_folder_ocr(folder_path):
    results = []
    existing_path_res= get_all_files_path()
    existing_path = []
    for ele in existing_path_res:
        existing_path.append(ele['file_path'])
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        print(f"processing {filename}  ...")
        ocr_text = extract_text(file_path).lower()
        
        if (file_path in existing_path):
            try:
                update_file(file_path,ocr_text)
                results.append({
                    file_path:file_path,
                    ocr_text:ocr_text
                })
                print("update success")
            except:
                print("update err")
            continue
        try:
            save_file(file_path,ocr_text)
            results.append({
                    file_path:file_path,
                    ocr_text:ocr_text
            })
            print("save file success")
        except:
            print("save file err")
        print(f"Done {filename}")


    return results
# print(process_folder('/home/alok/my_files/projects/hackathon/test/'))