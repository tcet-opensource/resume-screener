from flask import request, jsonify, Blueprint

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from models.get_ats_recommendation import load_json_file , ats_recommendations

ats_recommendations_bp = Blueprint('ats_recommendations', __name__)


@ats_recommendations_bp.route('/ats-recommendations', methods=['GET'])
def get_recommendations():
    file_path = "models\json-data\prathiks-resume.json"
    json_data = load_json_file(file_path)
    recommendations = ats_recommendations(json_data)
    recommendations_json = jsonify({'suggestions' : recommendations})
    # recommendations_json = jsonify(recommendations)   
    return recommendations_json