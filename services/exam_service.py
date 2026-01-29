from database_connector import db
import os
from file_handler import save_uploaded_file

def create_exam(teacher_id, title, subject, total_marks, question_paper_file, answer_key_file, upload_folder):
    """Create new exam with uploaded files"""
    conn = db.get_connection()
    if not conn:
        return None
    
    try:
        qp_filename = save_uploaded_file(question_paper_file, upload_folder, 'qp')
        ak_filename = save_uploaded_file(answer_key_file, upload_folder, 'ak')
        
        if not qp_filename or not ak_filename:
            return None
        
        with conn.cursor() as cursor:
            sql = """INSERT INTO exams 
                     (teacher_id, title, subject, total_marks, question_paper, answer_key) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (teacher_id, title, subject, total_marks, qp_filename, ak_filename))
            exam_id = cursor.lastrowid
        
        return {
            'exam_id': exam_id,
            'question_paper': qp_filename,
            'answer_key': ak_filename
        }
    
    except Exception as e:
        print(f"Error creating exam: {e}")
        if qp_filename:
            os.remove(os.path.join(upload_folder, qp_filename))
        if ak_filename:
            os.remove(os.path.join(upload_folder, ak_filename))
        return None