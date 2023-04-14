from flask import Flask,render_template

app = Flask(__name__)

# Register blueprints
from routes.upload_resume import upload_resume_bp
app.register_blueprint(upload_resume_bp)

from routes.get_resume_data import get_resume_data_bp
app.register_blueprint(get_resume_data_bp)

from routes.recommend_courses import recommend_courses_bp
app.register_blueprint(recommend_courses_bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
