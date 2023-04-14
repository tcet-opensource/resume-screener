from flask import Flask

app = Flask(__name__)

# Register blueprints
from routes.upload_resume import upload_resume_bp
app.register_blueprint(upload_resume_bp)

from routes.get_resume_data import get_resume_data_bp
app.register_blueprint(get_resume_data_bp)

from routes.recommended_courses import recommended_courses
app.register_blueprint(recommended_courses)


if __name__ == "__main__":
    app.run(debug=True)
