from flask import request, jsonify
from . import bp

@bp.route("/get-resume-data", methods=["POST"])
def get_resume_data():
    # Code to extract data from the uploaded resume should be implemented
    return jsonify({"data": "Resume data extracted successfully."})
    # replace the output with appriopriate data
