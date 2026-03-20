from fastapi import FastAPI  # pyright: ignore[reportMissingImports]
from pydantic import BaseModel
from process_folder.process_ocr import process_folder_ocr
from db.db_utils import delete_file, init_db,search_files_ocr
app = FastAPI()

@app.get('/')
async def hello():
    try:
        init_db()
        return {"db connention success"}
    except:
        return {" unable to connect to db"}

@app.get('/fullSearch')
async def fullSearch(qry:str):
    # do the full process here.. 
    return qry


# -------- index files -------------
class IndexBody(BaseModel):
    folder_path:str

@app.post('/index_files')
async def index_files(bod:IndexBody):
    try:
        folder_path = bod.folder_path
        res = process_folder_ocr(folder_path)
        return res
    except:
        return {'msg':"unable to delete"}


# ------- ocr search ------------
@app.get('/ocr_search')
async def ocr_search(qry:str):
    try:
        res = search_files_ocr(qry)
        return res
    except:
        return {'msg':"unable to search"}

@app.delete('/delete_ocr_record')
async def delete_record(file_path:str):
    try:
        delete_file(file_path)
        return {"file deleted"}
    except:
        return {'msg':"unable to delete"}