from flask import request, jsonify, Blueprint

get_resume_data_bp = Blueprint('get_resume_data', __name__)


@get_resume_data_bp.route("/get-resume-data", methods=["GET"])
def get_resume_data():
    # Code to extract data from the uploaded resume should be implemented
    return jsonify({"data": "Resume data extracted successfully."})
    # replace the output with appriopriate data
