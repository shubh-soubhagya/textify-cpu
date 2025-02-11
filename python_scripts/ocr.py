from paddleocr import PaddleOCR
import cv2

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)  # Change "en" to "ch", "hi", etc., for different languages

def extract_text(image_path):
    """Extracts text from an image using PaddleOCR"""
    results = ocr.ocr(image_path, cls=True)
    
    extracted_text = []
    for result in results:
        for line in result:
            extracted_text.append(line[1][0])  # Extracting detected text
    
    text_output = "\n".join(extracted_text)
    # print("Extracted Text:\n", text_output)  # Ensure text is printed
    return text_output


