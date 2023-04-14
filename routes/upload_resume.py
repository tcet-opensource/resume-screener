from flask import request, jsonify
from . import bp

@bp.route("/upload-resume", methods=["POST"])
def upload_resume():
    # Code to handle resume upload from user end
    return jsonify({"message": "Resume uploaded successfully."})
    # replace the output with appriopriate data