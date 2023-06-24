from flask import Flask,render_template,send_from_directory

# ImportError: attempted relative import with no known parent package
import sys
sys.path.append("..") # Adds higher directory to python modules path.

app = Flask(__name__)

# Register blueprints
from routes.upload_resume import upload_resume_bp
app.register_blueprint(upload_resume_bp)

from routes.get_resume_data import get_resume_data_bp
app.register_blueprint(get_resume_data_bp)

from routes.recommend_courses import recommend_courses_bp
app.register_blueprint(recommend_courses_bp)

from routes.recommend_skills import recommend_skills_bp
app.register_blueprint(recommend_skills_bp)

from routes.ats_recommendations import ats_recommendations_bp
app.register_blueprint(ats_recommendations_bp)

from routes.overall_score import overall_score_bp
app.register_blueprint(overall_score_bp)

@app.route("/")
def index():
    return "hello world!"

if __name__ == "__main__":
    app.run(debug=True)
