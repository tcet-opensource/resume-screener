from flask import Blueprint

from .upload_resume import upload_resume_bp
from .get_resume_data import get_resume_data_bp
from .recommend_courses import recommend_courses_bp

def register_routes(app):
    app.register_blueprint(upload_resume_bp)
    app.register_blueprint(get_resume_data_bp)
    app.register_blueprint(recommend_courses_bp)
  

# import & regsiter more routes like this

