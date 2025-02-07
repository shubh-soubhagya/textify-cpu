from paddleocr import PaddleOCR
import cv2

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="en")  # Change "en" to "ch", "hi", etc., for different languages

def extract_text(image_path):
    """Extracts text from an image using PaddleOCR"""
    results = ocr.ocr(image_path, cls=True)
    
    extracted_text = []
    for result in results:
        for line in result:
            extracted_text.append(line[1][0])  # Extracting detected text
    
    return "\n".join(extracted_text)


