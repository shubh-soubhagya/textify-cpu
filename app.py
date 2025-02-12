from flask import Flask, render_template, request, send_file
import os
from python_scripts.ocr import extract_text
from python_scripts.spelling_corrections import correct_spelling
from python_scripts.spacings import add_space_after_punctuation
from python_scripts.groqllm import clean_text
from werkzeug.utils import secure_filename
from fpdf import FPDF
from docx import Document

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder
# UPLOAD_FOLDER = 'textify/uploads'
# TEMP_FOLDER = 'textify/temp_files'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
TEMP_FOLDER = os.path.join(BASE_DIR, 'temp_files')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(image_path):
    """
    Process the image through OCR pipeline
    """
    try:
        # Extract text from image
        text = extract_text(image_path)
        
        # Apply corrections
        corrected_text = correct_spelling(text)
        
        # Add proper spacing
        spaced_text = add_space_after_punctuation(corrected_text)
        
        # Clean and format text
        final_text = clean_text(spaced_text)
        
        return final_text
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None

def create_text_file(text, output_path):
    """Save text to a file"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

def create_pdf_file(text, output_path):
    """Convert text to PDF"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text)
    pdf.output(output_path)

def create_docx_file(text, output_path):
    """Convert text to DOCX"""
    doc = Document()
    doc.add_paragraph(text)
    doc.save(output_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'image' not in request.files:
            return 'No file part', 400
        
        file = request.files['image']
        
        # If user doesn't select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file', 400
        
        if file and allowed_file(file.filename):
            # Secure the filename
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            try:
                # Save the file temporarily
                file.save(filepath)
                
                # Process the image
                extracted_text = process_image(filepath)
                
                # Clean up the uploaded file
                os.remove(filepath)
                
                if extracted_text is None:
                    return 'Error processing image', 500
                
                return extracted_text
                
            except Exception as e:
                # Clean up on error
                if os.path.exists(filepath):
                    os.remove(filepath)
                return f'Error: {str(e)}', 500
                
        return 'Invalid file type', 400
        
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    text = request.form.get('text')
    format_type = request.form.get('format')
    
    if not text:
        return 'No text provided', 400
    
    if not format_type:
        return 'No format specified', 400
    
    filename = f'extracted_text.{format_type}'
    output_path = os.path.join(TEMP_FOLDER, filename)
    
    try:
        # Create file based on requested format
        if format_type == 'txt':
            create_text_file(text, output_path)
        elif format_type == 'pdf':
            create_pdf_file(text, output_path)
        elif format_type == 'docx':
            create_docx_file(text, output_path)
        else:
            return 'Invalid format type', 400
        
        # Send file to user
        return_data = send_file(
            output_path,
            as_attachment=True,
            download_name=filename
        )
        
        # Clean up after sending
        os.remove(output_path)
        
        return return_data
        
    except Exception as e:
        if os.path.exists(output_path):
            os.remove(output_path)
        return f'Error creating file: {str(e)}', 500

@app.errorhandler(413)
def too_large(e):
    return 'File is too large', 413

if __name__ == '__main__':
    app.run(debug=True)