from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from db.db_utils import delete_file, init_db, search_files_ocr
from process_folder.process_ocr import process_folder_ocr, process_file_ocr
from process import fullProcess
from db.db_utils import save_file
import shutil
import os

app = FastAPI()

# allow requests from Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "./uploads"

@app.on_event("startup")
def startup():
    init_db()

@app.get('/')
async def hello():
    return {"msg": "Recall API running"}

@app.get('/full_search')
async def fullSearch(qry: str, folder_path: str):
    try:
        res = fullProcess(qry, folder_path)
        return res
    except Exception as e:
        return {'msg': f'unable to search: {str(e)}'}

class IndexBody(BaseModel):
    folder_path: str

@app.post('/index_files')
async def index_files(bod: IndexBody):
    try:
        res = process_folder_ocr(bod.folder_path)
        return res
    except Exception as e:
        return {'msg': f"unable to index: {str(e)}"}

@app.get('/ocr_search')
async def ocr_search(qry: str):
    try:
        res = search_files_ocr(qry)
        return res
    except Exception as e:
        return {'msg': f"unable to search: {str(e)}"}

@app.delete('/delete_ocr_record')
async def delete_record(file_path: str):
    try:
        delete_file(file_path)
        return {"msg": "file deleted"}
    except Exception as e:
        return {'msg': f"unable to delete: {str(e)}"}

# upload endpoint for mobile app ----takes files and saves the ocr result in db
@app.post('/upload')
async def upload_files(files: List[UploadFile] = File(...)):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    saved = []

    for file in files:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        ocr_text = process_file_ocr(file_path)
        if ocr_text:
            save_file(file_path, ocr_text)

        saved.append(file_path)

    return {"msg": "uploaded and indexed", "files": saved}