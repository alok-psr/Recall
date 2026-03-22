import os
from models.OCR import extract_text
from db.db_utils import save_file, get_all_files_path, update_file
from pdf2image import convert_from_path
import tempfile

SUPPORTED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp', '.tiff', '.bmp']
PDF_EXTENSIONS = ['.pdf']

def process_file_ocr(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext in PDF_EXTENSIONS:
        # convert each PDF page to image(temp file) and extract text then delete it(temp file)
        images = convert_from_path(file_path)
        full_text = ""
        for i, image in enumerate(images):
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                image.save(tmp.name)
                text = extract_text(tmp.name)
                full_text += f" {text}"
                os.unlink(tmp.name) 
        return full_text.lower()
    
    elif ext in SUPPORTED_EXTENSIONS:
        return extract_text(file_path).lower()
    else:
        return None  # unsupported file type

def process_folder_ocr(folder_path):
    results = []
    existing_path_res = get_all_files_path()
    existing_path = [ele['file_path'] for ele in existing_path_res]

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        ext = os.path.splitext(filename)[1].lower()

        if ext not in SUPPORTED_EXTENSIONS + PDF_EXTENSIONS:
            print(f"Skipping unsupported file: {filename}")
            continue

        print(f"Processing {filename}...")
        ocr_text = process_file_ocr(file_path)

        if ocr_text is None:
            continue

        if file_path in existing_path:
            try:
                update_file(file_path, ocr_text)
                results.append({"file_path": file_path, "ocr_text": ocr_text})
                print("update success")
            except:
                print("update err")
            continue

        try:
            save_file(file_path, ocr_text)
            results.append({"file_path": file_path, "ocr_text": ocr_text})
            print("save file success")
        except:
            print("save file err")

        print(f"Done {filename}")

    return results