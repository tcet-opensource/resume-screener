from flask import Blueprint, jsonify

upload_resume_bp = Blueprint('upload_resume', __name__)

@upload_resume_bp.route("/upload-resume", methods=["POST"])
def upload_resume():
    # Code to handle resume upload from user end
    return jsonify({"message": "Resume uploaded successfully."})
    # replace the output with appriopriate data