from flask import Flask,request,jsonify,Blueprint
import numpy as np
import nltk
nltk.download('stopwords')
import io
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

overall_score_bp = Blueprint('overall_score', __name__)

@overall_score_bp.route('/skills')
def skill_scorer():
    def pdf_reader(file):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)
        with open(file, 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                        caching=True,
                                        check_extractable=True):
                page_interpreter.process_page(page)
                print(page)
            text = fake_file_handle.getvalue()
        return text
    # pdf_file = request.files['pdf_file']
    resume_text = pdf_reader('resume-screener/api.resume-screener.com/data/Resume-TCET-FORMAT-PKS.pdf')
    print(resume_text)
    resume_score = 0
    if 'Objective' in resume_text or 'Summary' in resume_text:
        resume_score += 6

    if 'Education' in resume_text or 'School' in resume_text or 'College' in resume_text:
        resume_score += 12

    if 'EXPERIENCE' in resume_text or 'Experience' in resume_text:
        resume_score += 16
        
    if 'INTERNSHIPS' in resume_text or 'INTERNSHIP' in resume_text or 'Internships' in resume_text or 'Internship' in resume_text:
        resume_score += 6
   
    if 'SKILLS' in resume_text or 'SKILL' in resume_text or 'Skills' in resume_text or 'Skill' in resume_text:
        resume_score += 7

    if 'HOBBIES' in resume_text or 'Hobbies' in resume_text:
        resume_score += 4

    if 'INTERESTS' in resume_text or 'Interests' in resume_text:
        resume_score += 5

    if 'ACHIEVEMENTS' in resume_text or 'Achievements' in resume_text:
        resume_score += 13

    if 'CERTIFICATIONS' in resume_text or 'Certifications' in resume_text or 'Certification' in resume_text:
        resume_score += 12

    if 'PROJECTS' in resume_text or 'PROJECT' in resume_text or 'Projects' in resume_text or 'Project' in resume_text:
        resume_score += 19

    skill_score={'resume_score':resume_score}

    return jsonify(skill_score)

    