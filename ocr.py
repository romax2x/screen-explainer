import pytesseract
import cv2
from preprocess import preprocess_image

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def extract_text(image_path):

    img = cv2.imread(image_path)

    processed = preprocess_image(img)

    config_text = r"""
    --oem 3
    --psm 6
    """

    config_code = r"""
    --oem 3
    --psm 6
    -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_(){}[]:.,=+-*/"'<>
    """

    text1 = pytesseract.image_to_string(
        processed,
        lang="eng+rus",
        config=config_text
    )

    text2 = pytesseract.image_to_string(
        processed,
        lang="eng",
        config=config_code
    )

    # объединяем
    if len(text2) > len(text1):
        return text2
    else:
        return text1