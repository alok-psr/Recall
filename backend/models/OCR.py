import pytesseract
from PIL import Image

def extract_text(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(
        image,
        lang='eng+hin',       # english + hindi
        config='--psm 3'      # psm 3 = fully automatic page segmentation
    )
    return text

