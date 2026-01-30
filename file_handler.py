
import os
from werkzeug.utils import secure_filename
from datetime import datetime

ALLOWED_EXTENSIONS = {'pdf' , 'jpg', 'jpeg', 'png'} 

def allowed_file(filename):
    """check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename, prefix=''):
    """Generate a unique filename using a timestamp"""
    ext = os.path.splitext(original_filename)[1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe_name = secure_filename(original_filename)
    return f"{prefix}_{timestamp}{ext}"

def save_uploaded_file(file, upload_folder, prefix=''):
    """save uploaded file and return saved path"""
    if not file or not allowed_file(file.filename):
       return None
    
    filename = generate_unique_filename(file.filename, prefix)
    filepath = os.path.join(upload_folder, filename)

    try:
        file.save(filepath)
        return filepath
    except Exception as e:
        print(f"Error saving file: {e}")
        return None 
    
def cleanup_old_files(upload_folder, days=30):
    """optional; clean files older than X days"""
    pass 
      