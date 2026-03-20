# -------------------- how to do -----------------------------------
# db like query and process clip will give data then i have to
# in clip .. we get the data of all the files .. we need ones where the qry has the highest probability in the result object for that file 
# -------------------- clip res -----------------------------------
# clip res format eg :: 
# [{
#     "file_path": "/home/alok/my_files/projects/hackathon/test/quespaper.webp",
#     "clip_tags": {
#       "lotus": 0.0101,
#       "a_person": 0.029,
#       "a_document": 0.961
#     }
#   },
#   {
#     "file_path": "/home/alok/my_files/projects/hackathon/test/lotus.webp",
#     "clip_tags": {
#       "lotus": 0.9985,
#       "a_person": 0.001,
#       "a_document": 0.0006
#     }
#   },
#   {
#     "file_path": "/home/alok/my_files/projects/hackathon/test/Fake-AADHAAR-Card.webp",
#     "clip_tags": {
#       "lotus": 0.0007,
#       "a_person": 0.3048,
#       "a_document": 0.6945
#     }
#   },
#   {
#     "file_path": "/home/alok/my_files/projects/hackathon/test/aad_book.webp",
#     "clip_tags": {
#       "lotus": 0.0313,
#       "a_person": 0.8547,
#       "a_document": 0.114
#     }
#   }
# ]


# ----------------- ocr res format ---------------
# [
# {'file_path': '/home/alok/my_files/projects/hackathon/test/Fake-AADHAAR-Card.webp',
#  'ocr_text': 'आपका आधार क्रमाक / your aadhaar no. :\n\n2094 7051 9541\nआधार - आम आदमी का अधिकार\n\n|" _. government of india\nहनुमान जी\nhanumana ji\nजन्म तिथि । 0098 : 01/01/1950\nपुरुष / male\n\n'}
# ]

from process_folder.process_clip import process_folder_clip
from db.db_utils import search_files_ocr

def fullProcess(qry,folder_path):
    clip_res = process_folder_clip(folder_path,query=qry)

    path_list = []

    clip_match = [] # contains the objects with the max prob == that of the given query
    for ele in clip_res: # getting the max prob elements from the clip res
        
        THRESHOLD = 0.9
        qry_tag = ele['clip_tags']
        m_value = max(qry_tag.values())
        if(qry_tag[f"photo of {qry}"]== m_value and m_value>THRESHOLD ):
            clip_match.append(ele)
    
    ocr_res = search_files_ocr(qry)

    ocr_path=[]
    if len(ocr_res)!=0:
        for ele in ocr_res:
            p = ele['file_path']
            ocr_path.append(p)
            path_list.append(p)
    clip_path=[]
    if len(clip_match)!=0:
        for ele in clip_match:
            p = ele['file_path']
            clip_path.append(p)
            path_list.append(p)

    path_list= list(set(path_list))
    return {'all_matching_path':path_list,'clip_path':clip_path,'ocr_path':ocr_path}
# print(fullProcess('aadhaar','/home/alok/my_files/projects/hackathon/test/'))
